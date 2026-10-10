# src/color_recommender.py
import logging

import cv2
import numpy as np
import json
from image_validation import validate_image

# Used to record unexpected errors in the terminal (instead of print)
logger = logging.getLogger(__name__)


def classify_skin_tone(h, s, v):
    """
    Classify a skin tone as "warm", "neutral", or "cool" from average HSV values.

    h: hue, s: saturation, v: brightness (accepted but not used in the rules yet).
    """
    if h <= 20 and s > 60:
        return "warm"
    elif h <= 20 and s <= 60:
        return "neutral"
    else:
        return "cool"


def load_color_rules():
    """Load the skin tone color rules from data/color_rules.json and return them as a dict."""
    with open("data/color_rules.json", "r") as f:
        return json.load(f)


def get_recommended_colors(skin_tone):
    """Return the list of best colors (each with a name and hex code) for a skin tone."""
    rules = load_color_rules()
    return rules[skin_tone]["best_colors"]


def analyze_and_recommend(image_path):
    """
    Find the face in a photo, classify the skin tone, and recommend colors.

    Returns {"skin_tone": ..., "recommended_colors": [...]} on success,
    or {"error": "friendly message"} if the image is invalid, no face is found,
    or anything unexpected goes wrong.
    """
    try:
        is_valid, message = validate_image(image_path)
        if not is_valid:
            return {"error": message}

        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )

        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=8, minSize=(80, 80))

        if len(faces) == 0:
            return {"error": "No face detected. Please make sure your face is clearly visible and try again."}

        (face_x, face_y, face_width, face_height) = faces[0]
        face_region = img[face_y:face_y + face_height, face_x:face_x + face_width]
        face_hsv = cv2.cvtColor(face_region, cv2.COLOR_BGR2HSV)

        avg_hue = np.mean(face_hsv[:, :, 0])
        avg_saturation = np.mean(face_hsv[:, :, 1])
        avg_value = np.mean(face_hsv[:, :, 2])

        skin_tone = classify_skin_tone(avg_hue, avg_saturation, avg_value)
        recommended_colors = get_recommended_colors(skin_tone)

        return {
            "skin_tone": skin_tone,
            "recommended_colors": recommended_colors
        }

    except Exception:
        # Record the full technical details in the terminal, but show the user a friendly message
        logger.exception("Unexpected error in analyze_and_recommend")
        return {"error": "Something went wrong while analyzing your photo. Please try again with a different image."}


if __name__ == "__main__":
    result = analyze_and_recommend("data/photo.jpg")
    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print(f"\nYour skin tone is: {result['skin_tone'].upper()}")
        color_names = [c["name"] for c in result["recommended_colors"]]
        print(f"Best colors for you: {', '.join(color_names)}")
