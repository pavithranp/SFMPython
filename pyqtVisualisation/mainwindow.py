from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtOpenGL import *
import numpy as np
from PIL import Image
import math
from PyQt5 import QtCore, QtWidgets
import pygame


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.widget = glWidget(self)
        # self.button = QPushButton('Test', self)
        self.widget.setFocusPolicy(Qt.StrongFocus)
        mainLayout = QHBoxLayout()

        mainLayout.addWidget(self.widget)
        # mainLayout.addWidget(self.button)
        self.setLayout(mainLayout)


class glWidget(QGLWidget):

    def __init__(self, parent):
        self.zoom = -5
        self.camera=[0,0]

        self.action_keymap = {
            'a': [0,-1],
            'd': [0,1],
            'w': [1,0],
            's': [-1,0],
        }

        self.picture = "ozil.png"
        QGLWidget.__init__(self, parent)
        self.setMinimumSize(640, 480)
        main_camera_translation = np.zeros(3)
        main_camera_rotation = np.zeros(3)

        self.cubeVertices = (
            (0.5, 0.5, 0.5), (0.5, 0.5, -0.5), (0.5, -0.5, -0.5), (0.5, -0.5, 0.5), (-0.5, 0.5, 0.5),
            (-0.5, -0.5, -0.5),
            (-0.5, -0.5, 0.5), (-0.5, 0.5, -0.5))
        self.cubeEdges = (
            (0, 1), (0, 3), (0, 4), (1, 2), (1, 7), (2, 5), (2, 3), (3, 6), (4, 6), (4, 7), (5, 6), (5, 7))
        self.cubeQuads = ((0, 3, 6, 4), (2, 5, 6, 3), (1, 2, 5, 7), (1, 0, 4, 7), (7, 4, 6, 5), (2, 3, 0, 1))


    def image_load(self,lox,loy,loz,picture,rotate):
        self.read_texture(picture)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glRotated(rotate, 0.0, 1.0, 0.0)
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(-1.0+lox, -1.0+loy, 1.0+loz)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(1.0+lox, -1.0+loy, 1.0+loz)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(1.0+lox, 1.0+loy, 1.0+loz)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(-1.0+lox, 1.0+loy, 1.0+loz)
        glEnd()
        glPopMatrix()

    def keyPressEvent(self, event):
        print("pressed",event.text())
        # gluLookAt(2,1,1,0,0,0,0,1,0)
        self.camera = self.action_keymap.get(event.text())
        glRotate(self.camera[0],1,0,0)
        glRotate(self.camera[1],0,1,0)
        self.update()

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.image_load(-1,0,0,"../reconstruction/mon_r.jpg",-20)
        self.image_load(1, 0, 0,"../reconstruction/mon_l.jpg",20)
        glFlush()

#   def drawAxes(self):


    def initializeGL(self):
        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, 1.33, 0.1, 100.0)

        glTranslatef(0.0, 0.0, -10)
        glMatrixMode(GL_MODELVIEW)

    def resizeGL(self, width, height):
        self.width = width
        self.height = height
        self.aspect = width / height
        glViewport(0, 0, width, height)

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        if delta > 0:
            glTranslate(0,0,1)
        else:
            glTranslate(0,0,-1)
        self.update()

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

    def read_texture(self,picture):
        textureSurface = pygame.image.load(picture)
        textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
        width = textureSurface.get_width()
        height = textureSurface.get_height()

        glEnable(GL_TEXTURE_2D)
        texid = glGenTextures(1)


        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height,
                     0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)

        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        return texid


if __name__ == '__main__':
    app = QApplication(['QT image'])
    window = MainWindow()
    window.show()
    app.exec_()
