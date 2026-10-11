import pandas as pd
import itertools
import random

random.seed(42)

top_colors = [
    "Navy Blue", "Royal Blue", "Emerald Green", "Olive Green", "Maroon",
    "True Red", "Mustard", "Camel", "Beige", "Charcoal",
    "Purple", "Lavender", "Fuchsia", "Silver", "Rust", "Teal"
]

bottom_colors = [
    "Black", "White", "Denim Blue", "Beige", "Charcoal",
    "Navy Blue", "Camel", "Grey", "Olive Green", "Cream"
]

occasions = ["Casual", "Formal", "Party", "Business", "Wedding"]
seasons = ["Summer", "Winter", "Spring", "Autumn"]
style_types = ["Western", "Ethnic", "Streetwear", "Minimalist"]

all_combinations = list(itertools.product(
    top_colors, bottom_colors, occasions, seasons, style_types
))

random.shuffle(all_combinations)

selected = all_combinations[:55]

rows = []
for i, (top, bottom, occasion, season, style) in enumerate(selected, start=1):
    rows.append({
        "outfit_id": i,
        "top_color": top,
        "bottom_color": bottom,
        "occasion": occasion,
        "season": season,
        "style_type": style
    })

df = pd.DataFrame(rows)
df.to_csv("data/outfits.csv", index=False)

print(f"Generated {len(df)} outfit rows.")
print(df.head(10))

