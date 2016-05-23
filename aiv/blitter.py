import pyglet


class Blitter(object):
    """
    this is a didactical class
    fir implementing a blittable canvas
    """

    def __init__(self, width, height, fmt='RGBA'):
        self.width = width
        self.height = height
        self.fmt = fmt
        self.window = pyglet.window.Window(width, height)
        self.draw_area = pyglet.image.create(width, height)
        self.bitmap = width * height * len(fmt) * [0]

    def _update(self):
        """
        this is a closure for setting the on_draw window hook
        """
        def draw():
            self.draw()
            data = ''
            size = self.width * self.height * len(self.fmt)
            stride = self.width * len(self.fmt)
            for i in range(size, -1, -stride):
                data += ''.join(map(chr, self.bitmap[i:i+stride]))
            self.draw_area.set_data(self.fmt, stride, data)
            self.draw_area.blit(0, 0, 0)
        return draw

    def run(self, hook):
        """
        run the whole app
        """
        self.window.on_draw = self._update()
        self.draw = hook
        pyglet.app.run()
