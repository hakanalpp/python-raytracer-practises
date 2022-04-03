# CENG 488 Assignment#3 by
# Hakan Alp
# StudentId: 250201056
# March 2022

import sys

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from src.utils.initalizejson import initalize_scene

from src.window import MainWindow


if __name__ == "__main__":
	qApp = QApplication(sys.argv)
	scene = initalize_scene("scene.json")
	
	mainWindow = MainWindow(qApp, scene)
	mainWindow.setupUi()
	mainWindow.show()

	exit(qApp.exec_())
