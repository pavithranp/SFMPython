from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtOpenGL import *
import math
from PyQt5 import QtCore, QtWidgets


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.widget = glWidget(self)
        # self.button = QPushButton('Test', self)
        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.widget)
        # mainLayout.addWidget(self.button)
        self.setLayout(mainLayout)


class glWidget(QGLWidget):

    def __init__(self, parent):
        QGLWidget.__init__(self, parent)
        self.setMinimumSize(640, 480)
        self.cubeVertices = (
            (0.5, 0.5, 0.5), (0.5, 0.5, -0.5), (0.5, -0.5, -0.5), (0.5, -0.5, 0.5), (-0.5, 0.5, 0.5),
            (-0.5, -0.5, -0.5),
            (-0.5, -0.5, 0.5), (-0.5, 0.5, -0.5))
        self.cubeEdges = (
            (0, 1), (0, 3), (0, 4), (1, 2), (1, 7), (2, 5), (2, 3), (3, 6), (4, 6), (4, 7), (5, 6), (5, 7))
        self.cubeQuads = ((0, 3, 6, 4), (2, 5, 6, 3), (1, 2, 5, 7), (1, 0, 4, 7), (7, 4, 6, 5), (2, 3, 0, 1))

    def wireCube(self):
        glBegin(GL_LINES)
        for cubeEdge in self.cubeEdges:
            for cubeVertex in cubeEdge:
                glVertex3fv(self.cubeVertices[cubeVertex])
        glEnd()

    def solidCube(self):
        glBegin(GL_QUADS)
        for cubeQuad in self.cubeQuads:
            for cubeVertex in cubeQuad:
                glVertex3fv(self.cubeVertices[cubeVertex])
        glEnd()

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(-0.0, 0.0, -2.0)
        # glRotatef(10,10,10,10)
        glColor3f(1.0, 1.5, 0.0)
        glPolygonMode(GL_FRONT, GL_FILL)

        self.wireCube()
        # self.solidCube()
        glFlush()

    def initializeGL(self):
        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, 1.33, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def resizeGL(self, width, height):
        self.width = width
        self.height = height
        self.aspect = width / height
        glViewport(0, 0, width, height)

    def mousePressEvent(self, event):

        print("pressed")
        btns = event.buttons()
        x = event.localPos().x()
        y = event.localPos().y()

        if btns & Qt.LeftButton:
            print("left")

        elif btns & (Qt.MidButton):
            print("middle")

        elif btns & (Qt.RightButton):
            print("right")

    def mouseReleaseEvent(self, event):
        # nothing to be done here.
        print("released")
        pass


if __name__ == '__main__':
    app = QApplication(['QT image'])
    window = MainWindow()
    window.show()
    app.exec_()
