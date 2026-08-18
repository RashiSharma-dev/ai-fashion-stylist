import cv2
import numpy as np


def validate_image(image_path):
    """
    Checks if an image file can be read and is bright enough to analyze.
    Returns a tuple: (is_valid: bool, message: str)
    """
    img = cv2.imread(image_path)

    if img is None:
        return False, "Could not read this file. Please make sure you uploaded a valid image (JPG or PNG)."

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    avg_brightness = np.mean(gray)

    if avg_brightness < 40:
        return False, f"This image looks too dark to analyze (brightness: {avg_brightness:.0f}/255). Please retake it in better lighting."

    return True, "Image looks good."
