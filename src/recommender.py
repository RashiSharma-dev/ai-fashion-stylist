import pandas as pd
import json
from color_recommender import load_color_rules


class OutfitRecommender:
    def __init__(self):
        self.df = pd.read_csv("data/outfits.csv")
        self.color_rules = load_color_rules()
        with open("data/recommendation_rules.json", "r") as f:
            self.rules = json.load(f)

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
    results = recommender.recommend("cool", "Party", "Winter")

    print(f"Found {len(results)} recommendations:\n")
    for outfit in results:
        print(f"Outfit #{outfit['outfit_id']}: {outfit['top_color']} + {outfit['bottom_color']} ({outfit['style_type']})")
        print(f"Why: {recommender.explain(outfit)}\n")
