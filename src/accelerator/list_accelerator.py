# CENG 488 Assignment#5 by
# Hakan Alp
# StudentId: 250201056
# April 2022


from ..math import RGBA, Ray
from .accelerator import Accelerator


class ListAccelerator(Accelerator):
    def __init__(self, objects):
        super().__init__(objects)

    def initalize(self):
        return

    def intersect_ray(self, ray: "Ray", distance = float("inf")):
        selected = (
            None,  # shape
            distance,  # distance
            RGBA(0, 0, 0),  # color
            None,  # ray
            None,  # normal
            None,  # hitPoint
        )  # (object, distance, color, ray, normal, hitPoint)

        for obj in self.objects:
            bb_dist = obj.bounding_box.intersect(ray)
            if bb_dist == -1 or bb_dist > selected[1]:
                continue

            distance, color, normal, hitPoint = obj.intersect(ray)
            if distance > 10e-3 and selected[1] - distance > 10e-3:
                selected = (obj, distance, color, ray, normal, hitPoint)

        return selected
