# CENG 488 Assignment#3 by
# Hakan Alp
# StudentId: 250201056
# March 2022

from math import sqrt

from ..shading import Shader
from ..math import RGBA, Point3f, Ray, Vector3f
from .shape import Shape
from .material import Material


class Sphere(Shape):
    def __init__(
        self,
        posX,
        posY,
        posZ,
        radius,
        r,
        g,
        b,
        material: "Material",
        shader: "Shader",
        type: str = "default",
    ) -> "Sphere":
        super().__init__(material, shader, type)
        self.position: "Point3f" = Point3f(posX, posY, posZ)
        self.radius: "float" = radius
        self.color: "RGBA" = RGBA(r, g, b)
        self.calculate_bounding_box()

    def intersect(self, ray: "Ray"):  # TODO
        oc = ray.position - self.position
        a = ray.direction.dot(ray.direction)
        b = 2.0 * oc.dot(ray.direction)
        c = oc.dot(oc) - (self.radius * self.radius)
        sqr_disc = b * b - 4 * a * c
        if sqr_disc < 0:
            return [-1, None, None, None]
        discriminant = sqrt(sqr_disc)
        if a == 0:
            a = 10e-12  # prevent division by zero
        t0 = (-b + discriminant) / (2 * a)
        t1 = (-b - discriminant) / (2 * a)
        
        t_min = min(t0, t1)
        hitPoint = ray.position + (ray.direction.normalize() * t_min)
        normal = (hitPoint - self.position).normalize()
        return [t_min, self.color, normal, hitPoint]

    def calculate_bounding_box(self):
        area = self.radius * sqrt(2)

        self.bounding_box.min = Vector3f(-area, -area, -area) + self.position
        self.bounding_box.max = Vector3f(area, area, area) + self.position
