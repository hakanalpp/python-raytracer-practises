from math import acos, asin, cos, sin
from multiprocessing import Value
import queue

from .task import Task

from ..shape import Shape
from ..math import Point3f, Vector3f, Ray, RGBA


class Worker:
    def __init__(self, objects, id):
        self.objects: list[Shape] = objects
        self.id = id
        self.stop = Value("b", False, lock=False)

    def stopp(self):
        self.stop.value = True

    def do_job(self, taskQueue, eventQueue):
        while taskQueue.qsize() != 0 and not self.stop.value:
            try:
                task = taskQueue.get_nowait()

                c = self.trace(task)
                task.r, task.g, task.b = c.l[:3]

                eventQueue.put((task.id, task.r, task.g, task.b))

            except queue.Empty:
                pass
            except Exception as e:
                raise e
        print(f"Worker - {self.id}: terminated!!")
        return True

    def trace(self, t):
        base_color, t, should_bounce, old_reflection = self.intersect(t, t.bounce != 0)
        while t.bounce != 0 and should_bounce:
            color, t, should_bounce, new_reflection = self.intersect(t, True)
            base_color = base_color + color.scalar_product(old_reflection)
            old_reflection = new_reflection
        return base_color

    def intersect(self, t, should_bounce: bool):
        selected = (
            -1,  # index
            float("inf"),  # distance
            RGBA(0, 0, 0),  # color
            None,  # ray
            None,  # normal
            None,  # hitPoint
        )  # (index, distance, color, ray, normal, hitPoint)

        for index, obj in enumerate(self.objects):
            ray = Ray(
                "Camera",
                Point3f(t.pointX, t.pointY, t.pointZ),
                Vector3f(t.dirX, t.dirY, t.dirZ),
                t.bounce,
            )
            bb_dist = obj.bounding_box.intersect(ray)
            if bb_dist == -1 or bb_dist > selected[1]:
                continue

            distance, color, normal, hitPoint = obj.intersect(ray)
            if distance != -1 and distance < selected[1]:
                selected = (index, distance, color, ray, normal, hitPoint)

        if selected[0] == -1:
            return RGBA(0, 0, 0), t, False, 0

        obj = self.objects[selected[0]]
        color = selected[2]

        new_c = obj.shader.calculate_light(self.objects, selected[5], selected[4])
        color = (color * new_c).scalar_product(obj.material.diffuse)

        if not obj.material.shouldBounce() or not should_bounce:
            return color, t, False, 0

        if obj.material.shouldReflect():
            t = self.calculate_reflection_ray(t, selected[4], selected[5])
            return color, t, True, obj.material.reflection

        t = self.calculate_refraction_ray(
            t, selected[4], selected[5], obj.material.refractive_index
        )
        return color, t, True, obj.material.refraction

    def calculate_reflection_ray(self, t, normal: "Vector3f", hitPoint: "Point3f"):
        rayDirection = Vector3f(
            t.dirX, t.dirY, t.dirZ
        ).normalize()  # this may need to be negated from time to time.
        nDotRay = normal.dot(rayDirection)
        newRay = rayDirection - (2 * nDotRay * normal)
        return Task(
            t.id,
            t.bounce - 1,
            hitPoint.x,
            hitPoint.y,
            hitPoint.z,
            newRay.x,
            newRay.y,
            newRay.z,
            t.x,
            t.y,
            t.r,
            t.g,
            t.b,
        )

    def calculate_refraction_ray(
        self, t, normal: "Vector3f", hitPoint: "Point3f", refractive_index
    ):
        rayDirection = Vector3f(t.dirX, t.dirY, t.dirZ).normalize()

        angle1 = acos(min(-1, max(normal.dot(rayDirection), 1)))
        angle2 = asin(sin(angle1) / refractive_index)
        newRay = (-normal).divide_scalar(cos(angle2))
        return Task(
            t.id,
            t.bounce - 1,
            hitPoint.x,
            hitPoint.y,
            hitPoint.z,
            newRay.x,
            newRay.y,
            newRay.z,
            t.x,
            t.y,
            t.r,
            t.g,
            t.b,
        )
