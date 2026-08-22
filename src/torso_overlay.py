import cv2
from color_overlay import apply_color_overlay

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)


def detect_face(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=8, minSize=(80, 80))

    if len(faces) == 0:
        return None

    return faces[0]


def estimate_torso_region(face_box, image_shape):
    x, y, w, h = face_box
    img_height, img_width = image_shape[:2]

    torso_top = y + h
    torso_bottom = y + (h * 3)

    width_expansion = int(w * 0.6)
    torso_left = x - width_expansion
    torso_right = x + w + width_expansion

    torso_top = max(0, torso_top)
    torso_bottom = min(img_height, torso_bottom)
    torso_left = max(0, torso_left)
    torso_right = min(img_width, torso_right)

    return torso_left, torso_top, torso_right, torso_bottom


def apply_torso_overlay(image, color_bgr, strength):
    face_box = detect_face(image)

    if face_box is None:
        return None, "No face detected"

    left, top, right, bottom = estimate_torso_region(face_box, image.shape)

    result = image.copy()

    torso_region = result[top:bottom, left:right]
    tinted_torso = apply_color_overlay(torso_region, color_bgr, strength)
    result[top:bottom, left:right] = tinted_torso

    return result, None


if __name__ == "__main__":
    image = cv2.imread("data/photo.jpg")

    red_bgr = (30, 30, 220)
    result, error = apply_torso_overlay(image, red_bgr, strength=50)

    if error:
        print(f"Error: {error}")
    else:
        cv2.imwrite("data/torso_overlay_test.jpg", result)
        print("Saved to data/torso_overlay_test.jpg")
