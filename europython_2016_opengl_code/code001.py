from aiv.window import Window

# import OpenGL functions
from aiv.opengl import *

# ask the OS for a drawable context
window = Window()

glClearColor(1, 0, 0, 1)

# the game loop
while window.is_opened:
    # clear the color buffer
    glClear(GL_COLOR_BUFFER_BIT)
    # draw the color buffer
    window.update()
