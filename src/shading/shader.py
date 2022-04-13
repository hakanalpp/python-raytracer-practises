from abc import abstractmethod
from math import cos, radians, sin

from ..math import Point3f, Ray, Vector3f

from ..light import Light


class Shader:
    def __init__(
        self, lights, ambient_ray_count, ambient_coefficient, ambient_occlusion: "bool"
    ) -> None:
        self.lights: "list[Light]" = lights
        self.ambient_ray_count = ambient_ray_count
        self.ambient_coefficient = ambient_coefficient
        self.ambient_occlusion = ambient_occlusion
        pass

    @abstractmethod
    def calculate_light(self):
        return

    def calculate_ambient_occlusion(self, objects, hitPoint: "Point3f"):
        if not self.ambient_occlusion or self.ambient_ray_count == 0:
            return self.ambient_coefficient, 0

        angle = 180 / self.ambient_ray_count
        count = 0
        for x in range(0, 180, int(angle)):
            for y in range(0, 180, int(angle)):
                xRad = radians(x)
                yRad = radians(y)
                count += self.send_ambient_ray(
                    objects,
                    Ray(
                        "Ambient",
                        hitPoint,
                        Vector3f(
                            cos(xRad),
                            sin(xRad) + sin(yRad),
                            cos(yRad),
                        ).normalize(),
                        0,
                    ),
                )

        return self.ambient_coefficient * (count / (self.ambient_ray_count**2)), self.ambient_ray_count**2

    def send_ambient_ray(self, objects, ray: "Ray"):
        dist = -1
        for obj in objects:
            dist = obj.intersect(ray)[0]
            if dist != float("inf") and dist > 0.00000001:
                return False
        return True
