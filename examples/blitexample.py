from blitter import Blitter

# create an 800x600 window with blitting capabilities
window = Blitter(800, 600)


def put_pixel(x, y, r, g, b):
    """
    draw a pixel on the specified position
    """
    pos = y * window.width * 4 + x * 4
    window.bitmap[pos] = r
    window.bitmap[pos+1] = g
    window.bitmap[pos+2] = b
    window.bitmap[pos+3] = 255


def clear_red():
    """
    fill all pixels with red
    """
    for y in range(0, window.height):
        for x in range(0, window.width):
            put_pixel(x, y, 255, 0, 0)


def draw():
    """
    this will be called at every refresh
    """
    clear_red()
    put_pixel(window.width/2, window.height/2, 0, 0, 255)

# run the app using the draw function as the hook
window.run(draw)
