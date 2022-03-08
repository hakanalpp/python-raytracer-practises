# CENG 488 Assignment#1 by
# Hakan Alp
# StudentId: 250201056
# March 2022

from ..math.vector import RGBA, Point3f
from .shape import Shape


class Sphere(Shape):
    def __init__(self, posX, posY, posZ, radius, r, g, b) -> "Sphere":
        super().__init__()
        self.position: "Point3f" = Point3f(posX, posY, posZ)
        self.radius: "float" = radius
        self.color: "RGBA" = RGBA(r, g, b, 255)
