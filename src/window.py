# CENG 488 Assignment#6 by
# Hakan Alp
# StudentId: 250201056
# April 2022

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from .signal import Communicate
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
        self.imgBuffer.fill(QColor(0, 0, 0))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setCompositionMode(QPainter.CompositionMode_Source)
        painter.drawImage(0, 0, self.imgBuffer)

    def sizeHint(self):
        return QSize(self.width, self.height)


class MainWindow(QMainWindow):
    def __init__(self, qApp, scene: "Scene", name="string"):
        super().__init__()
        self.qApp: QApplication = qApp
        self.gfxScene = QGraphicsScene()

        self.scene = scene
        self.width = scene.resolution[0]
        self.height = scene.resolution[1]
        self.name = name

        self.signals = Communicate()
        self.signals.status_message.connect(self.statusbar_message)
        self.signals.paint_message.connect(self.paint_message)
        self.scene.signals = self.signals

        self.timer = QTimer()
        self.timer.setInterval(500)
        self.timer.timeout.connect(lambda *_: self.updateBuffer())
        self.timer.start()

    def showEvent(self, event):
        self.rendererThread.start()
        return super().showEvent(event)

    def closeEvent(self, event):
        self.scene.stopRender = True

        while not self.scene.processes_closed():
            pass

        self.paintWidget.imgBuffer.save(f"images/{self.name}")
        self.qApp.processEvents()
        self.rendererThread.quit()
        self.rendererThread.wait()
        super().closeEvent(event)

    @Slot(str)
    def statusbar_message(self, message):
        self.statusBar.showMessage(message)

    @Slot(int)
    def paint_message(self):
        self.updateBuffer()

    def setupUi(self):
        if not self.objectName():
            self.setObjectName("lala")
        self.resize(self.width + 25, self.height + 30)
        self.setWindowTitle("Hakan Alp - Assignment 7")
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
        self.scene.imgBuffer = self.paintWidget.imgBuffer

        self.rendererThread = QThread()
        self.rendererThread.started.connect(self.scene.render)
        self.scene.moveToThread(self.rendererThread)

    def updateBuffer(self):
        self.paintWidget.update()
