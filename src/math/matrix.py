# CENG 488 Assignment#5 by
# Hakan Alp
# StudentId: 250201056
# April 2022


import sys

import numpy

from .vector import HCoord
from math import sin, cos


# My matrix3d is in row major format which looks like this [[row1],[row2],[row3],[row4]]
class Matrix:
    def __init__(self, *args):
        if len(args) == 4:
            self.m = [i for i in args]
        elif len(args) == 1:
            self.m = args[0]
        elif len(args) == 0:
            self.m = [[1.0, 0, 0, 0], [0, 1.0, 0, 0], [0, 0, 1.0, 0], [0, 0, 0, 1.0]]
        else:
            print("There should be either 0, 1 or 4 args for creating Matrix.")
            sys.exit()

    def __str__(self) -> "str":
        res = ""
        for i in self.m:
            res += "[{:.2f} {:.2f} {:.2f} {:.2f}]\n".format(*i)
        return res

    @staticmethod
    def from_numpy(arr: "numpy.ndarray"):
        return Matrix(arr.tolist())

    def as_np(self):
        return numpy.array(self.m, dtype="float32")

    def invert(self) -> "Matrix":
        return numpy.array(self).invert()

    def __matmul__(self, m2) -> "Matrix":
        m1 = self.m
        m2 = m2.m
        temp = [[0 for i in range(4)] for j in range(4)]
        for i1 in range(len(m1)):
            for i2 in range(len(m2)):
                for i2_2 in range(len(m2)):
                    temp[i1][i2] += m1[i1][i2_2] * m2[i2_2][i2]
        return Matrix(temp)

    def transpose(self) -> "Matrix":
        matrix3d = self.m
        tempMatrix = []
        for j in range(4):
            row = []
            for i in range(4):
                row.append(matrix3d[i][j])
            tempMatrix.append(row)

        return Matrix(tempMatrix)

    def scalarMul(self, scalar) -> "Matrix":
        m = self.m
        tempMatrix = Matrix()
        tempM = tempMatrix.m
        for i1 in range(len(m)):
            for i2 in range(len(m[i1])):
                tempM[i1][i2] = m[i1][i2] * scalar
        return tempMatrix

    def __mul__(self, other):
        m1 = self.m
        v1 = other.asList()
        tempV = [0 for i in range(4)]
        for i in range(len(m1)):
            res = 0
            for j in range(len(v1)):
                res += v1[j] * m1[i][j]
            tempV[i] = res
        return HCoord(*tempV)

    @staticmethod
    def product3(m1, m2, m3) -> "Matrix":
        return m1 @ m2 @ m3

    @staticmethod
    def translation(x, y, z) -> "Matrix":
        return Matrix([[1, 0, 0, x], [0, 1, 0, y], [0, 0, 1, z], [0, 0, 0, 1]])

    @staticmethod
    def scale(sX, sY, sZ) -> "Matrix":
        return Matrix([[sX, 0, 0, 0], [0, sY, 0, 0], [0, 0, sZ, 0], [0, 0, 0, 1]])

    @staticmethod
    def rotateX(theta) -> "Matrix":
        return Matrix(
            [
                [1, 0, 0, 0],
                [0, cos(theta), -sin(theta), 0],
                [0, sin(theta), cos(theta), 0],
                [0, 0, 0, 1],
            ]
        )

    @staticmethod
    def rotateY(theta) -> "Matrix":
        return Matrix(
            [
                [cos(theta), 0, sin(theta), 0],
                [0, 1, 0, 0],
                [-sin(theta), 0, cos(theta), 0],
                [0, 0, 0, 1],
            ]
        )

    @staticmethod
    def rotateZ(theta) -> "Matrix":
        return Matrix(
            [
                [cos(theta), -sin(theta), 0, 0],
                [sin(theta), cos(theta), 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1],
            ]
        )
