# CENG 488 Assignment#1 by
# Hakan Alp
# StudentId: 250201056
# March 2022

from ..math.vector import *


class Ray:
    def __init__(self, type, pos: 'Point3f', dir: 'Vector3f'):
        self.type = type
        self.position: 'Point3f' = pos
        self.direction: 'Vector3f' = dir
        