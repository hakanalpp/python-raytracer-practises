# CENG 488 Assignment#1 by
# Hakan Alp
# StudentId: 250201056
# March 2022


from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from math import acos, pi

from numpy import ndarray


class HCoord:
    def __init__(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def asList(self) -> "list[float]":
        return [self.x, self.y, self.z, self.w]

    def clone(self) -> "HCoord":
        return HCoord(self)

    def asVertex3f(self, mat: "ndarray"):
        v = mat.dot(self.asList())
        return [v[0], v[1], v[2]]

    def normalize(self) -> "HCoord":
        l = self.len()
        if l == 0:
            return HCoord(0, 0, 0, self.w)
        return HCoord(self.x / l, self.y / l, self.z / l, self.w / l)

    def sqrlen(self) -> "float":
        return self.x ** 2 + self.y ** 2 + self.z ** 2

    def len(self) -> "float":
        return (self.sqrlen()) ** 0.5

    def dot(self, v2) -> "float":
        return self.x * v2.x + self.y * v2.y + self.z * v2.z + self.w * v2.w

    def __str__(self) -> "str":
        return "[{:.2f}, {:.2f}, {:.2f}, {:.2f}]".format(self.x, self.y, self.z, self.w)

    def __add__(self, v2) -> "HCoord":
        return HCoord(self.x + v2.x, self.y + v2.y, self.z + v2.z, self.w + v2.w)

    def __sub__(self, v2) -> "HCoord":
        return self + (-v2)

    def __neg__(self) -> "HCoord":
        return HCoord(-self.x, -self.y, -self.z, -self.w)

    def __mul__(self, i2):
        if isinstance(i2, self.__class__):  # dot product
            return self.dot(i2)
        elif isinstance(i2, int) or isinstance(i2, float):  # scalar multiplication
            return HCoord(self.x * i2, self.y * i2, self.z * i2, self.w)
        else:  # Matrix * Vector
            return self * i2

    def __rmul__(self, i2) -> "HCoord":
        if isinstance(i2, self.__class__):  # dot product
            return self.dot(i2)
        elif isinstance(i2, int) or isinstance(i2, float):  # scalar multiplication
            return HCoord(self.x * i2, self.y * i2, self.z * i2, self.w * i2)

    def crossProduct(self, v2) -> "HCoord":
        return HCoord(
            self.y * v2.z - self.z * v2.y,
            self.z * v2.x - self.x * v2.z,
            self.x * v2.y - self.y * v2.x,
            self.w,
        )

    def projectionVec3(self, v2) -> "HCoord":
        return self.projectionVec3(self, v2)

    def angleBetweenVectors(self, v2) -> "float":
        return self.angleBetweenVectors(self, v2)

    def middle_point(self, v2) -> "HCoord ":
        return self.middle_point(self, v2)

    @staticmethod
    def projectionVec3(v1, v2) -> "HCoord":
        return v1 * ((v1 * v2) / (v1.len() ** 2))

    @staticmethod
    def angleBetweenVectors(v1, v2):
        angle = acos((v1 * v2) / (v1.len() * v2.len()))
        return (angle * 180) / pi

    @staticmethod
    def middle_point(v1, v2):
        return Point3f((v1.x + v2.x) / 2, (v1.y + v2.y) / 2, (v1.z + v2.z) / 2)

    @staticmethod
    def average_point(*args) -> "Point3f":
        x, y, z = 0, 0, 0
        index = 0
        for i in args:
            if i == None:
                continue
            x += i.x
            y += i.y
            z += i.z
            index += 1
        return Point3f(x / index, y / index, z / index)

    @staticmethod
    def get_normal_vector(p1: 'Point3f', p2: 'Point3f', p3: 'Point3f') -> 'Vector3f':
        m1 = p2-p1
        m2 = p3-p2
        return m1.normalize().crossProduct(m2.normalize())

    @staticmethod
    def get_length_between_points(p1, p2) -> 'float':
        return ((p2.x - p1.x)**2 + (p2.y-p1.y)**2 + (p2.z - p1.z)**2)**0.5
        

class Vector3f(HCoord):
    def __init__(self, x, y, z):
        HCoord.__init__(self, x, y, z, 0.0)


class Point3f(HCoord):
    def __init__(self, x, y, z):
        HCoord.__init__(self, x, y, z, 1.0)

    def __sub__(self, other):
        return Vector3f(self.x - other.x, self.y - other.y, self.z - other.z)

    def __add__(self, other):
        return Point3f(self.x + other.x, self.y + other.y, self.z + other.z)


class RGBA(HCoord):
    def __init__(self, r, g, b, a):
        HCoord.__init__(self, r, g, b, a)
        self.r = self.x
        self.g = self.y
        self.b = self.z
        self.a = self.w

    def asList(self, faceCount):
        return [self.r, self.g, self.b, self.a] * faceCount

    def to_qcolor(self):
        return QColor(self.r, self.g, self.b)
