# CENG 488 Assignment#3 by
# Hakan Alp
# StudentId: 250201056
# March 2022

import sys
from os.path import exists

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from src.utils.initalizejson import initalize_scene

from src.window import MainWindow


if __name__ == "__main__":
	qApp = QApplication(sys.argv)
	if len(sys.argv) == 1 or sys.argv[1][len(sys.argv[1])-5:] != ".json":
		print("Use like this: python assignment<X>.py scene_name.json")
		exit(0)
	if not exists(sys.argv[1]):
		print("This scene file does not exist.")
		exit(0)
	scene = initalize_scene(sys.argv[1])

	mainWindow = MainWindow(qApp, scene)
	mainWindow.setupUi()
	mainWindow.show()

	exit(qApp.exec_())
