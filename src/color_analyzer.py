import cv2
import numpy as np

class ColorAnalyzer:
    def __init__(self):
        self.colors = []

    def analyze(self, image_path):
        # Load the image
        img = cv2.imread(image_path)

        if img is None:
            print("Error: Could not load image!")
            return None

        # Convert to HSV
        hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Calculate average HSV
        avg_hue = np.mean(hsv_img[:, :, 0])
        avg_saturation = np.mean(hsv_img[:, :, 1])
        avg_value = np.mean(hsv_img[:, :, 2])

        result = {
            "hue": avg_hue,
            "saturation": avg_saturation,
            "value": avg_value
        }

        self.colors.append(result)

        return result

    def get_history(self):
        return self.colors


analyzer = ColorAnalyzer()

result1 = analyzer.analyze("data/photo.jpg")
print("Analysis result:", result1)

print("History so far:", analyzer.get_history())
