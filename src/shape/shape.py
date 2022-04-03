# CENG 488 Assignment#3 by
# Hakan Alp
# StudentId: 250201056
# March 2022

from abc import abstractmethod

from .bounding_box import AABB
from ..shading.shader import Shader

class Shape:
    def __init__(self, shader, type = "default"):
        self.shader: 'Shader' = shader
        self.bounding_box: 'AABB' = AABB()
        self.type = type

    @abstractmethod
    def intersect(self):
        return

    @abstractmethod
    def calculate_bounding_box(self):
        return