from noise import pnoise2
import numpy as np
from PIL import Image

width, height = 512, 512
scale = 100.0

img = np.zeros((width, height))

for x in range(width):
    for y in range(height):
        img[x][y] = pnoise2(x/scale, y/scale, octaves=6)

img = (img - img.min()) / (img.max() - img.min())
img = (img * 255).astype(np.uint8)

Image.fromarray(img).save("heightmap.png")
