from ..math import HCoord, Point3f, Ray, Vector3f
from src.shading.shader import Shader


class LambertShader(Shader):
    def __init__(self, lights) -> None:
        super().__init__(lights)
        self.ambient_factor = 0.2

    def calculate_light(self, objects, hitPoint: "Point3f", normal: "Vector3f"):
        ligs = []
        light_count = len(self.lights)
        for l in self.lights:
            distance = HCoord.get_length_between_points(hitPoint, l.position)
            l_factor = 0.2
            ray = Ray("light", l.position, (hitPoint - l.position).normalize(), 0)
            flag = False
            for obj in objects:
                if obj.type == "shadowless":
                    continue
                bb_dist = obj.bounding_box.intersect(ray)
                if bb_dist == -1 or bb_dist > distance:
                    continue

                temp_dist, _, _, _ = obj.intersect(ray)
                if(temp_dist == distance):
                    continue
                if temp_dist != -1 and distance - temp_dist > 0.001:
                    ligs.append(l.color.scalar_product(self.ambient_factor * (l.intensity / light_count))) # TODO /light_count'u gamma functionla değiştir.
                    flag = True
                    break
            if flag:
                continue
            
            l_factor = max(-normal.normalize().dot(ray.direction.normalize()), 0.0001)
            ligs.append(l.color.scalar_product(l_factor * (l.intensity / light_count)))

        total_light = ligs[0]
        for i in range(1, len(ligs)):
            total_light += ligs[i]

        return total_light
