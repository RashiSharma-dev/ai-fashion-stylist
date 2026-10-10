import cv2

# Step 1: Load the image
img = cv2.imread("data/photo.jpg")

# Check if image loaded successfully
if img is None:
    print("Error: Could not load image. Check the file path!")
else:
    print("Image loaded successfully!")
    print("Image shape:", img.shape)

    # Step 2: Convert BGR to RGB (so colors display correctly)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Step 3: Flip the image horizontally
    flipped_img = cv2.flip(img, 1)  # 1 = horizontal flip

    # Step 4: Save the flipped image
    cv2.imwrite("data/flipped.jpg", flipped_img)
    print("flipped.jpg has been saved!")
