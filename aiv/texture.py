from PIL import Image
import numpy

class Texture(object):
    def __init__(self, width=0, height=0, filename=None):
        if filename != None:
            # opengl expect images data starting from bottom
            self.image = Image.open(filename).transpose(Image.FLIP_TOP_BOTTOM)
        else:
            self.image = Image.new(mode='RGBA', size=(width, height))
        # flatten the image data
        self.pixels = numpy.array([component for pixel in self.image.getdata() for component in pixel], dtype=numpy.uint8)

    @property
    def width(self):
        return self.image.size[0]

    @property
    def height(self):
        return self.image.size[1]
