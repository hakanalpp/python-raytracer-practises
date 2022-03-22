# CENG 488 Assignment#1 by
# Hakan Alp
# StudentId: 250201056
# March 2022

from math import pi, tan
from .math.vector import Point3f, Vector3f
from .ray.ray import Ray


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

    def getRay(self, x, y):  # newX and newY are between -1 and 1
        newX = (2 * ((x + 0.5) / self.res[0]) - 1) * self.aspectRatio * self.fov
        newY = (1 - 2 * ((y + 0.5) / self.res[1])) * self.fov

        k = self.midPoint + (newX * self.right) + (newY * (self.up))
        m: "Vector3f" = k - self.position

        return Ray("Camera", self.position, m.normalize())
