import os
import os.path
from PIL import Image

WIDTH = 300
HEIGHT = 300


def ResizeImage(imageDir, width=WIDTH, height=HEIGHT):
    img = Image.open(imageDir)
    out = img.resize((width, height),Image.ANTIALIAS) #resize image with high-quality
    out.save(imageDir)
