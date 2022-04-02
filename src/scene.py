# CENG 488 Assignment#3 by
# Hakan Alp
# StudentId: 250201056
# March 2022

from .renderer.renderer import Renderer
from .camera import Camera
from .shape.shape import Shape


class Scene:
    def __init__(self, xRes, yRes, camera, objects, workerCount, samples, shader):
        self.resolution: "tuple(int, int)" = (xRes, yRes)
        self.workerCount = workerCount
        self.camera: "Camera" = camera
        self.objects: "list[Shape]" = objects
        self.samples = samples
        self.sentRayCount = 0

        ## Rest is generated.
        self.renderer: "Renderer" = Renderer(
            self.objects, self.camera, self.workerCount, xRes, yRes
        )
