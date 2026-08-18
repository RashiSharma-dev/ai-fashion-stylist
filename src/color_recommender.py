import cv2
import numpy as np
import json
from image_validation import validate_image


def classify_skin_tone(h, s, v):
    if h <= 20 and s > 60:
        return "warm"
    elif h <= 20 and s <= 60:
        return "neutral"
    else:
        return "cool"


def load_color_rules():
    with open("data/color_rules.json", "r") as f:
        return json.load(f)


def get_recommended_colors(skin_tone):
    rules = load_color_rules()
    return rules[skin_tone]["best_colors"]


def analyze_and_recommend(image_path):
    try:
        is_valid, message = validate_image(image_path)
        if not is_valid:
            print(f"Validation failed: {message}")
            return {"error": message}

        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )

        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=8, minSize=(80, 80))

        if len(faces) == 0:
            return {"error": "No face detected. Please make sure your face is clearly visible and try again."}

        (x, y, w, h) = faces[0]
        face_region = img[y:y+h, x:x+w]
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

    except Exception as e:
        print(f"Unexpected error in analyze_and_recommend: {e}")
        return {"error": "Something went wrong while analyzing your photo. Please try again with a different image."}


if __name__ == "__main__":
    result = analyze_and_recommend("data/photo.jpg")
    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print(f"\nYour skin tone is: {result['skin_tone'].upper()}")
        color_names = [c["name"] for c in result["recommended_colors"]]
        print(f"Best colors for you: {', '.join(color_names)}")
