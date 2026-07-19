import cv2
import numpy as np

# Load the face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Load the photo
img = cv2.imread("data/photo.jpg")

if img is None:
    print("Error: Could not load image!")
else:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=8, minSize=(80, 80))

    if len(faces) == 0:
        print("No face detected!")
    else:
        # Take the first detected face
        (x, y, w, h) = faces[0]

        # Crop the face region from the original color image
        face_region = img[y:y+h, x:x+w]

        # Save the cropped face so we can visually verify it
        cv2.imwrite("data/face_cropped.jpg", face_region)
        print("face_cropped.jpg saved!")

        # Convert the cropped face to HSV
        face_hsv = cv2.cvtColor(face_region, cv2.COLOR_BGR2HSV)

        # Calculate average HSV values of just the face region
        avg_hue = np.mean(face_hsv[:, :, 0])
        avg_saturation = np.mean(face_hsv[:, :, 1])
        avg_value = np.mean(face_hsv[:, :, 2])

        print(f"Average skin Hue: {avg_hue:.2f}")
        print(f"Average skin Saturation: {avg_saturation:.2f}")
        print(f"Average skin Value: {avg_value:.2f}")
