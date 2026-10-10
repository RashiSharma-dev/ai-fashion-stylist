import numpy as np
from PIL import Image

# Practice 1: Create a simple array
simple_array = np.array([1, 2, 3])
print("Simple array:", simple_array)

# Practice 2: Create a 100x100 image that is pure red
# Shape = (height, width, 3) -> 3 is for Red, Green, Blue
height = 100
width = 100
red_image = np.zeros((height, width, 3), dtype=np.uint8)

# Set the Red channel (index 0) to 255 (full red), keep Green and Blue at 0
red_image[:, :, 0] = 255

print("Image shape:", red_image.shape)

# Practice 3: Save this array as an actual image file
img = Image.fromarray(red_image)
img.save("red.png")

print("red.png has been created!")
