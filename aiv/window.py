import glfw

class Window(object):
    def __init__(self, width=800, height=600, title="aiv"):
        glfw.init()
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, 1)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        self.window = glfw.create_window(width, height, title, None, None)
        glfw.make_context_current(self.window)
        glfw.swap_interval(1)
        self.time = glfw.get_time()
        self.delta_time = 0

    def update(self):
        glfw.swap_buffers(self.window)
        glfw.poll_events()
        time = glfw.get_time()
        self.delta_time = time - self.time
        self.time = time

    @property
    def is_opened(self):
        return not glfw.window_should_close(self.window)

    def get_key(self, key):
        return glfw.get_key(self.window, key) == glfw.PRESS
