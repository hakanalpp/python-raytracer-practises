# CENG 488 Assignment#3 by
# Hakan Alp
# StudentId: 250201056
# March 2022

from abc import abstractmethod
from ..shading.shader import Shader

class Shape:
    def __init__(self, shader):
        self.shader: 'Shader' = shader

    @abstractmethod
    def intersect(self):
        return