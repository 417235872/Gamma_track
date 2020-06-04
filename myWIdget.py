import numpy as np
import pyqtgraph.opengl as pl
from OpenGL.GL import *
from myGLGridItem import myGLGridItem
class myGLWidget_withGride(pl.GLViewWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def paintGL(self, region=None, viewport=None, useItemNames=False):
        super().paintGL(region,viewport,useItemNames)


    def addCoordinatePlane(self):
        # add reference plane (x,y,z)
        gx = myGLGridItem(parent=self)
        gx.rotate(90, 0, 1, 0)
        #gx.translate(-10, 0, 0)
        # gx.setSize(x.max(),y.max(),z.max())
        self.addItem(gx)
        gy = myGLGridItem(parent=self)
        gy.rotate(90, 1, 0, 0)
        gy.translate(0, -10, 0)
        # gy.setSize(500,y=y.max(),z=500)
        self.addItem(gy)
        #gz = pl.GLGridItem()
        gz = myGLGridItem(parent=self)
        gz.translate(0, 0, -10)
        # gz.setSize(x.max(),y.max(),z.max())
        self.addItem(gz)


    def loadData(self,x,y,z,**kwargs):
        pts = np.vstack([x, y, z]).transpose()
        self.plot_line = None
        self.plot_scatter = None
        try:
            self.removeItem(self.plot_line)
        except ValueError as e :
            pass
        try:
            self.removeItem(self.plot_scatter)
        except ValueError as e:
            pass
        if kwargs.get('line',True):
            self.setDataLine(pts)
        if kwargs.get('scatter',True):
            self.setDataScatter(pts)

    def setDataLine(self,pts):
        self.plot_line = gl.GLLinePlotItem(pos=pts, color=pg.glColor("#4D3454"), width=3, antialias=True)
        self.addItem(self.plot_line)

    def setDataScatter(self,pts):
        self.plot_scatter = gl.GLScatterPlotItem(pos=pts, color=pg.glColor("#E57012"), size=10)
        self.addItem(self.plot_scatter)




if __name__ == '__main__':
    from pyqtgraph.Qt import QtCore, QtGui
    import pyqtgraph.opengl as gl
    import pyqtgraph as pg
    import numpy as np
    import pandas as pd
    import sys

    data = pd.read_excel("A:\工作\实验室\测斜软件\钻探所软件\钻探所软件\\导出实钻数据2017-02-17.xls")
    x = data['Unnamed: 5'][2:54].values/10
    y = data['Unnamed: 6'][2:54].values/10
    z = data['Unnamed: 7'][2:54].values/10

    app = QtGui.QApplication([])
    w = myGLWidget_withGride()
    w.addCoordinatePlane()
    w.setBackgroundColor(pg.mkColor("#B9B3A3"))
    w.opts['distance'] = 40
    w.show()
    w.setWindowTitle('pyqtgraph example: GLLinePlotItem')
    w.loadData(x,y,z,scatter = False)

    # # add line
    # pts = np.vstack([x, y, z]).transpose()
    # plt = gl.GLLinePlotItem(pos=pts, color=pg.glColor("#4D3454"), width=3, antialias=True)
    # w.addItem(plt)
    #
    # # add scatter
    # pos = gl.GLScatterPlotItem(pos=pts, color=pg.glColor("#E57012"), size=10)
    # w.addItem(pos)

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()