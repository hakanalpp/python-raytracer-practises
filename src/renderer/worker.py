from math import acos, asin, cos, sin
from multiprocessing import Value
import queue

from ..accelerator import Accelerator
from ..shape import Shape
from .task import Task
from ..math import Point3f, Vector3f, Ray, RGBA


class Worker:
    def __init__(self, accelerator, id):
        self.accelerator: 'Accelerator' = accelerator
        self.id = id
        self.stop = Value("b", False, lock=False)

    def stopp(self):
        self.stop.value = True

    def do_job(self, taskQueue, eventQueue):
        while taskQueue.qsize() != 0 and not self.stop.value:
            try:
                task = taskQueue.get_nowait()

                c, sentRay = self.trace(task)
                task.r, task.g, task.b = c.l[:3]

                eventQueue.put((task.id, task.r, task.g, task.b, sentRay))

            except queue.Empty:
                pass
            except Exception as e:
                raise e
        print(f"Worker - {self.id}: terminated!!")
        return True

    def trace(self, t):
        rayCount = 0
        base_color, t, should_bounce, old_reflection, sentRay = self.intersect(t, t.bounce != 0)
        rayCount += sentRay
        while t.bounce != 0 and should_bounce:
            color, t, should_bounce, new_reflection, sentRay = self.intersect(t, True)
            rayCount += sentRay
            base_color = base_color + color.scalar_product(old_reflection)
            old_reflection = new_reflection
        return base_color, rayCount

    def intersect(self, t, should_bounce: bool):
        rayCount = 1
        
        ray = Ray(
            "Camera",
            Point3f(t.pointX, t.pointY, t.pointZ),
            Vector3f(t.dirX, t.dirY, t.dirZ),
            t.bounce,
        )
        selected = self.accelerator.intersect_ray(ray)

        if selected[0] == None:
            return RGBA(0, 0, 0), t, False, 0, rayCount

        obj: Shape = selected[0]
        color = selected[2]

        new_c, sentRay = obj.shader.calculate_light(selected[5], selected[4])
        rayCount += sentRay
        color = (color * new_c).scalar_product(obj.material.diffuse)

        if not obj.material.shouldBounce() or not should_bounce:
            return color, t, False, 0, rayCount

        if obj.material.shouldReflect():
            t = self.calculate_reflection_ray(t, selected[4], selected[5])
            return color, t, True, obj.material.reflection, rayCount

        t = self.calculate_refraction_ray(
            t, selected[4], selected[5], obj.material.refractive_index
        )
        return color, t, True, obj.material.refraction, rayCount

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
