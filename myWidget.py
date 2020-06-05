import numpy as np
import pandas as pd
import pyqtgraph.opengl as pl
from OpenGL.GL import *
from myItem import myGLGridItem
#3D轨迹成像图
class myGLWidget_withGride(pl.GLViewWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.addCoordinatePlane()

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
        self.plot_line = pl.GLLinePlotItem(pos=pts, color=pg.glColor("#4D3454"), width=3, antialias=True)
        self.addItem(self.plot_line)

    def setDataScatter(self,pts):
        self.plot_scatter = pl.GLScatterPlotItem(pos=pts, color=pg.glColor("#E57012"), size=10)
        self.addItem(self.plot_scatter)

#2D轨迹投影图
import pyqtgraph as pg
class myPlotWidget_y(pg.PlotWidget):
    def __init__(self ,parent=None, background='w', **kargs):
        super(myPlotWidget_y, self).__init__(parent, background, **kargs)
        self.plotItem.showAxis('top')
        self.plotItem.showAxis('right')
        self.plotItem.getAxis('bottom').setStyle(showValues=False)
        self.plotItem.getAxis('right').setStyle(showValues = False)
        self.plotItem.showGrid(x=True,y=True)
        self.plotItem.setTitle("")

class myPlotWidget_x(pg.PlotWidget):
    def __init__(self,parent=None, background='w', **kargs):
        super(myPlotWidget_x, self).__init__(parent, background, **kargs)
        self.plotItem.showAxis('top')
        self.plotItem.showAxis('right')
        self.plotItem.getAxis('top').setStyle(showValues=False)
        self.plotItem.getAxis('right').setStyle(showValues = False)
        self.plotItem.showGrid(x=True,y=True)





from PyQt5.QtWidgets import *
import xml.etree.ElementTree as ET
from myItem import trackItem

class trackTree(QTreeWidget):
    def __init__(self,parent = None):
        super(trackTree, self).__init__(parent)

    #测试用函数，直接读取info.xml来0测试遍历track树
    def _loadTrackInfo(self,path):
        self.clear()
        self.RootTrack = ET.parse(path)
        self._branchInit(self,self.RootTrack.getroot())

    #载入track的info信息
    def setTrackInfo(self,RootTrack : ET.Element):
        self.clear()
        self.RootTrack = RootTrack
        self._branchInit(self,RootTrack)

    #递归遍历track树，设置节点
    def _branchInit(self,Parent,track : ET.Element):
        node = trackItem(Parent)
        node.setElement(track)
        branch = track.find('./branch').findall('track')
        if branch is None:
            return True
        else:
            for i in branch:
                self._branchInit(node, i)
            return True



if __name__ == '__main__':
    pass

