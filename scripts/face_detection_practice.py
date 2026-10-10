import cv2

# Load the pre-trained face detector that comes with OpenCV
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Load your test photo
img = cv2.imread("data/photo.jpg")

if img is None:
    print("Error: Could not load image!")
else:
    # Convert to grayscale - face detection works better on grayscale images
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect faces (stricter settings to reduce false positives)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=8, minSize=(80, 80))

    print(f"Number of faces found: {len(faces)}")

    # Draw a rectangle around each detected face
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        print(f"Face found at position: x={x}, y={y}, width={w}, height={h}")

    # Save the result
    cv2.imwrite("data/face_detected.jpg", img)
    print("face_detected.jpg has been saved!")