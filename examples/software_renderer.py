from aiv.draw import Window
from aiv.utils.objloader import ObjLoader
import math
from aiv.math.vector3 import Vector3
import numpy


window = Window(640, 480, "Aiv.Renderer")

window.zbuffer = numpy.array([0] * 640 * 480, dtype=numpy.float32)

obj = ObjLoader('examples/Stormtrooper.obj')

def clamp(f):
    return max(0, min(f, 1))

def clear_screen(win):
    for i in range(0, len(win.texture.pixels)):
        win.texture.pixels[i] = 0
    for i in range(0, len(win.zbuffer)):
        win.zbuffer[i] = float(999999)

def put_pixel(win, x, y, r, g, b, a=255):
    if x < 0 or x > win.width-1 or y < 0 or y > win.height-1:
        return
    pos = y * win.width * 4 + x * 4
    win.texture.pixels[pos] = r
    win.texture.pixels[pos+1] = g
    win.texture.pixels[pos+2] = b
    win.texture.pixels[pos+3] = a

class Vertex(object):
    def __init__(self, v, n, u):
        self.v = v
        self.n = n
        self.u = u

    def project(self, window, translate, fov):
        # distance from camera
        d = math.tan(math.radians(fov/2.0))
        v = self.v + translate
        self.projected = Vector3(0.0, 0.0, 0.0)
        self.projected.y = v.y / (d * v.z)
        self.projected.x = v.x / (window.aspect_ratio * d * v.z)
        self.projected.z = v.z

        self.projected.x = (self.projected.x * window.width / 2.0) + (window.width / 2.0)
        self.projected.y = -(self.projected.y * window.height / 2.0) + (window.height / 2.0)

        # compute lambert
        light_direction = (Vector3(0.0, 10.0, -3) - self.v).normalized
        self.lambert = max(light_direction.dot(self.n), 0)

class Triangle(object):
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def draw(self, window, fov):
        self.a.project(window, Vector3(0, -1.5, 5), fov) 
        self.b.project(window, Vector3(0, -1.5, 5), fov) 
        self.c.project(window, Vector3(0, -1.5, 5), fov) 

        p1 = self.a
        p2 = self.b
        p3 = self.c

        if p1.projected.y > p2.projected.y:
            tmp = p2
            p2 = p1
            p1 = tmp

        if p2.projected.y > p3.projected.y:
            tmp = p2
            p2 = p3
            p3 = tmp

        if p1.projected.y > p2.projected.y:
            tmp = p2
            p2 = p1
            p1 = tmp


        p1p2 = (p2.projected.x - p1.projected.x) / (p2.projected.y - p1.projected.y)
        p1p3 = (p3.projected.x - p1.projected.x) / (p3.projected.y - p1.projected.y)

        for y in range(int(p1.projected.y), int(p3.projected.y)+1):
            if p1p3 > p1p2:
               if y < p2.projected.y:
                   self.scanline(window, y, p1, p2, p1, p3)
               else:
                   self.scanline(window, y, p2, p3, p1, p3)
            else:
               if y < p2.projected.y:
                   self.scanline(window, y, p1, p3, p1, p2)
               else:
                   self.scanline(window, y, p1, p3, p2, p3)

    def scanline(self, window, y, left_top, left_bottom, right_top, right_bottom):
        if y < 0 or y > window.height-1:
            return
        gradient_left = 1
        gradient_right = 1
        if left_top.projected.y != left_bottom.projected.y:
            gradient_left = (y - left_top.projected.y) / (left_bottom.projected.y - left_top.projected.y)
        if right_top.projected.y != right_bottom.projected.y:
            gradient_right = (y - right_top.projected.y) / (right_bottom.projected.y - right_top.projected.y)

        left = left_top.projected.x + (left_bottom.projected.x - left_top.projected.x) * clamp(gradient_left)
        right = right_top.projected.x + (right_bottom.projected.x - right_top.projected.x) * clamp(gradient_right)

        zstart = left_top.projected.z + (left_bottom.projected.z - left_top.projected.z) * clamp(gradient_left)
        zend = right_top.projected.z + (right_bottom.projected.z - right_top.projected.z) * clamp(gradient_right)

        lstart = left_top.lambert + (left_bottom.lambert - left_top.lambert) * clamp(gradient_left)
        lend = right_top.lambert + (right_bottom.lambert - right_top.lambert) * clamp(gradient_right)

        for x in range(int(left), int(right)):
            if x < 0 or x > window.texture.width-1:
                continue
            zgradient = (x - left) / (right - left)
            z = zstart + (zend - zstart) * clamp(zgradient)
            lambert = lstart + (lend - lstart) * clamp(zgradient)
            zpos = y * 640 + x
            if window.zbuffer[zpos] > z:
                put_pixel(window, x, y, 100 * lambert * 2, 100 * lambert * 2, 100 * lambert * 2)
                window.zbuffer[zpos] = z

class Mesh(object):


    def __init__(self, obj):
        self.triangles = []
        for index in range(0, len(obj.vertices), 9):

            v = Vector3(obj.vertices[index], obj.vertices[index+1], obj.vertices[index+2]*-1)
            n = Vector3(obj.normals[index], obj.normals[index+1], obj.normals[index+2]*-1)
            a = Vertex(v, n, None)

            v = Vector3(obj.vertices[index+3], obj.vertices[index+4], obj.vertices[index+5]*-1)
            n = Vector3(obj.normals[index+3], obj.normals[index+4], obj.normals[index+5]*-1)
            b = Vertex(v, n, None)

            v = Vector3(obj.vertices[index+6], obj.vertices[index+7], obj.vertices[index+8]*-1)
            n = Vector3(obj.normals[index+6], obj.normals[index+7], obj.normals[index+8]*-1)
            c = Vertex(v, n, None)


            triangle = Triangle(a, b, c)
            self.triangles.append(triangle)
        print(len(self.triangles))
  

    def draw(self, window):
        for triangle in self.triangles:
            triangle.draw(window, 60.0)
        

stormtrooper = Mesh(obj)

while window.is_opened:
    clear_screen(window)
    stormtrooper.draw(window)
    window.blit()
