from multiprocessing import Value
import queue


from ..math.vector import Point3f, Vector3f
from ..ray.ray import Ray


class Worker:
    def __init__(self, objects, id):
        self.objects = objects
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
        for obj in self.objects:
            temp_dist, temp_color, _, hitPoint = obj.intersect(
                Ray(
                    "Camera",
                    Point3f(t.pointX, t.pointY, t.pointZ),
                    Vector3f(t.dirX, t.dirY, t.dirZ),
                )
            )
            if temp_dist != -1 and temp_dist < dist:
                selected_index = index
                dist = temp_dist
                color = temp_color
            index += 1

        if selected_index != -1:
            new_c = self.objects[selected_index].shader.calculate_light(
                self.objects, hitPoint
            )
            color = [color.r * new_c.x, color.g * new_c.y, color.b * new_c.z]

        return color
