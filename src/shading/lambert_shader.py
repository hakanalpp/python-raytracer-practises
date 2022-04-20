from ..math import HCoord, Point3f, Ray, Vector3f, RGBA
from src.shading.shader import Shader


class LambertShader(Shader):
    def __init__(
        self,
        lights,
        ambient_ray_count,
        ambient_coefficient,
        ambient_occlusion,
        sampling_type,
    ) -> None:
        super().__init__(
            lights,
            ambient_ray_count,
            ambient_coefficient,
            ambient_occlusion,
            sampling_type,
        )

    def calculate_light(self, objects, hitPoint: "Point3f", normal: "Vector3f"):
        rayCount = 0
        ambient_rate, sentRay = self.calculate_ambient_occlusion(
            objects, hitPoint, normal
        )  # Calculate ambient occlusion as first step.
        rayCount += sentRay

        if len(self.lights) == 0:
            return RGBA(ambient_rate, ambient_rate, ambient_rate), rayCount

        ligs = []
        light_count = len(self.lights)
        for l in self.lights:
            distance = HCoord.get_length_between_points(hitPoint, l.position)
            ray = Ray("light", l.position, (hitPoint - l.position).normalize(), 0)

            flag = False
            for obj in objects:
                if obj.type == "shadowless":
                    continue
                bb_dist = obj.bounding_box.intersect(ray)
                if bb_dist == -1 or bb_dist > distance:
                    continue

                temp_dist, _, _, _ = obj.intersect(ray)
                if temp_dist == distance:
                    continue

                if temp_dist != -1 and distance - temp_dist > 0.001:
                    ligs.append(
                        l.color.scalar_product(
                            ambient_rate * (l.intensity / light_count)
                        )
                    )  # TODO /light_count'u gamma functionla değiştir.
                    flag = True
                    break
            if flag:
                continue

            l_factor = max(-normal.normalize().dot(ray.direction.normalize()), 0.0001)
            new_color = l.color.scalar_product(
                l_factor * (l.intensity / light_count)
            ) + RGBA(ambient_rate, ambient_rate, ambient_rate)
            ligs.append(new_color)

        total_light = ligs[0]
        for i in range(1, len(ligs)):
            total_light += ligs[i]

        return total_light, rayCount + light_count
