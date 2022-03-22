# CENG 488 Assignment#3 by
# Hakan Alp
# StudentId: 250201056
# March 2022

from .shading.shader import Shader
from .camera import Camera
from .math.vector import RGBA
from .ray.ray import Ray
from .shape.shape import Shape


class Scene:
    def __init__(self, xRes, yRes, camera, objects, samples, shader):
        self.resolution: "tuple(int, int)" = (xRes, yRes)
        self.camera: "Camera" = camera
        self.objects: "list[Shape]" = objects
        self.samples = samples
        self.sentRayCount = 0
        self.shader: "Shader" = shader

    def send_ray(self, x, y) -> "RGBA":
        self.sentRayCount += 1

        ray: "Ray" = self.camera.getRay(x, y)
        return self.trace(ray)

    def trace(self, ray: "Ray") -> "RGBA":
        dist = float("inf")
        color = RGBA(0, 0, 0, 0)
        index = 0
        selected_index = -1
        for obj in self.objects:
            temp_dist, temp_color, _, hitPoint = obj.intersect(ray)
            if temp_dist != -1 and temp_dist < dist:
                selected_index = index
                dist = temp_dist
                color = temp_color
            index += 1

        if selected_index != -1:
            new_c = self.shader.calculate_light(self.objects, hitPoint)
            self.sentRayCount += len(self.shader.lights)
            color = RGBA(color.r * new_c.x, color.g * new_c.y, color.b * new_c.z, 255)

        return color
