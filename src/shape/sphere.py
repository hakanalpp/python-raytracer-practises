# CENG 488 Assignment#2 by
# Hakan Alp
# StudentId: 250201056
# March 2022

from math import sqrt

from ..ray.ray import Ray
from ..math.vector import RGBA, Point3f
from .shape import Shape


class Sphere(Shape):
    def __init__(self, posX, posY, posZ, radius, r, g, b) -> "Sphere":
        super().__init__()
        self.position: "Point3f" = Point3f(posX, posY, posZ)
        self.radius: "float" = radius
        self.color: "RGBA" = RGBA(r, g, b, 255)

    def intersect(self, ray: 'Ray'):
        oc = ray.position - self.position
        a = ray.direction.dot(ray.direction)
        b = 2.0 * oc.dot(ray.direction)
        c = oc.dot(oc) - (self.radius* self.radius)
        sqr_disc = b*b - 4*a*c
        if sqr_disc < 0:
            return [-1, None]
        discriminant = sqrt(sqr_disc)
        if (a == 0): a = 0.0000000001 # prevent division by zero
        t0 = (-b + discriminant)/(2*a)
        t1 = (-b - discriminant)/(2*a) 
        return [min(t0,t1), self.color]