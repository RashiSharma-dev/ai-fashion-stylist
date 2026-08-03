from color_recommender import analyze_and_recommend, load_color_rules
from dominant_color_extractor import get_most_dominant_color
from palette_generator import rgb_to_hex
from color_harmony import hex_to_rgb, color_distance


def get_all_known_colors():
    rules = load_color_rules()
    all_colors = {}
    for skin_tone, data in rules.items():
        for c in data["best_colors"]:
            all_colors[c["name"]] = c["hex"]
    return all_colors


def identify_color_name(hex_code, known_colors, threshold=80):
    rgb = hex_to_rgb(hex_code)
    best_name = None
    best_distance = float("inf")

    for name, ref_hex in known_colors.items():
        dist = color_distance(rgb, hex_to_rgb(ref_hex))
        if dist < best_distance:
            best_distance = dist
            best_name = name

    return best_name, best_distance


def check_outfit_compatibility(selfie_path, outfit_path):
    skin_result = analyze_and_recommend(selfie_path)
    if skin_result is None:
        return None

    skin_tone = skin_result["skin_tone"]
    recommended_colors = skin_result["recommended_colors"]
    recommended_names = [c["name"] for c in recommended_colors]

    dominant_rgb = get_most_dominant_color(outfit_path)
    dominant_hex = rgb_to_hex(dominant_rgb)

    known_colors = get_all_known_colors()
    outfit_color_name, distance = identify_color_name(dominant_hex, known_colors)

    is_recommended = outfit_color_name in recommended_names

    if is_recommended:
        message = f"This outfit's color is {outfit_color_name.upper()} — Excellent for your {skin_tone} skin tone ✓"
    else:
        message = f"This outfit's color is {outfit_color_name.upper()} — Not ideal for your {skin_tone} skin tone ✗"

    return {
        "skin_tone": skin_tone,
        "outfit_color_name": outfit_color_name,
        "outfit_hex": dominant_hex,
        "is_recommended": is_recommended,
        "message": message
    }


if __name__ == "__main__":
    result = check_outfit_compatibility("data/photo.jpg", "data/shirt.jpeg")
    if result:
        print(result["message"])
