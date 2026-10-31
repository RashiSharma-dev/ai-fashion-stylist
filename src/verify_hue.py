"""Hue check: tests whether the red wrap-around in HSV hue distorts the average hue of a face."""
import sys

import cv2
import numpy as np

from color_recommender import FACE_CASCADE


def hue_breakdown(image_path):
    """
    Measure how the hue values of the largest face in a photo are spread out.

    Returns {"error": None, plus plain_mean, median, wrapped_mean and the percentage
    of pixels in the low (0-20), middle (21-149) and high (150-179) hue ranges},
    or {"error": "message"} if the photo can't be read or has no face.
    """
    image = cv2.imread(image_path)
    if image is None:
        return {"error": "Could not read the photo."}

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = FACE_CASCADE.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=8, minSize=(80, 80))
    if len(faces) == 0:
        return {"error": "No face detected."}

    largest_face = max(faces, key=lambda face_box: face_box[2] * face_box[3])
    face_x, face_y, face_width, face_height = (int(value) for value in largest_face)
    face_region = image[face_y:face_y + face_height, face_x:face_x + face_width]

    hues = cv2.cvtColor(face_region, cv2.COLOR_BGR2HSV)[:, :, 0].astype(float)
    # Treat hues above 90 as slightly below zero, so reds at 175 and reds at 5 sit together
    wrapped_hues = np.where(hues > 90, hues - 180, hues)

    return {
        "error": None,
        "plain_mean": float(np.mean(hues)),
        "median": float(np.median(hues)),
        "wrapped_mean": float(np.mean(wrapped_hues)),
        "share_low": float(np.mean(hues <= 20) * 100),
        "share_middle": float(np.mean((hues > 20) & (hues < 150)) * 100),
        "share_high": float(np.mean(hues >= 150) * 100),
    }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python src/verify_hue.py path/to/selfie.jpg")
    else:
        result = hue_breakdown(sys.argv[1])
        if result["error"]:
            print(result["error"])
        else:
            print(f"Plain average hue (what the app uses): {result['plain_mean']:.1f}")
            print(f"Median hue:                            {result['median']:.1f}")
            print(f"Wrap-aware average hue:                {result['wrapped_mean']:.1f}")
            print(f"Pixels with hue 0-20 (skin range):     {result['share_low']:.1f}%")
            print(f"Pixels with hue 21-149 (greens/blues): {result['share_middle']:.1f}%")
            print(f"Pixels with hue 150-179 (wrapped red): {result['share_high']:.1f}%")
