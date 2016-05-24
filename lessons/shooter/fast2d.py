import pyglet

Key = pyglet.window.key


class Window(object):
    """
    This is the main class needed for
    creating a drawable context and for
    getting keyboard input
    """

    def __init__(self, width, height, title='Fast2D',
                 fps=60.0, fullscreen=False):
        self.fps = fps
        self.window = pyglet.window.Window(width, height, caption=title,
                                           fullscreen=fullscreen)
        self.keyboard = {}

    @property
    def width(self):
        return self.window.width

    @property
    def height(self):
        return self.window.height

    def clear(self, r=0.0, g=0.0, b=0.0):
        """
        fast clear of the screen using opengl
        """
        pyglet.gl.glClearColor(r/255.0, g/255.0, b/255.0, 1)
        self.window.clear()

    def get_key(self, key):
        return self.keyboard.get(key, False)

    def _keyboard_down(self):
        """
        hook for filling the keyboard table
        """
        def key_down(symbol, modifier):
            self.keyboard[symbol] = True
        return key_down

    def _keyboard_up(self):
        """
        hook for filling the keyboard table
        """
        def key_up(symbol, modifier):
            self.keyboard[symbol] = False
        return key_up

    def run(self, hook):
        """
        call this to start your game
        """
        self.hook = hook

        def _update(delta_time):
            self.delta_time = delta_time
            self.hook()
        pyglet.clock.schedule_interval(_update, 1.0/self.fps)
        self.window.on_key_press = self._keyboard_down()
        self.window.on_key_release = self._keyboard_up()
        pyglet.app.run()


class Text(object):
    """
    A simple class for drawing text
    """
    def __init__(self, text=''):
        self.label = pyglet.text.Label(text)
        self.x = 0.0
        self.y = 0.0

    @property
    def text(self):
        return self.label.text

    @text.setter
    def text(self, value):
        self.label.text = value

    def set_color(self, r, g, b):
        self.label.color = (r, g, b, 255)

    def draw(self):
        self.label.x = self.x
        self.label.y = self.y
        self.label.draw()


class Image(object):
    """
    A simple class for loading images
    """
    def __init__(self, filename):
        self.image = pyglet.image.load(filename)


class Sprite(object):
    """
    A Sprite is a generic object that can be drawned on screen
    """
    def __init__(self, filename):
        self.image = pyglet.image.load(filename)
        self.sprite = pyglet.sprite.Sprite(self.image)
        self.x = 0.0
        self.y = 0.0

    @property
    def width(self):
        return self.sprite.width

    @property
    def height(self):
        return self.sprite.height

    def draw(self, image=None):
        if image is not None:
            self.sprite.image = image.image
        self.sprite.x = self.x
        self.sprite.y = self.y
        self.sprite.draw()


class Box(object):
    """
    This is a bounding box implementation
    with graphics representation

    box coordinates are relative to other objects
    (like sprites)
    """

    def __init__(self, xoffset, yoffset, width, height, r=0, g=0, b=0, a=0):
        pattern = pyglet.image.SolidColorImagePattern(color=(r, g, b, a))
        self.image = pattern.create_image(int(width), int(height))
        self.sprite = pyglet.sprite.Sprite(self.image)
        self.xoffset = xoffset
        self.yoffset = yoffset
        self.width = width
        self.height = height
        self.drawn = False

    def draw(self, x, y):
        self.sprite.x = x + self.xoffset
        self.sprite.y = y + self.yoffset
        self.x = self.sprite.x
        self.y = self.sprite.y
        self.sprite.draw()
        self.drawn = True

    def intersects(self, other_box):
        """
        check for 2 boxes intersection
        the box position must be updated with a draw
        """
        if not self.drawn or not other_box.drawn:
            return False
        if self.x + self.width < other_box.x:
            return False
        if self.x > other_box.x+other_box.width:
            return False
        if self.y + self.height < other_box.y:
            return False
        if self.y > other_box.y+other_box.height:
            return False
        return True
