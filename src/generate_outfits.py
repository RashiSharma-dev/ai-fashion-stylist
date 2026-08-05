import pandas as pd
import itertools
import random

random.seed(42)

top_colors = [
    "Olive Green", "Camel", "Mustard", "Warm Red", "Orange", "Coral", "Gold", "Terracotta",
    "Royal Blue", "Emerald Green", "True Red", "Purple", "Fuchsia", "Silver", "Navy", "Lavender",
    "Soft White", "Grey", "Rose Pink", "Teal", "Mauve", "Jade", "Soft Blue", "Blush"
]

bottom_colors = ["Black", "White", "Navy", "Grey", "Beige", "Denim Blue"]

occasions = ["Formal", "Casual", "Party", "Office", "Wedding"]
seasons = ["Summer", "Winter", "Autumn", "Spring"]
style_types = ["Ethnic", "Western", "Fusion", "Minimalist", "Bohemian"]
genders = ["Male", "Female", "Unisex"]

rows = []
outfit_id = 1

for i in range(60):
    top = random.choice(top_colors)
    bottom = random.choice(bottom_colors)
    occasion = random.choice(occasions)
    season = random.choice(seasons)
    style = random.choice(style_types)
    gender = random.choice(genders)

    rows.append({
        "outfit_id": outfit_id,
        "top_color": top,
        "bottom_color": bottom,
        "occasion": occasion,
        "season": season,
        "style_type": style,
        "gender": gender
    })
    outfit_id += 1

df = pd.DataFrame(rows)
df.to_csv("data/outfits.csv", index=False)

print(f"Generated {len(df)} outfit rows.")
print(df.head(10))
