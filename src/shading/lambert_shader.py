from ..math import HCoord, Point3f, Ray, Vector3f, RGBA
from src.shading.shader import Shader


class LambertShader(Shader):
    def __init__(
        self,
        accelerator,
        lights,
        ambient_ray_count,
        ambient_coefficient,
        ambient_occlusion,
        sampling_type,
    ) -> None:
        super().__init__(
            accelerator,
            lights,
            ambient_ray_count,
            ambient_coefficient,
            ambient_occlusion,
            sampling_type,
        )

    def calculate_light(self, hitPoint: "Point3f", normal: "Vector3f"):
        rayCount = 0
        ambient_rate, sentRay = self.calculate_ambient_occlusion(
            hitPoint, normal
        )
        rayCount += sentRay

        if len(self.lights) == 0:
            return RGBA(ambient_rate, ambient_rate, ambient_rate), rayCount

        ligs = []
        light_count = len(self.lights)
        for l in self.lights:
            distance = HCoord.get_length_between_points(hitPoint, l.position)
            ray = Ray("light", l.position, (hitPoint - l.position).normalize(), 0)

            selected = self.accelerator.intersect_ray(ray, distance)

            if selected[0] is None:
                l_factor = max(-normal.normalize().dot(ray.direction.normalize()), 0.0001)
                new_color = l.color.scalar_product(
                    l_factor * l.intensity
                )
                ligs.append(new_color)

        total_light = RGBA(ambient_rate, ambient_rate, ambient_rate)

        for i in range(0, len(ligs)):
            total_light += ligs[i]

        return total_light, rayCount + light_count
