from aiv.window import Window
from aiv.opengl import *

# import numpy for advanced array support
import numpy

window = Window()

# set the color to use when clearing the color buffer
glClearColor(1, 0, 0, 1)

# build and bind a vertex array
vao = glGenVertexArrays(1)
glBindVertexArray(vao)

# generate a buffer (will be mapped to the currently bound vertexarray)
vbo = glGenBuffers(1)
# bind it
glBindBuffer(GL_ARRAY_BUFFER, vbo)

# build an array of vertices for a triangle (2d)
vertices = numpy.array([ 0, 1, -1, -1, 1, -1], dtype=numpy.float32)
# upload data to the GPU buffer (the vbo)
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

# map the current buffer (vbo) to the vertex array (index 0)
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, None)

# a simple vertex shader
vertex_shader = """
#version 330 core
layout(location=0) in vec2 vertex;
out vec4 out_color;
void main() {
	gl_Position = vec4(vertex + vec2(0.2, 0), 1, 1);
	out_color = vec4(vertex, 0, 1);
}
"""

# the fragment shader for choosing the pixel color
fragment_shader = """
#version 330 core
out vec4 color;
in vec4 out_color;
void main() {
	color = out_color;
}
"""

# compile and link the two shaders into a "program"
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

# "bind" the program
glUseProgram(program)

# finally the game loop
while window.is_opened:
    glClear(GL_COLOR_BUFFER_BIT)

    # the draw call
    glDrawArrays(GL_TRIANGLES, 0, 3)

    # show the color buffer
    window.update()
