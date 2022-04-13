# CENG 488 Assignment#5 by
# Hakan Alp
# StudentId: 250201056
# April 2022

from math import pi, tan
from .math import Point3f, Vector3f, Ray


class Camera:
    def __init__(
        self,
        posX,
        posY,
        posZ,
        fov,
        focalLength,
        dirX,
        dirY,
        dirZ,
        upX,
        upY,
        upZ,
        resX,
        resY,
    ) -> "Camera":
        if resY > resX:
            print("y resolution can not be smaller than x!")
            exit()
        self.position: "Point3f" = Point3f(posX, posY, posZ)
        self.fov: "float" = tan(fov / 2 * pi / 180) * focalLength
        self.focalLength: "float" = focalLength
        self.direction: "Vector3f" = Vector3f(dirX, dirY, dirZ)
        self.up: "Vector3f" = Vector3f(upX, upY, upZ)
        self.res = (resX, resY)

        # Calculated after above things
        self.right = self.direction.crossProduct(self.up)
        self.midPoint = self.position + self.direction * self.focalLength
        self.aspectRatio = resX / resY

    def calculateRay(self, x, y):
        newX = (2 * ((x + 0.5) / self.res[0]) - 1) * self.aspectRatio * self.fov
        newY = (1 - 2 * ((y + 0.5) / self.res[1])) * self.fov

        k = self.midPoint + (newX * self.right) + (newY * (self.up))
        m: "Vector3f" = k - self.position

        return (self.position, m.normalize())

    # def getRay(self, x, y):  # not used anymore
    #     r = self.calculateRay(x, y)
    #     return Ray("Camera", r[0], r[1], 0)