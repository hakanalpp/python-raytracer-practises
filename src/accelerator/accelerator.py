# CENG 488 Assignment#6 by
# Hakan Alp
# StudentId: 250201056
# April 2022


from abc import ABC, abstractclassmethod
from typing import Union

from ..math import Point3f, Vector3f, Ray, RGBA
from ..shape import Shape


class Accelerator(ABC):
    def __init__(self, objects):
        self.objects: "list[Shape]" = objects

    def initialize(self):
        pass 

    @abstractclassmethod
    def intersect_ray(
        self, ray: "Ray", distance
    ) -> Union[
        Shape,  # shape
        float,  # distance
        RGBA,  # color
        Ray,  # ray
        Vector3f,  # normal
        Point3f,  # hitPoint
    ]:
        pass
