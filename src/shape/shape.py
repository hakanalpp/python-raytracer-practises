# CENG 488 Assignment#4 by
# Hakan Alp
# StudentId: 250201056
# April 2022

from abc import abstractmethod

from .material import Material
from .bounding_box import AABB
from ..shading import Shader


class Shape:
    def __init__(self, material, shader, type="default"):
        self.material: "Material" = material
        self.shader: "Shader" = shader
        self.bounding_box: "AABB" = AABB()
        self.type = type

    @abstractmethod
    def intersect(self):
        return

    @abstractmethod
    def calculate_bounding_box(self):
        return
