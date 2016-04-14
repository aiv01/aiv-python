import numpy
import math
from .vector3 import Vector3

class Matrix4(object):

    def __init__(self, m=None):
        self.m = m 
        if self.m is None:
            self.m = numpy.array([
                1, 0, 0, 0,
                0, 1, 0, 0,
                0, 0, 1, 0,
                0, 0, 0, 1
                ], numpy.float32)

    @staticmethod
    def translate(x, y, z):
        m = numpy.array([
            1, 0, 0, 0,
            0, 1, 0, 0,
            0, 0, 1, 0,
            x, y, z, 1
            ], dtype=numpy.float32)
        return Matrix4(m) 

    @staticmethod
    def scale(x, y, z):
        m = numpy.array([
            x, 0, 0, 0,
            0, y, 0, 0,
            0, 0, z, 0,
            0, 0, 0, 1
            ], dtype=numpy.float32)
        return Matrix4(m) 

    @staticmethod
    def look_at(eye_x, eye_y, eye_z, center_x, center_y, center_z, up_x, up_y, up_z):
        eye = Vector3(eye_x, eye_y, eye_z)
        center = Vector3(center_x, center_y, center_z)
        up = Vector3(up_x, up_y, up_z)

        fwd = (eye-center).normalized
        right = up.cross(fwd).normalized
        up = fwd.cross(right).normalized

        m = numpy.array([
            right.x, up.x, fwd.x, 0,
            right.y, up.y, fwd.y, 0,
            right.z, up.z, fwd.z, 0,
            0, 0, 0, 1
            ], numpy.float32)

        t = Matrix4.translate(-eye_x, -eye_y, -eye_z)
        return t * Matrix4(m)

    @staticmethod
    def rotate_y(deg):
        ysin = math.sin(math.radians(deg))
        ycos = math.cos(math.radians(deg))
        m = numpy.array([
            ycos, 0, -ysin, 0,
            0, 1, 0, 0,
            ysin, 0, ycos, 0,
            0, 0, 0, 1
            ], dtype=numpy.float32)
        return Matrix4(m) 

    @staticmethod
    def rotate_x(deg):
        xsin = math.sin(math.radians(deg))
        xcos = math.cos(math.radians(deg))
        m = numpy.array([
            1, 0, 0, 0,
            0, xcos, xsin, 0,
            0, -xsin, xcos, 0,
            0, 0, 0, 1
            ], dtype=numpy.float32)
        return Matrix4(m) 


    @staticmethod
    def rotate_z(deg):
        zsin = math.sin(math.radians(deg))
        zcos = math.cos(math.radians(deg))
        m = numpy.array([
            zcos, zsin, 0, 0,
            -zsin, zcos, 0, 0,
            0, 0, 1, 0,
            0, 0, 0, 1
            ], dtype=numpy.float32)
        return Matrix4(m) 
    
    @staticmethod
    def ortho(left, right, bottom, top, near, far):
        m = numpy.array([
            2.0/(right - left), 0, 0, 0,
            0, 2.0/(top - bottom), 0, 0,
            0, 0, -2.0/(far - near), 0,
            -((right + left)/(right - left)), -((top + bottom)/(top - bottom)), -((far + near)/(far - near)), 1
            ], dtype=numpy.float32)
        return Matrix4(m) 

    @staticmethod
    def perspective(fovy, aspect, near, far):
        top = near * math.tan(math.radians(fovy) * 0.5)
        bottom = -top
        right = top * aspect
        left = -right

        m = numpy.array([
                (2.0 * near) / (right - left), 0, 0, 0,
                0, (2.0 * near) / (top - bottom), 0, 0,
                (right + left) / (right - left), (top + bottom) / (top - bottom), -(far + near) / (far - near), -1,
                0, 0, -(2.0 * far * near) / (far - near), 0
            ], dtype=numpy.float32)
        return Matrix4(m) 
        
        

    def __mul__(self, other):
        if isinstance(other, Matrix4):
            m00 = self.m[0] * other.m[0] + self.m[1] * other.m[4] + self.m[2] * other.m[8] + self.m[3] * other.m[12]
            m01 = self.m[0] * other.m[1] + self.m[1] * other.m[5] + self.m[2] * other.m[9] + self.m[3] * other.m[13]
            m02 = self.m[0] * other.m[2] + self.m[1] * other.m[6] + self.m[2] * other.m[10] + self.m[3] * other.m[14]
            m03 = self.m[0] * other.m[3] + self.m[1] * other.m[7] + self.m[2] * other.m[11] + self.m[3] * other.m[15]

            m10 = self.m[4] * other.m[0] + self.m[5] * other.m[4] + self.m[6] * other.m[8] + self.m[7] * other.m[12]
            m11 = self.m[4] * other.m[1] + self.m[5] * other.m[5] + self.m[6] * other.m[9] + self.m[7] * other.m[13]
            m12 = self.m[4] * other.m[2] + self.m[5] * other.m[6] + self.m[6] * other.m[10] + self.m[7] * other.m[14]
            m13 = self.m[4] * other.m[3] + self.m[5] * other.m[7] + self.m[6] * other.m[11] + self.m[7] * other.m[15]

            m20 = self.m[8] * other.m[0] + self.m[9] * other.m[4] + self.m[10] * other.m[8] + self.m[11] * other.m[12]
            m21 = self.m[8] * other.m[1] + self.m[9] * other.m[5] + self.m[10] * other.m[9] + self.m[11] * other.m[13]
            m22 = self.m[8] * other.m[2] + self.m[9] * other.m[6] + self.m[10] * other.m[10] + self.m[11] * other.m[14]
            m23 = self.m[8] * other.m[3] + self.m[9] * other.m[7] + self.m[10] * other.m[11] + self.m[11] * other.m[15]

            m30 = self.m[12] * other.m[0] + self.m[13] * other.m[4] + self.m[14] * other.m[8] + self.m[15] * other.m[12]
            m31 = self.m[12] * other.m[1] + self.m[13] * other.m[5] + self.m[14] * other.m[9] + self.m[15] * other.m[13]
            m32 = self.m[12] * other.m[2] + self.m[13] * other.m[6] + self.m[14] * other.m[10] + self.m[15] * other.m[14]
            m33 = self.m[12] * other.m[3] + self.m[13] * other.m[7] + self.m[14] * other.m[11] + self.m[15] * other.m[15]


            m00 = self.m[0] * other.m[0] + self.m[4] * other.m[1] + self.m[8] * other.m[2] + self.m[12] * other.m[3]
            m01 = self.m[1] * other.m[0] + self.m[5] * other.m[1] + self.m[9] * other.m[2] + self.m[13] * other.m[3]
            m02 = self.m[2] * other.m[0] + self.m[6] * other.m[1] + self.m[10] * other.m[2] + self.m[14] * other.m[3]
            m03 = self.m[3] * other.m[0] + self.m[7] * other.m[1] + self.m[11] * other.m[2] + self.m[15] * other.m[3]

            m10 = self.m[0] * other.m[4] + self.m[4] * other.m[5] + self.m[8] * other.m[6] + self.m[12] * other.m[7]
            m11 = self.m[1] * other.m[4] + self.m[5] * other.m[5] + self.m[9] * other.m[6] + self.m[13] * other.m[7]
            m12 = self.m[2] * other.m[4] + self.m[6] * other.m[5] + self.m[10] * other.m[6] + self.m[14] * other.m[7]
            m13 = self.m[3] * other.m[4] + self.m[7] * other.m[5] + self.m[11] * other.m[6] + self.m[15] * other.m[7]

            m20 = self.m[0] * other.m[8] + self.m[4] * other.m[9] + self.m[8] * other.m[10] + self.m[12] * other.m[11]
            m21 = self.m[1] * other.m[8] + self.m[5] * other.m[9] + self.m[9] * other.m[10] + self.m[13] * other.m[11]
            m22 = self.m[2] * other.m[8] + self.m[6] * other.m[9] + self.m[10] * other.m[10] + self.m[14] * other.m[11]
            m23 = self.m[3] * other.m[8] + self.m[7] * other.m[9] + self.m[11] * other.m[10] + self.m[15] * other.m[11]

            m30 = self.m[0] * other.m[12] + self.m[4] * other.m[13] + self.m[8] * other.m[14] + self.m[12] * other.m[15]
            m31 = self.m[1] * other.m[12] + self.m[5] * other.m[13] + self.m[9] * other.m[14] + self.m[13] * other.m[15]
            m32 = self.m[2] * other.m[12] + self.m[6] * other.m[13] + self.m[10] * other.m[14] + self.m[14] * other.m[15]
            m33 = self.m[3] * other.m[12] + self.m[7] * other.m[13] + self.m[11] * other.m[14] + self.m[15] * other.m[15]

            m = numpy.array([
                m00, m01, m02, m03,
                m10, m11, m12, m13,
                m20, m21, m22, m23,
                m30, m31, m32, m33
                ], numpy.float32)

            return Matrix4(m) 

