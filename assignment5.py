# CENG 488 Assignment#5 by
# Hakan Alp
# StudentId: 250201056
# April 2022

from random import randint
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import sys
from os.path import exists


from src.utils import initalize_scene
from src.window import MainWindow


if __name__ == "__main__":
    qApp = QApplication(sys.argv)
    if len(sys.argv) == 1 or sys.argv[1][len(sys.argv[1])-5:] != ".json":
        print("Use like this: python assignment<X>.py scene_name.json <filename: optional>")
        exit(0)
    if not exists(sys.argv[1]):
        print("This scene file does not exist.")
        exit(0)
    scene = initalize_scene(sys.argv[1])

    name = f"{scene.resolution[0]}x{scene.resolution[1]}_{scene.workerCount}_{scene.bounceCount}"
    if len(sys.argv) == 3:
        name = sys.argv[2]
    if exists("images/ass5/" + name + ".png"):
        name = name + f"_{randint(1000,9999999)}"
    name += ".png"

    mainWindow = MainWindow(qApp, scene, name)
    mainWindow.setupUi()
    mainWindow.show()

    exit(qApp.exec_())
