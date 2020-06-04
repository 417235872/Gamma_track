import pyqtgraph as pg
import numpy as np
import pyqtgraph.opengl as pl
from OpenGL.GL import *
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
        glColor4f(1, 1, 1, .3)
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

