# CENG 488 Assignment#3 by
# Hakan Alp
# StudentId: 250201056
# March 2022

import sys
import threading
import time

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from src.scene import Scene


class PaintWidget(QWidget):
    def __init__(self, width, height, parent=None):
        super(PaintWidget, self).__init__(parent=parent)
        self.width = width
        self.height = height

        # setup an image buffer
        self.imgBuffer = QImage(
            self.width, self.height, QImage.Format_ARGB32_Premultiplied
        )
        self.imgBuffer.fill(QColor(120, 0, 0))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setCompositionMode(QPainter.CompositionMode_Source)
        painter.drawImage(0, 0, self.imgBuffer)
        # print(self.imgBuffer.pixelColor(150,150))

    def sizeHint(self):
        return QSize(self.width, self.height)





class MainWindow(QMainWindow):
    def __init__(self, qApp, scene: "Scene"):
        super(MainWindow, self).__init__()

        self.qApp = qApp
        self.width = scene.resolution[0]
        self.height = scene.resolution[1]
        self.gfxScene = QGraphicsScene()
        self.scene = scene
        self.closed = False

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(lambda *_: self.xxx())
        self.timer.start()

    def xxx(self):
        print("tick")
        self.updateBuffer()


    def renderBuffer(self):
        now = time.time()
        self.statusBar.showMessage("Sending rays...")
        print("m", threading.get_ident() )

        self.rendererThread.start()
        # print(self.paintWidget.imgBuffer.pixelColor(150,150))
        # for y in range(0, self.height):
        #     for x in range(0, self.width):
        #         self.communicate.number.emit(Output(x,y,120,0,0))

        diff = time.time() - now
        self.statusBar.showMessage(
            f"{self.scene.sentRayCount} rays sent in {diff:.2f} seconds..."
        )

    def closeEvent(self, event):
        self.closed = True


    def setupUi(self):
        if not self.objectName():
            self.setObjectName("lala")
        self.resize(self.width + 25, self.height + 30)
        self.setWindowTitle("Hakan Alp - Assignment 3")
        self.setStyleSheet("background-color:black;")
        self.setAutoFillBackground(True)

        # set centralWidget
        self.centralWidget = QWidget(self)
        self.centralWidget.setObjectName("CentralWidget")

        # create a layout to hold widgets
        self.horizontalLayout = QHBoxLayout(self.centralWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
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
        self.gfxView.setObjectName("GraphicsView")

        # assign our scene to view
        self.gfxView.setScene(self.gfxScene)
        self.gfxView.setGeometry(QRect(0, 0, self.width, self.height))

        # add widget to layout
        self.horizontalLayout.addWidget(self.gfxView)

        # set central widget
        self.setCentralWidget(self.centralWidget)

        # setup a status bar
        self.statusBar = QStatusBar(self)
        self.statusBar.setObjectName("StatusBar")
        self.statusBar.setStyleSheet("background-color:gray;")
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Ready...")
        self.scene.renderer.imgBuffer = self.paintWidget.imgBuffer

        self.rendererThread = QThread()
        self.rendererThread.started.connect(self.scene.renderer.render)
        self.scene.renderer.moveToThread(self.rendererThread)

    def updateBuffer(self):
        self.paintWidget.update()
