import pandas as pd
import json
from color_recommender import load_color_rules

df = pd.read_csv("data/outfits.csv")
color_rules = load_color_rules()

skin_tones = ["warm", "cool", "neutral"]
occasions = ["Formal", "Casual", "Party"]
seasons = ["Summer", "Winter"]

rules = {}

for skin in skin_tones:
    recommended_names = [c["name"] for c in color_rules[skin]["best_colors"]]

    for occasion in occasions:
        for season in seasons:
            key = f"{skin}_{occasion.lower()}_{season.lower()}"

            exact_matches = df[
                (df["top_color"].isin(recommended_names)) &
                (df["occasion"] == occasion) &
                (df["season"] == season)
            ]

            if len(exact_matches) >= 3:
                chosen = exact_matches.head(3)
                match_level = "exact"
            else:
                relaxed_matches = df[
                    (df["top_color"].isin(recommended_names)) &
                    (df["occasion"] == occasion)
                ]
                if len(relaxed_matches) >= 3:
                    chosen = relaxed_matches.head(3)
                    match_level = "season_relaxed"
                else:
                    fallback_matches = df[df["top_color"].isin(recommended_names)]
                    chosen = fallback_matches.head(3)
                    match_level = "color_only"

            rules[key] = {
                "skin_tone": skin,
                "occasion": occasion,
                "season": season,
                "match_level": match_level,
                "outfit_ids": chosen["outfit_id"].tolist()
            }

with open("data/recommendation_rules.json", "w") as f:
    json.dump(rules, f, indent=4)

print(f"Generated {len(rules)} rule combinations.")
for key, value in rules.items():
    print(f"{key}: {len(value['outfit_ids'])} outfits ({value['match_level']})")
