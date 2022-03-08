# CENG 488 Assignment#1 by
# Hakan Alp
# StudentId: 250201056
# March 2022

import time

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from src.math.vector import RGBA

from src.scene import Scene


class PaintWidget(QWidget):
	def __init__(self, width, height, parent=None):
		super(PaintWidget, self).__init__(parent=parent)
		self.width = width
		self.height = height

		# setup an image buffer
		self.imgBuffer = QImage(self.width, self.height, QImage.Format_ARGB32_Premultiplied)
		self.imgBuffer.fill(QColor(0, 0, 0))


	def paintEvent(self, event):
		painter = QPainter(self)
		painter.setCompositionMode(QPainter.CompositionMode_Source)
		painter.drawImage(0, 0, self.imgBuffer)


	def sizeHint(self):
		return QSize(self.width, self.height)


class MainWindow(QMainWindow):
	def __init__(self, qApp, scene: 'Scene'):
		super(MainWindow, self).__init__()

		self.qApp = qApp
		self.width = scene.resolution[0]
		self.height = scene.resolution[1]
		self.gfxScene = QGraphicsScene()
		self.scene = scene

	def setupUi(self):
		if not self.objectName():
			self.setObjectName(u"lala")
		self.resize(self.width + 25, self.height + 25)
		self.setWindowTitle("Hakan Alp - Assignment 1")
		self.setStyleSheet("background-color:black;")
		self.setAutoFillBackground(True)

		# set centralWidget
		self.centralWidget = QWidget(self)
		self.centralWidget.setObjectName(u"CentralWidget")

		# create a layout to hold widgets
		self.horizontalLayout = QHBoxLayout(self.centralWidget)
		self.horizontalLayout.setObjectName(u"horizontalLayout")
		self.horizontalLayout.setContentsMargins(0, 0, 0, 0)

		# setup the gfxScene
		self.gfxScene.setItemIndexMethod(QGraphicsScene.NoIndex)

		# create a paint widget
		self.paintWidget = PaintWidget(self.width, self.height)
		self.paintWidget.setGeometry(QRect(0, 0, self.width, self.height))
		self.paintWidgetItem = self.gfxScene.addWidget(self.paintWidget)
		self.paintWidgetItem.setZValue(0)

		# create a QGraphicsView as the main widget
		self.gfxView = QGraphicsView(self.centralWidget)
		self.gfxView.setObjectName(u"GraphicsView")

		# assign our scene to view
		self.gfxView.setScene(self.gfxScene)
		self.gfxView.setGeometry(QRect(0, 0, self.width, self.height))

		# add widget to layout
		self.horizontalLayout.addWidget(self.gfxView)

		# set central widget
		self.setCentralWidget(self.centralWidget)

		# setup a status bar
		self.statusBar = QStatusBar(self)
		self.statusBar.setObjectName(u"StatusBar")
		self.statusBar.setStyleSheet("background-color:gray;")
		self.setStatusBar(self.statusBar)
		self.statusBar.showMessage("Ready...")


	def timerBuffer(self):
		now = time.time()
		self.statusBar.showMessage("Sending Camera rays...")
		imgBuffer: 'list[list[RGBA]]' = self.scene.render()
		self.statusBar.showMessage(f"{self.scene.sentRayCount} camera rays sent. Updating buffer...")

		# go through pixels
		for y in range(0, self.height):
			for x in range(0, self.width):
				self.paintWidget.imgBuffer.setPixelColor(x, y, imgBuffer[y][x].to_qcolor())

			self.updateBuffer()
			qApp.processEvents()

		diff = time.time() - now

		self.statusBar.showMessage(f'{self.scene.sentRayCount} camera rays sent in {diff:.2f} seconds...')
		self.scene.sentRayCount = 0

	def updateBuffer(self):
		self.paintWidget.update()



