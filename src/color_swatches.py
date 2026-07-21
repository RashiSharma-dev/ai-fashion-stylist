from PIL import Image, ImageDraw


def make_swatch(color_name, hex_code, size=80):
    """Creates a small solid-color square image (a swatch) for a given color."""
    img = Image.new("RGB", (size, size), hex_code)
    return img


# Quick test
if __name__ == "__main__":
    swatch = make_swatch("Royal Blue", "#4169E1")
    swatch.save("data/test_swatch.png")
    print("test_swatch.png saved!")
