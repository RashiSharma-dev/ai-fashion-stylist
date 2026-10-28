"""Speed check: measures how long the app's heavy operations take."""
import time

import cv2
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans


def time_it(label, function):
    """Run `function`, print how many milliseconds it took, and return its result."""
    start = time.perf_counter()
    result = function()
    elapsed_ms = (time.perf_counter() - start) * 1000
    print(f"{label:<35} {elapsed_ms:8.1f} ms")
    return result


def load_outfits():
    """Read the outfit CSV from disk."""
    return pd.read_csv("data/outfits.csv")


def load_face_detector():
    """Load OpenCV's Haar cascade face detector."""
    path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    return cv2.CascadeClassifier(path)


def run_kmeans():
    """Run K-Means with k=5 on a random 300x300 image, like the color extractor."""
    generator = np.random.default_rng(42)
    pixels = generator.integers(0, 256, size=(300 * 300, 3))
    return KMeans(n_clusters=5, n_init=10, random_state=42).fit(pixels)


def run_kmeans_fast():
    """Same test as run_kmeans, but with n_init=3 (the new setting used in the app)."""
    generator = np.random.default_rng(42)
    pixels = generator.integers(0, 256, size=(300 * 300, 3))
    return KMeans(n_clusters=5, n_init=3, random_state=42).fit(pixels)


if __name__ == "__main__":
    print("Speed check (smaller number = faster)")
    print("-" * 46)
    time_it("Read outfits.csv (1st time)", load_outfits)
    time_it("Read outfits.csv (2nd time)", load_outfits)
    time_it("Load Haar face detector", load_face_detector)
    time_it("K-Means, 90,000 pixels, k=5", run_kmeans)
    time_it("K-Means, n_init=3 (new)", run_kmeans_fast)
