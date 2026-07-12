#Quiz Question 1: Write a function that loads an image and prints its shape.
import cv2

def load_and_show_shape(image_path):
    img = cv2.imread(image_path)
    print(img.shape)

load_and_show_shape("data/photo.jpg")
#Quiz Question 2: Write a class with an __init__ method and one other method.

class Wardrobe:
    def __init__(self):
        self.data = []
    def add_item(self, item):
            self.data.append(item)

my_wardrobe = Wardrobe()
my_wardrobe.add_item("Red shirt")
print(my_wardrobe.data)


