from aiv.draw import Window
from aiv.opengl import *

window = Window()

print(glGetString(GL_VERSION))

def clear_screen(window):
    for i in range(0, len(window.texture.pixels)):
        window.texture.pixels[i] = 0

def put_pixel(window, x, y, r, g, b, a=255):
    pos = y * window.texture.width * 4 + x * 4
    window.texture.pixels[pos] = r
    window.texture.pixels[pos+1] = g
    window.texture.pixels[pos+2] = b
    #window.texture.pixels[pos+3] = r

def draw_horizontal_line(window, x1, y1, width, r, g, b, a=255):
    for x in range(x1, x1+width):
        put_pixel(window, x, y1, r, g, b, a)

while window.is_opened:
    clear_screen(window)
    draw_horizontal_line(window, 10, 30, 200, 255, 0, 0)
    window.blit()
