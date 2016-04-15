from aiv.opengl import *

class Shader(object):

    def __init__(self, vertex_shader, fragment_shader):
        vshader = glCreateShader(GL_VERTEX_SHADER)
        fshader = glCreateShader(GL_FRAGMENT_SHADER)

        glShaderSource(vshader, vertex_shader)
        glShaderSource(fshader, fragment_shader)

        glCompileShader(vshader)
        glCompileShader(fshader)

        self.program = glCreateProgram()

        glAttachShader(self.program, vshader)
        glAttachShader(self.program, fshader)

        glLinkProgram(self.program)

        glDetachShader(self.program, vshader)
        glDetachShader(self.program, fshader)

        glDeleteShader(vshader)
        glDeleteShader(fshader)

    def use(self):
        glUseProgram(self.program)

    def get_uniform(self, name):
        return glGetUniformLocation(self.program, name)
