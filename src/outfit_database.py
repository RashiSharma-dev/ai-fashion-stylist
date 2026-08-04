import pandas as pd
from color_recommender import get_recommended_colors


def load_outfits():
    return pd.read_csv("data/outfits.csv")


def filter_outfits(skin_tone, occasion, season, top_n=5):
    df = load_outfits()

    recommended = get_recommended_colors(skin_tone)
    recommended_names = [c["name"].lower() for c in recommended]

    df["top_color_lower"] = df["top_color"].str.lower()

    matches = df[
        (df["top_color_lower"].isin(recommended_names)) &
        (df["occasion"].str.lower() == occasion.lower()) &
        (df["season"].str.lower() == season.lower())
    ]

    matches = matches.drop(columns=["top_color_lower"])

    return matches.head(top_n)


if __name__ == "__main__":
    results = filter_outfits("cool", "Party", "Winter")
    print(f"Found {len(results)} matching outfits:")
    print(results)
