from aiv.window import Window
from aiv.opengl import *

window = Window(1024, 576)

glClearColor(0, 0, 1, 1)

while window.is_opened:
    glClear(GL_COLOR_BUFFER_BIT)
    window.update()
