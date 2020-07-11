import numpy as np
import pandas as pd
import pyqtgraph.opengl as pl
from OpenGL.GL import *
from myItem import myGLGridItem
#3D轨迹成像图
class myGLWidget_withGride(pl.GLViewWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        #self.addCoordinatePlane()
        self.setBackgroundColor('w')

    def paintGL(self, region=None, viewport=None, useItemNames=False):
        super().paintGL(region,viewport,useItemNames)


    def addCoordinatePlane(self):
        # add reference plane (x,y,z)
        gx = myGLGridItem(parent=self)
        gx.rotate(90, 0, 1, 0)
        #gx.translate(-10, 0, 0)
        # gx.setSize(x.max(),y.max(),z.max())

        self.addItem(gx)
        gx.setSize(10, 10, 10)
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
class myPlotWidget_x(pg.PlotWidget):
    def __init__(self,parent=None, background='w', **kargs):
        super(myPlotWidget_x, self).__init__(parent, background, **kargs)
        self.plotItem.showAxis('top')
        self.plotItem.showAxis('right')
        self.plotItem.getAxis('top').setStyle(showValues=False)
        self.plotItem.getAxis('right').setStyle(showValues = False)
        self.plotItem.showGrid(x=True,y=True)
        self.plotItem.setLabel(axis='left',text='上下位移')
        self.plotItem.setLabel(axis='bottom', text='水平位移')


class myPlotWidget_y(pg.PlotWidget):
    def __init__(self ,parent=None, background='w', **kargs):
        super(myPlotWidget_y, self).__init__(parent, background, **kargs)
        self.plotItem.showAxis('top')
        self.plotItem.showAxis('right')
        self.plotItem.getAxis('bottom').setStyle(showValues=False)
        self.plotItem.getAxis('left').setStyle(showValues = False)
        self.plotItem.showGrid(x=True,y=True)
        # self.plotItem.setTitle("")
        self.plotItem.setLabel(axis='right', text='水平位移')
        self.plotItem.setLabel(axis='top', text='左右位移')


class myPlotWidget_z(pg.PlotWidget):
    def __init__(self,parent=None, background='w', **kargs):
        super(myPlotWidget_z, self).__init__(parent, background, **kargs)
        self.plotItem.showAxis('top')
        self.plotItem.showAxis('right')
        self.plotItem.getAxis('top').setStyle(showValues=False)
        self.plotItem.getAxis('left').setStyle(showValues = False)
        self.plotItem.showGrid(x=True,y=True)
        self.plotItem.setLabel(axis='right', text='上下位移')
        self.plotItem.setLabel(axis='bottom', text='左右位移')




from PyQt5.QtWidgets import *
import xml.etree.ElementTree as ET
from myItem import trackItem
#轨迹树控件
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



#实现文件树
from PyQt5.QtWidgets import QTreeView,QFileSystemModel
class NewTreeView(QTreeView):
    def __init__(self,parent= None,workPath = ''):
        super().__init__()
        self.myModel = QFileSystemModel()
        self.setTree(self.myModel)
        self.setWorkPath(workPath)
    #设置树控件大小等
    def setTree(self,model):
        self.setModel(self.myModel)
        self.setColumnHidden(1, True)
        self.setColumnHidden(2, True)
        self.setColumnHidden(3, True)
        self.header().hide()
        self.setAnimated(False)
        self.setIndentation(20)
        self.setSortingEnabled(True)
        self.setWindowTitle("Dir View")
        self.resize(640, 480)
    #设置工作目录
    def setWorkPath(self,workPath):
        self.myModel.setRootPath(workPath)
        self.setRootIndex(self.myModel.index(workPath))

#底部状态栏
from PyQt5.QtWidgets import QWidget
from UI.statusBarWidget import Ui_Form
class myStatusBarWidget(QWidget,Ui_Form):
    def __init__(self):
        super(myStatusBarWidget, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)

    def clearData(self):
        self.label_designDir.setText('')
        self.label_dipAngle.setText('')
        self.label_dirAngle.setText('')
        self.label_magneticAngle.setText('')
        self.label_magneticIntensity.setText('')

    def setDevStatus(self,designDir ,dipAngle,dirAngle,
                     magneticAngle,magneticIntensity):
        self.label_designDir.setText(designDir+'°')
        self.label_dipAngle.setText(dipAngle+'°')
        self.label_dirAngle.setText(dirAngle+'°')
        self.label_magneticAngle.setText(magneticAngle+'°')
        self.label_magneticIntensity.setText(magneticIntensity+'μT')


if __name__ == '__main__':
    import pyqtgraph.examples
    pyqtgraph.examples.run()


