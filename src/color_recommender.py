import cv2
import numpy as np
import json


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
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )

    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Could not load {image_path}")
        return None

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=8, minSize=(80, 80))

    if len(faces) == 0:
        print(f"No face detected in {image_path}")
        return None

    (x, y, w, h) = faces[0]
    face_region = img[y:y+h, x:x+w]
    face_hsv = cv2.cvtColor(face_region, cv2.COLOR_BGR2HSV)

    avg_hue = np.mean(face_hsv[:, :, 0])
    avg_saturation = np.mean(face_hsv[:, :, 1])
    avg_value = np.mean(face_hsv[:, :, 2])

    skin_tone = classify_skin_tone(avg_hue, avg_saturation, avg_value)
    recommended_colors = get_recommended_colors(skin_tone)

    print(f"\nYour skin tone is: {skin_tone.upper()}")
    print(f"Best colors for you: {', '.join(recommended_colors)}")

    return {
        "skin_tone": skin_tone,
        "recommended_colors": recommended_colors
    }


# Test it
result = analyze_and_recommend("data/photo.jpg")
