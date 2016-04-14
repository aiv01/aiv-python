from aiv import window
from aiv.texture import Texture
from aiv.opengl import *
import numpy
from aiv.math.matrix4 import Matrix4
from aiv.input import KEY_LEFT, KEY_RIGHT

class Window(window.Window):

    vertex_shader = """
    #version 330 core
    layout(location = 0) in vec2 vertex;
    layout(location = 1) in vec2 uv;
    out vec2 uv_out;
    void main() {
        gl_Position = vec4(vertex.xy, 1, 1);
        uv_out = uv;
    }
    """

    fragment_shader = """
    #version 330 core
    in vec2 uv_out;
    out vec4 color;
    uniform sampler2D tex;
    void main() {
        color = texture(tex, uv_out);
    }
    """

    def __init__(self, width=800, height=600, title="aiv.draw"):
        super(Window, self).__init__(width, height, title)
        glClearColor(0, 0, 0, 1)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        vbo_vertices = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo_vertices)
        vertices = numpy.array([
            -1, -1,
            1, -1,
            -1, 1,
            -1, 1,
            1, 1,
            1, -1
        ], numpy.float32)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW) 
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, None)

        vbo_uv = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo_uv)
        uvs = numpy.array([
            0, 1,
            1, 1,
            0, 0,
            0, 0,
            1, 0,
            1, 1 
        ], numpy.float32)
        glBufferData(GL_ARRAY_BUFFER, uvs.nbytes, uvs, GL_STATIC_DRAW) 
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 0, None)
        
        self.tid = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.tid)

        self.texture = Texture(width=width, height=height)

        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.texture.width, self.texture.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, self.texture.pixels)

        vshader = glCreateShader(GL_VERTEX_SHADER)
        fshader = glCreateShader(GL_FRAGMENT_SHADER)

        glShaderSource(vshader, self.vertex_shader)
        glShaderSource(fshader, self.fragment_shader)

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

        glUseProgram(self.program)

    def blit(self):

        glClear(GL_COLOR_BUFFER_BIT)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.texture.width, self.texture.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, self.texture.pixels)

        glDrawArrays(GL_TRIANGLES, 0, 6)
        self.update()
