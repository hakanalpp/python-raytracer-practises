# CENG 488 Assignment#5 by
# Hakan Alp
# StudentId: 250201056
# April 2022

from .vector import *


class Ray:
    def __init__(self, type, pos: 'Point3f', dir: 'Vector3f', bounce: 'int'):
        self.type = type
        self.position: 'Point3f' = pos
        self.direction: 'Vector3f' = dir
        self.bounce: 'int' = bounce
        