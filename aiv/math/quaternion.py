import numbers
import math
from .vector3 import Vector3

class Quaternion(object):

    def __init__(self, x=0, y=0, z=0, w=1):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    @staticmethod
    def euler(x, y, z):
        q = Quaternion()
        qx = x * math.pi/180.0 * 0.5
        sinx = math.sin(qx)
        cosx = math.cos(qx)
        qy = y * math.pi/180.0 * 0.5
        siny = math.sin(qy)
        cosy = math.cos(qy)
        qz = z * math.pi/180.0 * 0.5
        sinz = math.sin(qz)
        cosz = math.cos(qz)
        q.x = cosx * cosy * cosz + sinx * siny * sinz
        q.y = cosx * cosy * sinz + sinx * siny * cosz
        q.z = cosx * siny * cosz + sinx * cosy * sinz
        q.w = sinx * cosy * cosz + cosx * siny * sinz
        return q

    def __mul__(self, other):
        if isinstance(other, Vector3):
            num = self.x * 2
            num2 = self.y * 2
            num3 = self.z * 2
            num4 = self.x * num
            num5 = self.y * num2
            num6 = self.z * num3
            num7 = self.x * num2
            num8 = self.x * num3
            num9 = self.y * num3
            num10 = self.w * num
            num11 = self.w * num2
            num12 = self.w * num3

            x = (1.0 - (num5 + num6)) * other.x + (num7 - num12) * other.y + (num8 + num11) * other.z
            y = (num7 + num12) * other.x + (1.0 - (num4 + num6)) * other.y + (num9 - num10) * other.z
            z = (num8 - num11) * other.x + (num9 + num10) * other.y + (1.0 - (num4 + num5)) * other.z

            return Vector3(x, y, z)
