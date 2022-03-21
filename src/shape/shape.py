# CENG 488 Assignment#1 by
# Hakan Alp
# StudentId: 250201056
# March 2022

from abc import abstractmethod


class Shape:
    def __init__(self):
        pass

    @abstractmethod
    def intersect(self) -> 'float':
        return