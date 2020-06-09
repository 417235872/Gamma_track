import pyqtgraph as pg
import numpy as np
import pyqtgraph.opengl as pl
from OpenGL.GL import *
#让网格的一个轴显示刻度
class myGLGridItem(pl.GLGridItem):
    def __init__(self,size=None, color=None, antialias=True, glOptions='translucent',parent : pl.GLViewWidget = None):
        super().__init__(size,color,antialias,glOptions)
        self._parent = parent
    def paint(self):
        self.setupGLState()

        if self.antialias:
            glEnable(GL_LINE_SMOOTH)
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)

        glBegin(GL_LINES)

        x, y, z = self.size()
        xs, ys, zs = self.spacing()
        xvals = np.arange(-x / 2., x / 2. + xs * 0.001, xs)
        yvals = np.arange(-y / 2., y / 2. + ys * 0.001, ys)
        glColor4f(0.2, 0.2, 0.2, .3)
        for x in xvals:
            glVertex3f(x, yvals[0], 0)
            glVertex3f(x, yvals[-1], 0)
        for y in yvals:
            glVertex3f(xvals[0], y, 0)
            glVertex3f(xvals[-1], y, 0)
        glEnd()
        glColor4f(0,0,0,1.)
        for x in xvals:
            self._parent.renderText(x,yvals[-1]+1,0,str(int(x)*10))


class myGLGridItem_YoZ(pl.GLGridItem):
    def __init__(self,size=None, color=None, antialias=True, glOptions='translucent',parent : pl.GLViewWidget = None):
        super().__init__(size,color,antialias,glOptions)
        self._parent = parent
        self.rotate(90,0,1,0)

    def paint(self):
        self.setupGLState()
        if self.antialias:
            glEnable(GL_LINE_SMOOTH)
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        glBegin(GL_LINES)
        x, y, z = self.size()
        xs, ys, zs = self.spacing()
        xvals = np.arange(-x, x + xs * 0.001, xs)
        yvals = np.arange(-y, y + ys * 0.001, ys)
        glColor4f(0.2, 0.2, 0.2, .3)
        for x in xvals:
            glVertex3f(x, yvals[0], 0)
            glVertex3f(x, yvals[-1]+0.1, 0)
        for y in yvals:
            glVertex3f(xvals[0], y, 0)
            glVertex3f(xvals[-1], y, 0)
        glEnd()
        glColor4f(0, 0, 0, 1.)
        for x in xvals:
            self._parent.renderText(x, yvals[-1] + 1, 0, str(-int(x)))

class myGLGridItem_XoZ(pl.GLGridItem):
    def __init__(self,size=None, color=None, antialias=True, glOptions='translucent',parent : pl.GLViewWidget = None):
        super().__init__(size,color,antialias,glOptions)
        self._parent = parent

    def paint(self):
        self.setupGLState()
        if self.antialias:
            glEnable(GL_LINE_SMOOTH)
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        glBegin(GL_LINES)
        x, y, z = self.size()
        xs, ys, zs = self.spacing()
        xvals = np.arange(-x, xs * 0.001, xs)
        yvals = np.arange(-y, y + ys * 0.001, ys)
        glColor4f(0.2, 0.2, 0.2, .3)
        for x in xvals:
            glVertex3f(x, yvals[0], 0)
            glVertex3f(x, yvals[-1], 0)
        for y in yvals:
            glVertex3f(xvals[0] + 0.1, y, 0)
            glVertex3f(xvals[-1], y, 0)
        glEnd()
        glColor4f(0, 0, 0, 1.)
        for y in yvals:
            self._parent.renderText(xvals[0] - 1, y, 0, str(int(y)))

class myGLGridItem_XoY(pl.GLGridItem):
    def __init__(self, size=None, color=None, antialias=True, glOptions='translucent', parent: pl.GLViewWidget = None):
        super().__init__(size, color, antialias, glOptions)
        self._parent = parent
        self.rotate(90,1,0,0)

    def paint(self):
        self.setupGLState()
        if self.antialias:
            glEnable(GL_LINE_SMOOTH)
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        glBegin(GL_LINES)
        x, y, z = self.size()
        xs, ys, zs = self.spacing()
        xvals = np.arange(-x, xs * 0.001, xs)
        yvals = np.arange(-y, y + ys * 0.001, ys)
        glColor4f(0.2, 0.2, 0.2, .3)
        for x in xvals:
            glVertex3f(x, yvals[0], 0)
            glVertex3f(x, yvals[-1] + 0.1, 0)
        for y in yvals:
            glVertex3f(xvals[0], y, 0)
            glVertex3f(xvals[-1], y, 0)
        glEnd()
        glColor4f(0, 0, 0, 1.)
        for x in xvals:
            self._parent.renderText(x, yvals[-1] + 1, 0, str(-int(x)))

from PyQt5.QtWidgets import QTreeWidgetItem
import xml.etree.ElementTree as ET

#存储了track分支信息的TreeItem
class trackItem(QTreeWidgetItem):
    def __init__(self,*__args):
        super(trackItem, self).__init__(*__args)
        self.trackElement = None

    def setElement(self,element : ET.Element):
        self.trackElement = element
        self.setText(0,self.trackElement.find("./name").text)