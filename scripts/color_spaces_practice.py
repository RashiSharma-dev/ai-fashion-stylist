import cv2
import numpy as np

img = cv2.imread("data/photo.jpg")

if img is None: 
    print("Error: Could not load image!")
else:
    # # Convert BGR to HSV
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

 # For this exercise, let's isolate "red" colors using HSV ranges
 # Red in HSV can appear in two ranges (because Hue wraps around like a circle)
lower_red1 = np.array([0, 70, 50])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([170, 70, 50])
upper_red2 = np.array([180, 255, 255])

# Create masks - a "mask" is like a stencil that only shows pixels matching our color range
mask1  = cv2.inRange(hsv_img, lower_red1, upper_red1)
mask2 = cv2.inRange(hsv_img, lower_red2, upper_red2)
red_mask = mask1+mask2

# Apply the mask to isolate red regions from the original image
red_only = cv2.bitwise_and(img, img, mask=red_mask)

# Calculate average HSV values of the WHOLE image 
avg_hue = np.mean(hsv_img[:,:,0])
avg_saturation = np.mean(hsv_img[:,:,1])
avg_value = np.mean(hsv_img[:,:,2])

print(f"Dominant Hue: {avg_hue:.2f}")
print(f"Saturation: {avg_saturation:.2f}")
print(f"Value: {avg_hue:.2f}")

 # Save the red-isolated image so you can see the effect
cv2.imwrite("data/red_isolated.jpg", red_only)
print("red_isolated.jpg has been saved!")