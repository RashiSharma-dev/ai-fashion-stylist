import pandas as pd
from color_recommender import load_color_rules


def filter_outfits(skin_tone, occasion, season, top_n=5):
    rules = load_color_rules()
    recommended_names = [c["name"] for c in rules[skin_tone]["best_colors"]]

    df = pd.read_csv("data/outfits.csv")

    matches = df[
        (df["top_color"].isin(recommended_names)) &
        (df["occasion"].str.lower() == occasion.lower()) &
        (df["season"].str.lower() == season.lower())
    ]

    return matches.head(top_n)


if __name__ == "__main__":
    result = filter_outfits("warm", "Casual", "Summer")
    print(f"Found {len(result)} matching outfits:\n")
    print(result)
