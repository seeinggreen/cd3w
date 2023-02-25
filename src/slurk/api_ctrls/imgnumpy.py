
from PIL import Image
import numpy as np
import os

path = "./images/thumbnails"

files = os.listdir(path)

# Empty numpy array to store the images
image_stack = np.zeros((len(files), 256, 256, 3), dtype=np.uint8)

for i, file in enumerate(files):
    img = Image.open(os.path.join(path, file))
    img = img.resize((256, 256))  # resizing images
    image_stack[i] = np.array(img)

# Save the image stack as a .npy file
np.save("image_stack.npy", image_stack)
