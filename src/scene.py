# CENG 488 Assignment#1 by
# Hakan Alp
# StudentId: 250201056
# March 2022

from .camera import Camera
from .math.vector import RGBA
from .ray.ray import Ray
from .shape.shape import Shape


class Scene:
    def __init__(self, xRes, yRes, camera: 'Camera', objects: 'list[Shape]', samples) -> 'Scene':
        self.resolution: 'tuple(int, int)'= (xRes, yRes)
        self.camera: 'Camera' = camera
        self.objects: 'list[Shape]' = objects
        self.samples = samples
        self.sentRayCount = 0

    def send_ray(self, x,y) -> 'RGBA':
        self.sentRayCount += 1

        ray: 'Ray' = self.camera.getRay(x, y)
        return self.trace(ray)

    def trace(self, ray: 'Ray') -> 'RGBA':
        inter = float('inf')
        color = RGBA(0,0,0,0)
        for obj in self.objects:
            tempInt = obj.intersect(ray)
            if(tempInt != -1 and tempInt < inter):
                inter = tempInt
                color = obj.color
        return color
