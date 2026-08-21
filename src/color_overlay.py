import cv2
import numpy as np


def create_color_layer(shape, color_bgr):
    color_layer = np.full(shape, color_bgr, dtype=np.uint8)
    return color_layer


def apply_color_overlay(image, color_bgr, strength):
    alpha = strength / 100

    color_layer = create_color_layer(image.shape, color_bgr)

    blended = cv2.addWeighted(image, 1 - alpha, color_layer, alpha, 0)

    return blended


if __name__ == "__main__":
    image = cv2.imread("data/photo.jpg")

    red_bgr = (30, 30, 220)
    result = apply_color_overlay(image, red_bgr, strength=40)

    cv2.imwrite("data/overlay_test.jpg", result)
    print("Saved overlay test to data/overlay_test.jpg")
