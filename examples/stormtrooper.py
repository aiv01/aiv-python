from aiv.window import Window
from aiv.opengl import *
import numpy
from aiv.math.matrix4 import Matrix4
from aiv.input import KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN
from aiv.utils.objloader import ObjLoader

window = Window()

vertex_shader = """
    #version 330 core
    layout(location = 0) in vec3 vertex;
    layout(location = 1) in vec3 normal;

    uniform mat4 world;
    uniform mat4 camera;

    out vec4 color;
    out float lambert;

    void main() {
	vec4 vertex_world = world * vec4(vertex, 1);
        gl_Position = camera * vertex_world;
        vec3 light = vec3(0, 10, 0);
        vec3 light_direction = normalize(light - vec3(vertex_world)); 
        vec4 normal_world = world * vec4(normal, 0);

	lambert = max(dot(light_direction, normal_world.xyz), 0);
    }
    """

fragment_shader = """
    #version 330 core
    in float lambert;
    out vec4 color;
    void main() {
        color = vec4(1, 1, 1, 1) * lambert + vec4(0.1, 0.1, 0.1, 1);
    }
    """

glClearColor(0, 1, 1, 1)
glEnable(GL_DEPTH_TEST)

vao = glGenVertexArrays(1)
glBindVertexArray(vao)

obj = ObjLoader('examples/Stormtrooper.obj')

vbo_vertices = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vbo_vertices)
glBufferData(GL_ARRAY_BUFFER, obj.vertices.nbytes, obj.vertices, GL_STATIC_DRAW) 
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

vbo_normals = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vbo_normals)
glBufferData(GL_ARRAY_BUFFER, obj.normals.nbytes, obj.normals, GL_STATIC_DRAW) 
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)


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

        #mat = Matrix4.scale(1, 1, 1) * Matrix4.rotate_y(yrot) * Matrix4.rotate_x(xrot) * Matrix4.translate(0, 0, -5)
        mat = Matrix4.translate(0, -1, -2) * Matrix4.rotate_y(yrot) * Matrix4.scale(1, 1, 1)

        cam = Matrix4.perspective(60, 800.0/600.0, 0.1, 100) * Matrix4.look_at(0, 1, zoom, 0, 0, 0, 0, 1, 0)

        glUniformMatrix4fv(world, 1, GL_FALSE, mat.m)
        glUniformMatrix4fv(camera, 1, GL_FALSE, cam.m)

        glDrawArrays(GL_TRIANGLES, 0, len(obj.vertices) // 3)
        window.update()
