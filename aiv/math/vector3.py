import numbers
import math

class Vector3(object):

    def __init__(self, x, y, z):
        self.x = x
        self.y = y 
        self.z = z

    def __repr__(self):
        return "Vector3(x={0}, y={1}, z={2})".format(self.x, self.y, self.z)

    def __add__(self, other):
        if isinstance(other, Vector3):
            return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
        if isinstance(other, numbers.Number):
            return Vector3(self.x + other, self.y + other, self.z + other)
        raise TypeError("only Vectors and numbers can be added")

    def __sub__(self, other):
        if isinstance(other, Vector3):
            return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
        if isinstance(other, numbers.Number):
            return Vector3(self.x - other, self.y - other, self.z - other)
        raise TypeError("only Vectors and numbers can be subtracted")

    def __mul__(self, other):
        if isinstance(other, Vector3):
            return Vector3(self.x * other.x, self.y * other.y, self.z * other.z)
        if isinstance(other, numbers.Number):
            return Vector3(self.x * other, self.y * other, self.z * other)
        raise TypeError("only Vectors and numbers can be multiplied")

    def __truediv__(self, other):
        if isinstance(other, Vector3):
            return Vector3(self.x / other.x, self.y / other.y, self.z / other.z)
        if isinstance(other, numbers.Number):
            return Vector3(self.x / other, self.y / other, self.z / other)
        raise TypeError("only Vectors and numbers can be divided")

    def __eq__(self, other):
        if isinstance(other, Vector3):
            if self.x != other.x:
                return False
            if self.y != other.y:
                return False
            if self.z != other.z:
                return False
            return True
        raise TypeError("only Vectors can be compared")

    def __getitem__(self, index):
        if index == 0:
            return self.x
        if index == 1:
            return self.y
        if index == 2:
            return self.z
        raise IndexError("Vector3 has only 3 fields")

    @property
    def length(self):
        return math.sqrt( self.x * self.x + self.y * self.y + self.z * self.z)

    @property
    def normalized(self):
        l = self.length
        return Vector3(self.x / l, self.y / l, self.z / l)

    def cross(self, other):
        x = self.y * other.z - self.z * other.y
        y = self.z * other.x - self.x * other.z
        z = self.x * other.y - self.y * other.x
        return Vector3(x, y, z)

    @property
    def tuple(self):
        return (self.x, self.y, self.z)
