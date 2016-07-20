from aiv.window import Window

# ask the OS for a drawable context
window = Window()

# the game loop
while window.is_opened:
    # draw the color buffer
    window.update()
