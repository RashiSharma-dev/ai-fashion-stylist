import cv2
import numpy as np
from sklearn.cluster import KMeans
image = cv2.imread("data/shirt.jpeg")
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
pixels = image.reshape(-1, 3)
kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
kmeans.fit(pixels)
dominant_colors = kmeans.cluster_centers_.astype(int)

print("Top 5 Dominant Colors (RGB):")
for color in dominant_colors:
    print(tuple(int(c) for c in color))