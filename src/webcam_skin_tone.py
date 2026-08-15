import cv2
import time
import numpy as np
from skin_tone_classifier import classify_skin_tone

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

SWATCH_COLORS = {
    "warm": (30, 100, 220),
    "cool": (200, 100, 30),
    "neutral": (150, 150, 150),
}

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
else:
    print("Webcam opened. Press 'Q' to quit.")

    prev_time = time.time()
    frame_count = 0
    current_skin_tone = "detecting..."

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: Could not read frame from webcam.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=8, minSize=(80, 80))

        frame_count += 1

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (217, 108, 140), 2)

            if frame_count % 15 == 0:
                face_region = frame[y:y + h, x:x + w]
                face_hsv = cv2.cvtColor(face_region, cv2.COLOR_BGR2HSV)

                avg_hue = np.mean(face_hsv[:, :, 0])
                avg_saturation = np.mean(face_hsv[:, :, 1])
                avg_value = np.mean(face_hsv[:, :, 2])

                current_skin_tone = classify_skin_tone(avg_hue, avg_saturation, avg_value)

        current_time = time.time()
        fps = 1 / (current_time - prev_time)
        prev_time = current_time

        cv2.putText(
            frame, f"FPS: {int(fps)}", (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (217, 108, 140), 2
        )

        cv2.putText(
            frame, f"Skin Tone: {current_skin_tone.upper()}", (10, 70),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (217, 108, 140), 2
        )

        if current_skin_tone in SWATCH_COLORS:
            swatch_color = SWATCH_COLORS[current_skin_tone]
            cv2.rectangle(frame, (10, 90), (60, 140), swatch_color, -1)
            cv2.rectangle(frame, (10, 90), (60, 140), (255, 255, 255), 1)

        cv2.imshow("Live Skin Tone Detection", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == ord('Q') or key == 27:
            break

        if cv2.getWindowProperty("Live Skin Tone Detection", cv2.WND_PROP_VISIBLE) < 1:
            break

    cap.release()
    cv2.destroyAllWindows()
