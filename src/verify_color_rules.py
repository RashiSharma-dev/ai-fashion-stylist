import json

with open("data/color_rules.json", "r") as f:
    rules = json.load(f)

print("Skin tone categories:", list(rules.keys()))
print("\nWarm skin tone info:")
print(rules["warm"])

print("\nBest colors for cool skin tone:")
print(rules["cool"]["best_colors"])
