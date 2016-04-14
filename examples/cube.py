from aiv.window import Window
from aiv.opengl import *
import numpy
from aiv.math.matrix4 import Matrix4
from aiv.input import KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN

window = Window()

vertex_shader = """
    #version 330 core
    layout(location = 0) in vec3 vertex;
    uniform mat4 world;
    uniform mat4 camera;
    out vec4 color;
    void main() {
        gl_Position = camera * world * vec4(vertex, 1);
        color = vec4(vertex, 1);
    }
    """

fragment_shader = """
    #version 330 core
    in vec4 color;
    out vec4 final_color;
    void main() {
        final_color = color;
    }
    """

glClearColor(0, 0, 0, 1)
glEnable(GL_DEPTH_TEST)

vao = glGenVertexArrays(1)
glBindVertexArray(vao)

vbo_vertices = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vbo_vertices)
vertices = numpy.array([
            # front
            -1, -1, 1,
            1, -1, 1,
            -1, 1, 1,

            -1, 1, 1,
            1, 1, 1,
            1, -1, 1,

            # back
            -1, -1, -1,
            1, -1, -1,
            -1, 1, -1,

            -1, 1, -1,
            1, 1, -1,
            1, -1, -1,

            # right
            1, 1, 1,
            1, -1, 1,
            1, -1, -1,

            1, 1, 1,
            1, 1, -1,
            1, -1, -1,

            # left
            -1, 1, 1,
            -1, -1, 1,
            -1, -1, -1,

            -1, 1, 1,
            -1, 1, -1,
            -1, -1, -1,

            # top
            -1, 1, 1,
            1, 1, 1,
            -1, 1, -1,

            -1, 1, -1,
            1, 1, -1,
            1, 1, 1,

            # bottom
            -1, -1, 1,
            1, -1, 1,
            -1, -1, -1,

            -1, -1, -1,
            1, -1, -1,
            1, -1, 1
        ], numpy.float32)
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW) 
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)


vshader = glCreateShader(GL_VERTEX_SHADER)
fshader = glCreateShader(GL_FRAGMENT_SHADER)

glShaderSource(vshader, vertex_shader)
glShaderSource(fshader, fragment_shader)

glCompileShader(vshader)
glCompileShader(fshader)

program = glCreateProgram()

glAttachShader(program, vshader)
glAttachShader(program, fshader)

glLinkProgram(program)
        
glDetachShader(program, vshader)
glDetachShader(program, fshader)

glDeleteShader(vshader)
glDeleteShader(fshader)

glUseProgram(program)

world = glGetUniformLocation(program, "world")
camera = glGetUniformLocation(program, "camera")

yrot = 0
xrot = 0

while window.is_opened:

        if window.get_key(KEY_RIGHT):
            yrot += 60 * window.delta_time

        if window.get_key(KEY_LEFT):
            yrot -= 60 * window.delta_time

        if window.get_key(KEY_UP):
            xrot += 60 * window.delta_time

        if window.get_key(KEY_DOWN):
            xrot -= 60 * window.delta_time

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        #mat = Matrix4.scale(1, 1, 1) * Matrix4.rotate_y(yrot) * Matrix4.rotate_x(xrot) * Matrix4.translate(0, 0, -5)
        mat = Matrix4.translate(0, 0, -5) * Matrix4.rotate_x(xrot) * Matrix4.rotate_y(yrot) * Matrix4.scale(1, 1, 1)

        cam = Matrix4.perspective(60, 800.0/600.0, 0.1, 100) * Matrix4.look_at(0, 0, 5, 0, 0, 0, 0, 1, 0)

        glUniformMatrix4fv(world, 1, GL_FALSE, mat.m)
        glUniformMatrix4fv(camera, 1, GL_FALSE, cam.m)

        glDrawArrays(GL_TRIANGLES, 0, 6 * 6)
        window.update()
