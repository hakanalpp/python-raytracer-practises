from multiprocessing import Value
import queue

from ..shape.shape import Shape


from ..math import Point3f, Vector3f, Ray


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
                task.r, task.g, task.b = c[0], c[1], c[2]

                eventQueue.put((task.id, task.r, task.g, task.b))

            except queue.Empty:
                pass
            except Exception as e:
                print("Exception: ", e)
        print(f"Worker - {self.id}: terminated!!")
        return True

    def trace(self, t):
        dist = float("inf")
        color = [0, 0, 0, 0]
        index = 0
        selected_index = -1
        selected_normal = 0
        for obj in self.objects:
            r = Ray(
                "Camera",
                Point3f(t.pointX, t.pointY, t.pointZ),
                Vector3f(t.dirX, t.dirY, t.dirZ),
            )
            bb_dist = obj.bounding_box.intersect(r)
            if bb_dist == -1 or bb_dist > dist:
                continue

            temp_dist, temp_color, normal, hitPoint = obj.intersect(r)
            if temp_dist != -1 and temp_dist < dist:
                selected_normal = normal
                selected_index = index
                dist = temp_dist
                color = temp_color
            index += 1

        if selected_index != -1:
            new_c = self.objects[selected_index].shader.calculate_light(
                self.objects, hitPoint, selected_normal
            )
            color = [color.r * new_c.x, color.g * new_c.y, color.b * new_c.z]

        return color
