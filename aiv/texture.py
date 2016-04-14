from PIL import Image
import numpy

class Texture(object):
    def __init__(self, width=0, height=0, filename=None):
        if filename != None:
            self.image = Image.open(filename).transpose(Image.FLIP_TOP_BOTTOM)
        else:
            self.image = Image.new(mode='RGBA', size=(width, height))
        self.pixels = numpy.asarray(self.image.getdata(), dtype=numpy.uint8)

    @property
    def width(self):
        return self.image.size[0]

    @property
    def height(self):
        return self.image.size[1]
