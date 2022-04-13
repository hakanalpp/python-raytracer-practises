# CENG 488 Assignment#5 by
# Hakan Alp
# StudentId: 250201056
# April 2022

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


__all__ = ["AABB"]
