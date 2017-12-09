import os
import sys

from PIL import Image
from PIL import ImageOps
from papirus import Papirus

class ImagePos():

    def __init__(self):
        self.papirus = Papirus()

    def write(self, image,x=0 ,y=0, W=10,H=10):
        image = Image.open(image)
        image = ImageOps.grayscale(image)

        rs = image
       # if W != self.papirus.width or H != self.papirus.height:
        rs = image.resize((W, H))
        bw = rs.convert("1", dither=Image.FLOYDSTEINBERG)

        self.papirus.display(bw)
        self.papirus.update()