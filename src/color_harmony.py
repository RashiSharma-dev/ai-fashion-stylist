import json
import math


def hex_to_rgb(hex_code):
    hex_code = hex_code.lstrip("#")
    r = int(hex_code[0:2], 16)
    g = int(hex_code[2:4], 16)
    b = int(hex_code[4:6], 16)
    return (r, g, b)


def color_distance(rgb1, rgb2):
    r1, g1, b1 = rgb1
    r2, g2, b2 = rgb2
    distance = math.sqrt((r1 - r2)**2 + (g1 - g2)**2 + (b1 - b2)**2)
    return distance


NAMED_COLORS = {
    "Red": "#ff0000",
    "Green": "#008000",
    "Blue": "#0000ff",
    "Orange": "#ffa500",
    "Yellow": "#ffff00",
    "Purple": "#800080",
    "Navy Blue": "#000080",
    "Mustard": "#ffdb58",
    "Maroon": "#800000",
    "Emerald Green": "#50c878",
    "Teal": "#008080",
    "Royal Blue": "#4169e1",
    "Beige": "#f5f5dc",
    "Camel": "#c19a6d",
}


def closest_color_name(hex_code, threshold=60):
    rgb = hex_to_rgb(hex_code)
    best_name = None
    best_distance = float("inf")

    for name, ref_hex in NAMED_COLORS.items():
        ref_rgb = hex_to_rgb(ref_hex)
        dist = color_distance(rgb, ref_rgb)
        if dist < best_distance:
            best_distance = dist
            best_name = name

    if best_distance <= threshold:
        return best_name
    return None


def load_harmony_pairs():
    with open("data/color_harmony.json", "r") as f:
        return json.load(f)


def is_good_combination(color1_hex, color2_hex):
    pairs = load_harmony_pairs()

    rgb1 = hex_to_rgb(color1_hex)
    rgb2 = hex_to_rgb(color2_hex)
    distance = color_distance(rgb1, rgb2)

    name1 = closest_color_name(color1_hex)
    name2 = closest_color_name(color2_hex)

    if distance < 40:
        return False, "Too Matchy"

    for pair in pairs["complementary_pairs"]:
        if (name1 in pair) and (name2 in pair):
            return True, "Great Contrast"

    for pair in pairs["analogous_pairs"]:
        if (name1 in pair) and (name2 in pair):
            return True, "Elegant Look"

    return True, "Neutral Combination"


if __name__ == "__main__":
    tests = [
        ("#000080", "#ffdb58"),  # Navy Blue vs Mustard — complementary
        ("#000080", "#4169e1"),  # Navy Blue vs Royal Blue — analogous
        ("#000080", "#000090"),  # Navy vs near-navy — too matchy
    ]

    for c1, c2 in tests:
        result, label = is_good_combination(c1, c2)
        print(f"{c1} + {c2} → {label} (Good: {result})")