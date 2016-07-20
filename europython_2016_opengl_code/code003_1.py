from aiv.window import Window
from aiv.opengl import *
import numpy

window = Window()

glClearColor(1, 0, 0, 1)

# allocate vao on the GPU
vao = glGenVertexArrays(1)
glBindVertexArray(vao)

# allocate a vbo for vertices on the GPU
vbo = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vbo)

# upload vertices data to the buffer
vertices = numpy.array([ 0, 1, -1, -1, 1, -1], dtype=numpy.float32)
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

# map the buffer to the vao index 0
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, None)

# allocate a vbo for colors on the GPU
vbo_colors = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vbo_colors)

# upload colors
colors = numpy.array([ 0, 0, 1, 0, 1, 1, 1, 1, 0], dtype=numpy.float32)
glBufferData(GL_ARRAY_BUFFER, colors.nbytes, colors, GL_STATIC_DRAW)

# map the bufer for colors in vao index 1
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)

vertex_shader = """
#version 330 core
layout(location=0) in vec2 vertex;
layout(location=1) in vec3 color;
out vec4 out_color;
void main() {
	gl_Position = vec4(vertex, 1, 1);
        out_color = vec4(color, 1);
}
"""

fragment_shader = """
#version 330 core
in vec4 out_color;
out vec4 color;
void main() {
	color = out_color;
}
"""

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

glUseProgram(program)

while window.is_opened:
    glClear(GL_COLOR_BUFFER_BIT)

    glDrawArrays(GL_TRIANGLES, 0, 3)
    window.update()
