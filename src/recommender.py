import pandas as pd
import json
from color_recommender import load_color_rules
from color_harmony import hex_to_rgb, color_distance

BOTTOM_COLOR_HEX = {
    "Black": "#000000",
    "White": "#FFFFFF",
    "Navy": "#000080",
    "Grey": "#808080",
    "Beige": "#F5F5DC",
    "Denim Blue": "#1560BD",
}

OCCASION_FIT_SCORES = {
    "exact": 100,
    "season_relaxed": 70,
    "color_only": 40,
}


class OutfitRecommender:
    def __init__(self):
        self.df = pd.read_csv("data/outfits.csv")
        self.color_rules = load_color_rules()
        with open("data/recommendation_rules.json", "r") as f:
            self.rules = json.load(f)

    def get_color_hex(self, color_name):
        if color_name in BOTTOM_COLOR_HEX:
            return BOTTOM_COLOR_HEX[color_name]

        for skin_data in self.color_rules.values():
            for c in skin_data["best_colors"]:
                if c["name"] == color_name:
                    return c["hex"]

        return "#CCCCCC"

    def calculate_skin_match(self, top_color, skin_tone):
        top_hex = self.get_color_hex(top_color)
        top_rgb = hex_to_rgb(top_hex)
        recommended = self.color_rules[skin_tone]["best_colors"]

        distances = [color_distance(top_rgb, hex_to_rgb(c["hex"])) for c in recommended]
        avg_distance = sum(distances) / len(distances)

        if avg_distance < 60:
            return 100
        elif avg_distance < 100:
            return 90
        elif avg_distance < 150:
            return 75
        else:
            return 60

    def calculate_color_harmony(self, top_color, bottom_color):
        top_hex = self.get_color_hex(top_color)
        bottom_hex = self.get_color_hex(bottom_color)
        distance = color_distance(hex_to_rgb(top_hex), hex_to_rgb(bottom_hex))

        if distance < 40:
            return 40, "Too Matchy"
        elif distance < 150:
            return 85, "Elegant Look"
        else:
            return 90, "Great Contrast"

    def calculate_match_score(self, outfit):
        skin_score = self.calculate_skin_match(outfit["top_color"], outfit["skin_tone"])
        harmony_score, harmony_label = self.calculate_color_harmony(outfit["top_color"], outfit["bottom_color"])
        occasion_score = OCCASION_FIT_SCORES[outfit["match_level"]]

        total = round(skin_score * 0.4 + harmony_score * 0.3 + occasion_score * 0.3)

        return {
            "total": total,
            "skin_match": skin_score,
            "color_harmony": harmony_score,
            "harmony_label": harmony_label,
            "occasion_fit": occasion_score,
        }

    def recommend(self, skin_tone, occasion, season, top_n=5):
        recommended_names = [c["name"] for c in self.color_rules[skin_tone]["best_colors"]]

        exact = self.df[
            (self.df["top_color"].isin(recommended_names)) &
            (self.df["occasion"] == occasion) &
            (self.df["season"] == season)
        ]

        if len(exact) >= top_n:
            chosen = exact.head(top_n)
            match_level = "exact"
        else:
            relaxed = self.df[
                (self.df["top_color"].isin(recommended_names)) &
                (self.df["occasion"] == occasion)
            ]
            if len(relaxed) >= top_n:
                chosen = relaxed.head(top_n)
                match_level = "season_relaxed"
            else:
                fallback = self.df[self.df["top_color"].isin(recommended_names)]
                chosen = fallback.head(top_n)
                match_level = "color_only"

        outfits = chosen.to_dict("records")
        for outfit in outfits:
            outfit["match_level"] = match_level
            outfit["skin_tone"] = skin_tone

        return outfits

    def explain(self, outfit):
        color = outfit["top_color"]
        skin = outfit["skin_tone"]
        level = outfit["match_level"]

        reason = f"{color} is a recommended color for {skin} skin tones."

        if level == "exact":
            reason += f" This outfit also matches your selected occasion ({outfit['occasion']}) and season ({outfit['season']}) exactly."
        elif level == "season_relaxed":
            reason += f" This outfit matches your occasion ({outfit['occasion']}), though shown across seasons since exact-season options were limited."
        else:
            reason += " This outfit was selected primarily for its color compatibility with your skin tone, as occasion/season matches were limited in the dataset."

        return reason


if __name__ == "__main__":
    recommender = OutfitRecommender()
    results = recommender.recommend("warm", "Casual", "Summer")

    for outfit in results:
        score = recommender.calculate_match_score(outfit)
        print(f"Outfit #{outfit['outfit_id']}: {outfit['top_color']} + {outfit['bottom_color']}")
        print(f"  Total: {score['total']}% | Skin: {score['skin_match']}% | Harmony: {score['color_harmony']}% ({score['harmony_label']}) | Occasion: {score['occasion_fit']}%")
