# src/palette_generator.py
from PIL import Image, ImageDraw


def rgb_to_hex(rgb):
    """Convert an (r, g, b) tuple into a hex color string like "#ff8800"."""
    return "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2])


def create_palette_image(colors, square_size=50):
    """
    Draw a row of color squares, one per (r, g, b) color in the list.

    Each square is square_size pixels wide and tall. Returns a PIL image.
    """
    width = square_size * len(colors)
    height = square_size

    palette = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(palette)

    for i, color in enumerate(colors):
        x0 = i * square_size
        y0 = 0
        x1 = x0 + square_size
        y1 = y0 + square_size
        draw.rectangle([x0, y0, x1, y1], fill=color)

    return palette


if __name__ == "__main__":
    from dominant_color_extractor import extract_dominant_colors

    colors = extract_dominant_colors("data/shirt.jpeg")
    palette = create_palette_image(colors)
    palette.save("data/palette_test.png")

    for color in colors:
        print(rgb_to_hex(color))
