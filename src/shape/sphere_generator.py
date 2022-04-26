# CENG 488 Assignment#6 by
# Hakan Alp
# StudentId: 250201056
# April 2022


from abc import ABC
from typing import TYPE_CHECKING, List

import numpy as np


from ..math import RGBA, Vector3f
from .sphere import Sphere
from ..shading import Shader
from .shape import AABB, Material


# Sphere Generator is implemented by Gokberk Akdeniz
class SphereGenerator:
    def __init__(self, min_radius: float, max_radius: float, boundary: "AABB", shader: "Shader", color: RGBA = None, material: Material = None, seed: int = None) -> None:
        self.boundary = boundary
        self.color = color
        self.shader = shader
        self.material = material
        self.rng = np.random.default_rng(seed)
        self.min_radius = min_radius
        self.max_radius = max_radius

    def generate(self) -> Sphere:
        radius = self.rng.uniform(self.min_radius, self.max_radius)
        center = Vector3f(
            self.rng.uniform(self.boundary.min.x+radius, self.boundary.max.x-radius),
            self.rng.uniform(self.boundary.min.y+radius, self.boundary.max.y-radius),
            self.rng.uniform(self.boundary.min.z+radius, self.boundary.max.z-radius),
        )
        color = RGBA(*self.rng.uniform(size=3)) if self.color is None else self.color

        sphere = Sphere(center.x, center.y, center.z, radius, color.r, color.g, color.b, self.material, self.shader)

        return sphere