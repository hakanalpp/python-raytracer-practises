from multiprocessing import Lock, Process, Queue, current_process
import threading
import time
import queue
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from ..math.vector import Point3f, Vector3f
from ..ray.ray import Ray
from ..shape.shape import Shape
from .task import  Task  # imported for using queue.Empty exception

class Renderer(QObject):
    def __init__(self, objects, camera, workerCount, width, height):
        super().__init__()
        self.workerCount = workerCount
        self.objects: "list[Shape]" = objects
        self.camera = camera
        self.width = width
        self.height = height

        self.taskQueue = Queue()
        self.tasks = {}
        self.taskCounter = 0
        self.eventQueue = Queue()
        self.processes = []

    def trace(self, t):
        dist = float("inf")
        color = [0, 0, 0, 0]
        # if t.x == 0:
        #     print(t.y, t.x, current_process().name)
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

    def do_job(self, lock, taskQueue, eventQueue):
        while True:
            try:
                task = taskQueue.get_nowait()

                c = self.trace(task)
                task.r, task.g, task.b = c[0], c[1], c[2]
                # print("dj:a", task.id, task.r, task.g, task.b)
                eventQueue.put((task.id, task.r, task.g, task.b))
                # time.sleep(0.01)
            except queue.Empty:
                pass
            except Exception as e:
                print("Exception: ", e)

        return True

    def prepare_task_queue(self):
        i = 0
        for y in range(0, self.height):
            for x in range(0, self.width):
                r = self.camera.calculateRay(x, y)
                t = Task(i, r[0].x, r[0].y, r[0].z, r[1].x, r[1].y, r[1].z, x, y, 0, 0, 0)

                self.taskQueue.put(t)
                self.tasks[i] = t
                i += 1

        print(i)

    def render(self):
        print("r", threading.get_ident() )

        self.prepare_task_queue()
        lock = Lock()
        # creating processes
        for _ in range(self.workerCount):
            p = Process(
                target=self.do_job,
                args=(lock, self.taskQueue, self.eventQueue),
            )
            self.processes.append(p)
            p.start()

        while self.taskCounter < len(self.tasks):
            try:
                tid, r, g, b = self.eventQueue.get_nowait()
                ev = self.tasks[tid]
                self.taskCounter += 1
                # print("r:a", tid, r, g, b)
                self.updateImgBuffer(tid, r, g, b)
            except queue.Empty:
                pass
            except Exception as e:
                print("Exception: ", e)
        print("!!!!!!!!!!!!!!!!!!!!!!!!")

        # todo stop all workers with worker.stop()

        # completing process
        # for p in self.processes:
        #     p.join()

        # # print the output
        # while not self.tasks_that_are_done.empty():
        #     print(self.tasks_that_are_done.get())
        print("lala end.")
        return True

    # @Slot(Output)
    def updateImgBuffer(self, tid, r, g, b):
        c = QColor(r, g, b)
        ev = self.tasks[tid]
        self.imgBuffer.setPixelColor(ev.x, ev.y, c)
