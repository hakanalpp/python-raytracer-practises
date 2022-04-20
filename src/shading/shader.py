# CENG 488 Assignment#5 by
# Hakan Alp
# StudentId: 250201056
# April 2022

from abc import abstractmethod
from math import cos, isqrt, pi, radians, sin, sqrt

from ..math import Point3f, Ray, Vector3f

from ..light import Light

import numpy as np


class Shader:
    def __init__(
        self,
        lights,
        ambient_ray_count,
        ambient_coefficient,
        ambient_occlusion: "bool",
        sampling_type: "str",
    ) -> None:
        self.lights: "list[Light]" = lights
        self.ambient_ray_count = ambient_ray_count
        self.ambient_coefficient = ambient_coefficient
        self.ambient_occlusion = ambient_occlusion
        self.rng = np.random.default_rng(53641345)
        self.sampling_type = sampling_type

    @abstractmethod
    def calculate_light(self):
        return

    def calculate_ambient_occlusion(self, objects, hitPoint: "Point3f", normal):
        if not self.ambient_occlusion or self.ambient_ray_count == 0:
            return self.ambient_coefficient, 0

        ray_count = self.ambient_ray_count

        count, ambient_ray_count = 0, 0
        if self.sampling_type == "cosine_weighted":
            count, ambient_ray_count = self.calculate_sampled_hemisphere(
                ray_count, objects, hitPoint, normal
            )
        elif self.sampling_type == "grid":
            count, ambient_ray_count = self.calculate_grid_hemisphere(
                ray_count, objects, hitPoint, normal
            )
        elif self.sampling_type == "grid_cosine_importance":
            count, ambient_ray_count = self.calculate_grid_cosine_importance(
                ray_count, objects, hitPoint, normal
            )

        return self.ambient_coefficient * (count / ambient_ray_count), ambient_ray_count

    def calculate_grid_cosine_importance(
        self, ray_count, objects, hitPoint: "Point3f", normal
    ):
        count1, ambient_ray_count1 = self.calculate_grid_hemisphere(
            int(ray_count / 3), objects, hitPoint, normal
        )
        count2, ambient_ray_count2 = self.calculate_sampled_hemisphere(
            int(2 * ray_count / 3), objects, hitPoint, normal
        )

        return count1 + count2, ambient_ray_count1 + ambient_ray_count2

    def calculate_sampled_hemisphere(
        self, ray_count, objects, hitPoint: "Point3f", normal
    ):
        Nt, Nb = self.createCoordinateSystem(normal)

        count = 0
        sucessful_ray_count = 0
        while sucessful_ray_count < ray_count:
            ray = self.cosineSampleHemisphere(normal, Nt, Nb)

            if ray.dot(normal) < 0:
                print("error!", ray.dot(normal))
                continue

            sucessful_ray_count += 1
            count += self.send_ambient_ray(
                objects,
                Ray(
                    "Ambient",
                    hitPoint,
                    ray,
                    0,
                ),
            )

        return count, ray_count

    def calculate_grid_hemisphere(
        self, ray_count, objects, hitPoint: "Point3f", normal
    ):
        ray_count = isqrt(int(ray_count))

        angle = 180 / ray_count
        count = 0
        for x in range(0, 180, int(angle)):
            for y in range(0, 180, int(angle)):
                xRad = radians(x)
                yRad = radians(y)
                v = Vector3f(
                    cos(xRad),
                    sin(xRad) + sin(yRad),
                    cos(yRad),
                ).normalize()

                count += self.send_ambient_ray(
                    objects,
                    Ray(
                        "Ambient",
                        hitPoint,
                        v,
                        0,
                    ),
                )
        return count, int(ray_count ** 2)

    def createCoordinateSystem(self, N: "Vector3f"):
        if abs(N.x) > abs(N.y):
            Nt = Vector3f(N.z, 0, -N.x) * (1 / sqrt(N.x ** 2 + N.z ** 2))
        else:
            Nt = Vector3f(0, -N.z, N.y) * (1 / sqrt(N.y ** 2 + N.z ** 2))
        Nb = N.crossProduct(Nt)
        return Nt, Nb

    def cosineSampleHemisphere(self, normal, Nt, Nb):
        r1 = self.rng.random()
        r2 = self.rng.random()
        sinTheta = sqrt(1 - r1 * r1)
        phi = 2 * pi * r2
        x = sinTheta * cos(phi)
        z = sinTheta * sin(phi)
        v = Vector3f(x, r1, z)

        return Vector3f(
            v.x * Nb.x + v.y * normal.x + v.z * Nt.x,
            v.x * Nb.y + v.y * normal.y + v.z * Nt.y,
            v.x * Nb.z + v.y * normal.z + v.z * Nt.z,
        )

    def send_ambient_ray(self, objects, ray: "Ray"):
        dist = -1
        for obj in objects:
            dist = obj.intersect(ray)[0]
            if dist != float("inf") and dist > 10e-10:
                return False
        return True
