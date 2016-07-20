from aiv.window import Window
from aiv.opengl import *
import numpy
from aiv.math.matrix4 import Matrix4
from aiv.input import KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN
from aiv.utils.objloader import ObjLoader
from aiv.utils.shaders import Shader

window = Window()

vertex_shader = """
#version 330 core

layout(location = 0) in vec3 vertex;

uniform mat4 world;
uniform mat4 camera;

void main() {
        gl_Position = camera * world * vec4(vertex, 1);
}
"""

fragment_shader = """
#version 330 core

out vec4 color;

void main() {
	color = vec4(1, 1, 1, 1);
}

"""

glClearColor(1, 0, 0, 1)
glEnable(GL_DEPTH_TEST)

vao = glGenVertexArrays(1)
glBindVertexArray(vao)

# parse the OBJ file
obj = ObjLoader('Stormtrooper.obj')

vbo_vertices = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vbo_vertices)
# upload and map obj file vertices
glBufferData(GL_ARRAY_BUFFER, obj.vertices.nbytes, obj.vertices, GL_STATIC_DRAW) 
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

program = Shader(vertex_shader, fragment_shader)
program.use()

world = program.get_uniform("world")
camera = program.get_uniform("camera")

yrot = 0
zoom = 4

while window.is_opened:

        if window.get_key(KEY_RIGHT):
            yrot += 60 * window.delta_time

        if window.get_key(KEY_LEFT):
            yrot -= 60 * window.delta_time

        if window.get_key(KEY_UP):
            zoom -= 0.5 * window.delta_time

        if window.get_key(KEY_DOWN):
            zoom += 0.5 * window.delta_time

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        mat = Matrix4.translate(0, -1, -2) * Matrix4.rotate_y(yrot) * Matrix4.scale(1, 1, 1)

        cam = Matrix4.perspective(60, window.aspect_ratio, 0.1, 100) * Matrix4.look_at(0, 1, zoom, 0, 0, 0, 0, 1, 0)

        glUniformMatrix4fv(world, 1, GL_FALSE, mat.m)
        glUniformMatrix4fv(camera, 1, GL_FALSE, cam.m)

        glDrawArrays(GL_TRIANGLES, 0, len(obj.vertices) // 3)
        window.update()
