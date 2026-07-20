import cv2
import numpy as np

def classify_skin_tone(h, s, v):
    """
    Classifies skin tone as warm, cool, or neutral based on HSV values.
    h = Hue (0-179 in OpenCV)
    s = Saturation (0-255)
    v = Value/Brightness (0-255)
    """
    if h <= 20 and s > 60:
        return "warm"
    elif h <= 20 and s <= 60:
        return "neutral"
    else:
        return "cool"


def analyze_photo(image_path):
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

    print(f"\nImage: {image_path}")
    print(f"Hue: {avg_hue:.2f}, Saturation: {avg_saturation:.2f}, Value: {avg_value:.2f}")
    print(f"Classified skin tone: {skin_tone.upper()}")

    return skin_tone


# Test it on your photo
analyze_photo("data/photo.jpg")
