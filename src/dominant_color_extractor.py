import cv2
import numpy as np
from sklearn.cluster import KMeans

def extract_dominant_colors(image_path, k=5):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    pixels = image.reshape(-1, 3)

    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(pixels)

    dominant_colors = kmeans.cluster_centers_.astype(int)

    return [tuple(int(c) for c in color) for color in dominant_colors]


if __name__ == "__main__":
    colors = extract_dominant_colors("data/shirt.jpeg")
    print("Top 5 Dominant Colors (RGB):")
    for color in colors:
        print(color)
def get_most_dominant_color(image_path, k=5):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    pixels = image.reshape(-1, 3)

    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(pixels)

    counts = np.bincount(kmeans.labels_)
    dominant_index = np.argmax(counts)
    dominant_color = kmeans.cluster_centers_[dominant_index].astype(int)

    return tuple(int(c) for c in dominant_color)