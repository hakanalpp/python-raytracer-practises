# CENG 488 Assignment#5 by
# Hakan Alp
# StudentId: 250201056
# April 2022

from multiprocessing import Process

from PySide2.QtCore import *
from PySide2.QtGui import *
from multiprocessing import Queue
import time
import queue

from .accelerator import Accelerator
from .light.light import Light
from .renderer.worker import Worker
from .camera import Camera
from .renderer.task import Task


class Scene(QObject):
    def __init__(self, xRes, yRes, camera, accelerator: 'Accelerator', lights, workerCount, bounceCount):
        super().__init__()
        self.resolution: "tuple(int, int)" = (xRes, yRes)
        self.camera: "Camera" = camera
        self.accelerator: "Accelerator" = accelerator
        self.lights: "list[Light]" = lights
        self.bounceCount = bounceCount
        self.sentRayCount = 0

        self.workerCount = workerCount
        self.eventCounter = 0
        self.workers: dict = {}
        self.stopRender = False
        self.threadKilled = False

        self.taskQueue = Queue()
        self.eventQueue = Queue()
        self.tasks = {}
        self.imgBuffer: QImage = None  # updated from window.py
        self.signals = None  # updated from window.py

    def render(self):
        now = time.time()
        self.signals.status_message.emit("Preparing Task Queue...")

        self.prepare_task_queue()
        self.signals.status_message.emit("Sending rays...")

        for id in range(self.workerCount):
            w = Worker(self.accelerator, id)
            p = Process(
                target=w.do_job,
                args=(self.taskQueue, self.eventQueue),
            )
            self.workers[id] = (p, w)
            p.start()

        while self.eventCounter < len(self.tasks) and not self.stopRender:
            try:
                tid, r, g, b, rayCount = self.eventQueue.get_nowait()
                self.eventCounter += 1
                self.sentRayCount += rayCount

                self.updateImgBuffer(tid, r, g, b)
                if self.eventCounter % (self.resolution[0] * 10) == 0:
                    self.signals.status_message.emit(
                        f"[{self.workerCount} Workers] {self.eventCounter + self.sentRayCount} rays sent in {time.time()-now:.2f} seconds"
                    )
            except queue.Empty:
                time.sleep(0.0001)
                pass
            except Exception as e:
                print("Scene Exception: ", e)

        for w in self.workers.values():
            w[1].stopp()

        for w in self.workers.values():  # Just in case.
            w[0].join()

        self.signals.status_message.emit(
            f"[{self.workerCount} Workers] {len(self.tasks) + self.sentRayCount} rays sent in {time.time()-now:.2f} seconds..."
        )
        self.threadKilled = True
        return self.threadKilled

    def processes_closed(self):
        res = True
        for w in self.workers.values():
            if w[0].is_alive():
                res = False
        return res and self.threadKilled

    def updateImgBuffer(self, tid, r, g, b):
        c = qRgb(r*255, g*255, b*255) # Find a way to get it between 0-1
        ev = self.tasks[tid]
        self.imgBuffer.setPixel(ev.x, ev.y, c)

    def prepare_task_queue(self):
        c = 0
        for y in range(0, self.resolution[0]):
            for x in range(0, self.resolution[1]):
                r = self.camera.calculateRay(x, y)
                t = Task(
                    c, self.bounceCount, r[0].x, r[0].y, r[0].z, r[1].x, r[1].y, r[1].z, x, y, 0, 0, 0
                )

                self.taskQueue.put(t)
                self.tasks[c] = t
                c += 1
