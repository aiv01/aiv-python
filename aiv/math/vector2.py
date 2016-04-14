import numbers
import math

class Vector2(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y 

    def __repr__(self):
        return "Vector2(x={0}, y={1})".format(self.x, self.y)

    def __add__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x + other.x, self.y + other.y)
        if isinstance(other, numbers.Number):
            return Vector2(self.x + other, self.y + other)
        raise TypeError("only Vectors and numbers can be added")

    def __sub__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x - other.x, self.y - other.y)
        if isinstance(other, numbers.Number):
            return Vector2(self.x - other, self.y - other)
        raise TypeError("only Vectors and numbers can be subtracted")

    def __mul__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x * other.x, self.y * other.y)
        if isinstance(other, numbers.Number):
            return Vector2(self.x * other, self.y * other)
        raise TypeError("only Vectors and numbers can be multiplied")

    def __eq__(self, other):
        if isinstance(other, Vector2):
            if self.x != other.x:
                return False
            if self.y != other.y:
                return False
            return True
        raise TypeError("only Vectors can be compared")

    def __getitem__(self, index):
        if index == 0:
            return self.x
        if index == 1:
            return self.y
        raise IndexError("Vector2 has only 2 fields")

    @property
    def length(self):
        return math.sqrt( self.x * self.x + self.y * self.y)

    @property
    def normalized(self):
        l = self.length
        return Vector2(self.x / l, self.y / l)

    @property
    def tuple(self):
        return Vector2(self.x, self.y)
