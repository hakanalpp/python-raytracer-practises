# CENG 488 Assignment#7 by
# Hakan Alp
# StudentId: 250201056
# May 2022

import functools
from ..math import Vector3f, Ray

# Bounding Box is implemented by Gokberk Akdeniz
class AABB:
    def __init__(self):
        self.min = Vector3f(0, 0, 0)
        self.max = Vector3f(0, 0, 0)

    def intersect(self, ray: Ray):
        tmin = (self.min.x - ray.position.x) / (ray.direction.x + 10e-12)
        tmax = (self.max.x - ray.position.x) / (ray.direction.x + 10e-12)

        if tmin > tmax:
            tmin, tmax = tmax, tmin

        tymin = (self.min.y - ray.position.y) / (ray.direction.y + 10e-12)
        tymax = (self.max.y - ray.position.y) / (ray.direction.y + 10e-12)

        if tymin > tymax:
            tymin, tymax = tymax, tymin

        if (tmin > tymax) or (tymin > tmax):
            return -1

        if tymin > tmin:
            tmin = tymin

        if tymax < tmax:
            tmax = tymax

        tzmin = (self.min.z - ray.position.z) / (ray.direction.z + 10e-12)
        tzmax = (self.max.z - ray.position.z) / (ray.direction.z + 10e-12)

        if tzmin > tzmax:
            tzmin, tzmax = tzmax, tzmin

        if (tmin > tzmax) or (tzmin > tmax):
            return -1

        if tzmin > tmin:
            tmin = tzmin

        if tzmax < tmax:
            tmax = tzmax

        return tmin

    def union(self, aabb2: 'AABB') -> 'AABB':
        result = AABB()

        result.min.x = min(self.min.x, aabb2.min.x)
        result.min.y = min(self.min.y, aabb2.min.y)
        result.min.z = min(self.min.z, aabb2.min.z)

        result.max.x = max(self.max.x, aabb2.max.x)
        result.max.y = max(self.max.y, aabb2.max.y)
        result.max.z = max(self.max.z, aabb2.max.z)

        return result

    
    @functools.cached_property
    def centeroid(self):
        return (self.max + self.min)* 0.5


__all__ = ["AABB"]
