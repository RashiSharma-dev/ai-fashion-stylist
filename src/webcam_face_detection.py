import cv2
import time

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
else:
    print("Webcam opened. Press 'C' to capture a frame, 'Q' to quit.")

    prev_time = time.time()
    capture_count = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: Could not read frame from webcam.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=8, minSize=(80, 80))

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (217, 108, 140), 2)

        current_time = time.time()
        fps = 1 / (current_time - prev_time)
        prev_time = current_time

        cv2.putText(
            frame,
            f"FPS: {int(fps)}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (217, 108, 140),
            2
        )

        cv2.imshow("Live Face Detection", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('c') or key == ord('C'):
            capture_count += 1
            filename = f"data/capture_{capture_count}.jpg"
            cv2.imwrite(filename, frame)
            print(f"Captured frame saved as {filename}")

        if key == ord('q') or key == ord('Q') or key == 27:
            break

        if cv2.getWindowProperty("Live Face Detection", cv2.WND_PROP_VISIBLE) < 1:
            break

    cap.release()
    cv2.destroyAllWindows()
