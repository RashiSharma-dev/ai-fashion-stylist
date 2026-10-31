"""Depth-prep demo: shows the HSV numbers and K-Means color shares behind the app's decisions."""
import sys

import cv2
import numpy as np
from sklearn.cluster import KMeans

from color_recommender import FACE_CASCADE, classify_skin_tone
from dominant_color_extractor import resize_for_speed


def average_hsv(face_region):
    """Return the average (hue, saturation, value) of a BGR image region as three floats."""
    face_hsv = cv2.cvtColor(face_region, cv2.COLOR_BGR2HSV)
    return (
        float(np.mean(face_hsv[:, :, 0])),
        float(np.mean(face_hsv[:, :, 1])),
        float(np.mean(face_hsv[:, :, 2])),
    )


def face_report(image_path):
    """
    Detect every face in a photo and describe the first one and the largest one.

    Saves each of those two face crops to data/debug_face_first.jpg and
    data/debug_face_largest.jpg so you can look at what the detector picked.
    Returns {"error": None, "face_count": n, "reports": [...]} on success, or
    {"error": "message", "face_count": 0, "reports": []} if the photo can't be
    read or has no face.
    """
    image = cv2.imread(image_path)
    if image is None:
        return {"error": "Could not read the photo.", "face_count": 0, "reports": []}

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = FACE_CASCADE.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=8, minSize=(80, 80))
    if len(faces) == 0:
        return {"error": "No face detected.", "face_count": 0, "reports": []}

    first_face = faces[0]
    largest_face = max(faces, key=lambda box: box[2] * box[3])

    reports = []
    for label, box in (("first", first_face), ("largest", largest_face)):
        face_x, face_y, face_width, face_height = (int(value) for value in box)
        face_region = image[face_y:face_y + face_height, face_x:face_x + face_width]
        hue, saturation, brightness = average_hsv(face_region)
        cv2.imwrite(f"data/debug_face_{label}.jpg", face_region)
        reports.append({
            "label": label,
            "box": (face_x, face_y, face_width, face_height),
            "hue": hue,
            "saturation": saturation,
            "brightness": brightness,
            "skin_tone": classify_skin_tone(hue, saturation, brightness),
        })
    return {"error": None, "face_count": len(faces), "reports": reports}


def color_shares(image_path, k=5):
    """
    Cluster a photo's colors with K-Means and report each cluster's share of the pixels.

    Returns {"error": None, "colors": [((r, g, b), percent), ...]} sorted from biggest
    to smallest, or {"error": "message", "colors": []} if the photo can't be read.
    """
    image = cv2.imread(image_path)
    if image is None:
        return {"error": "Could not read the photo.", "colors": []}

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = resize_for_speed(image)
    pixels = image.reshape(-1, 3)

    model = KMeans(n_clusters=k, random_state=42, n_init=3).fit(pixels)
    counts = np.bincount(model.labels_, minlength=k)
    shares = counts / counts.sum() * 100

    colors = []
    for center, share in zip(model.cluster_centers_.astype(int), shares):
        colors.append((tuple(int(channel) for channel in center), round(float(share), 1)))
    colors.sort(key=lambda item: item[1], reverse=True)
    return {"error": None, "colors": colors}


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in ("hsv", "kmeans"):
        print("Usage: python src/verify_depth.py hsv path/to/selfie.jpg")
        print("   or: python src/verify_depth.py kmeans path/to/clothing.jpg")
    elif sys.argv[1] == "hsv":
        result = face_report(sys.argv[2])
        if result["error"]:
            print(result["error"])
        else:
            print(f"Faces found: {result['face_count']}")
            for report in result["reports"]:
                print(f"--- {report['label']} face, box (x, y, w, h) = {report['box']}")
                print(f"Average hue:        {report['hue']:.1f}   (rule cut-off: 20)")
                print(f"Average saturation: {report['saturation']:.1f}   (rule cut-off: 60)")
                print(f"Average value:      {report['brightness']:.1f}   (not used in the rules)")
                print(f"Skin tone result:   {report['skin_tone']}")
    else:
        result = color_shares(sys.argv[2])
        if result["error"]:
            print(result["error"])
        else:
            for color, share in result["colors"]:
                print(f"RGB {color}  ->  {share}% of the pixels")