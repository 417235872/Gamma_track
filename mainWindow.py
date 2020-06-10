import sys
import numpy as np
import pyqtgraph as pg
import pyqtgraph.opengl as pl
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from UI.mainWindows import Ui_MainWindow
from dataAnalisy import *
from dilog import projectFileChooseDialog,chooseRootTrackDialog
from myItem import *
trackData = track()

class myWindow(QMainWindow,Ui_MainWindow):
    global trackData
    def __init__(self):
        super(myWindow, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.setMore()
        self.setEvent()

    def setMore(self):
        self.projectPath = None
        #各图像元素的存储
        self.DataItemDic_3D = {}
        self.DesignItemDic_3D = {}
        self.XplotDic = {}
        self.YplotDic = {}
        self.ZplotDic = {}
        #链接2D投影图的坐标轴
        self.link2DplotAxis()
        #添加3D网格参考面
        self.addGrid3D()

    def setEvent(self):
        self.action_menu_openProjiect.triggered.connect(self.openProject_event)
        self.action_menu_newProject.triggered.connect(self.newProject_event)
        self.action_tool_chooseMainTrack.triggered.connect(self.chooseMainTrack_event)
        #设置滑动条和示数框关联
        self.horizontalSlider_referenceX.valueChanged.connect(self.linkSliderToBox_X)
        self.horizontalSlider_referenceY.valueChanged.connect(self.linkSliderToBox_Y)
        self.horizontalSlider_referenceZ.valueChanged.connect(self.linkSliderToBox_Z)
        self.doubleSpinBox_referenceX.valueChanged.connect(self.linkBoxToSlider_X)
        self.doubleSpinBox_referenceY.valueChanged.connect(self.linkBoxToSlider_Y)
        self.doubleSpinBox_referenceZ.valueChanged.connect(self.linkBoxToSlider_Z)

    #菜单事件：打开钻场
    def openProject_event(self):
        path,reply = projectFileChooseDialog().getOpenProject()
        if reply:
            self.setProjectPath(path)

    #菜单事件：新建钻场
    def newProject_event(self):
        path, reply = projectFileChooseDialog().getOpenProject()
        if reply:
            self.setProjectPath(path)

    #设置当前选择的钻场文件的路径
    def setProjectPath(self,path):
        self.projectPath = path

    #工具栏事件：选择主孔
    def chooseMainTrack_event(self):
        global trackData
        path,choosed = chooseRootTrackDialog().Dialog_show(projectPath=self.projectPath)
        if choosed:
            self.loadTrack(path)

    #工具栏事件：滑块和示数框关联
    def linkSliderToBox_X(self):
        self.Grid_XoZ.translate(0, 0, self.horizontalSlider_referenceX.value() - self.doubleSpinBox_referenceX.value())
        self.doubleSpinBox_referenceX.setValue(self.horizontalSlider_referenceX.value())
    def linkBoxToSlider_X(self):
        self.Grid_XoZ.translate(0, 0,  self.doubleSpinBox_referenceX.value() - self.horizontalSlider_referenceX.value())
        self.horizontalSlider_referenceX.setValue(self.doubleSpinBox_referenceX.value())
    def linkSliderToBox_Y(self):
        self.Grid_XoY.translate(0, self.horizontalSlider_referenceY.value() - self.doubleSpinBox_referenceY.value(), 0)
        self.doubleSpinBox_referenceY.setValue(self.horizontalSlider_referenceY.value())
    def linkBoxToSlider_Y(self):
        self.Grid_XoY.translate(0, self.doubleSpinBox_referenceY.value() - self.horizontalSlider_referenceY.value(), 0)
        self.horizontalSlider_referenceY.setValue(self.doubleSpinBox_referenceY.value())
    def linkSliderToBox_Z(self):
        self.Grid_YoZ.translate( -(self.horizontalSlider_referenceZ.value() - self.doubleSpinBox_referenceZ.value()),0, 0)
        self.doubleSpinBox_referenceZ.setValue(self.horizontalSlider_referenceZ.value())
    def linkBoxToSlider_Z(self):
        self.Grid_YoZ.translate( -(self.doubleSpinBox_referenceZ.value() - self.horizontalSlider_referenceZ.value()),0, 0)
        self.horizontalSlider_referenceZ.setValue(self.doubleSpinBox_referenceZ.value())



    #初始化：连接各二维投影图像的相同轴
    def link2DplotAxis(self):
        self.widget_z.plotItem.setXLink(self.widget_y.plotItem)
        self.widget_z.plotItem.setYLink(self.widget_x.plotItem)

    #初始化：向openGL中添加网格参考面
    def addGrid3D(self):
        print("3D Grid")
        self.Grid_YoZ = myGLGridItem_YoZ(parent=self.threeDwidget)
        self.Grid_YoZ.setSize(10,10,10)
        self.threeDwidget.addItem(self.Grid_YoZ)
        self.Grid_XoZ = myGLGridItem_XoZ(parent=self.threeDwidget)
        self.Grid_XoZ.setSize(10,10,10)
        self.threeDwidget.addItem(self.Grid_XoZ)
        self.Grid_XoY = myGLGridItem_XoY(parent=self.threeDwidget)
        self.Grid_XoY.setSize(10,10,10)
        self.threeDwidget.addItem(self.Grid_XoY)

    #载入测斜轨迹数据，并创建图像元素到相应Dic中（主孔加分支孔）{暂时没有添加设计文件}
    def loadTrack(self,path):
        global trackData
        trackData.loadData(path)
        self.treeWidget.setTrackInfo(trackData.tree)
        self.plotClear()
        self.DataItemDic_3D.clear()
        self.XplotDic.clear()
        self.YplotDic.clear()
        self.ZplotDic.clear()
        #根据数据生成图像元素
        for key in trackData.dataDic:
            # 这里要注意openGL内的坐标系为右手系，向左是X轴，向上是Y轴，垂直屏幕向外是Z轴。为匹配各方向投影的2D图像，
            # x轴为负的水平坐标，y轴为上下位移，z轴为左右位移
            dataCoordinate = np.vstack([-trackData.dataDic[key][dataHead[4]],
                                        trackData.dataDic[key][dataHead[6]],
                                        trackData.dataDic[key][dataHead[5]]]).transpose()
            self.DataItemDic_3D[key] = pl.GLLinePlotItem(pos=dataCoordinate,color =pg.glColor('b'),
                                                         width = 2,antialias=True)
            #轨迹的正视图
            self.XplotDic[key] = pg.PlotDataItem(x=trackData.dataDic[key][dataHead[4]].values,
                                                      y=trackData.dataDic[key][dataHead[5]].values)
            #轨迹的俯视图
            self.YplotDic[key] = pg.PlotDataItem(x=trackData.dataDic[key][dataHead[6]].values,
                                                 y=trackData.dataDic[key][dataHead[4]].values)
            #轨迹的左视图
            self.ZplotDic[key] = pg.PlotDataItem(x=trackData.dataDic[key][dataHead[6]].values,
                                                 y=trackData.dataDic[key][dataHead[5]].values)
        self.printPlot()
        self.autoGridSet()

    #辅助：清空画布上的元素
    def plotClear(self,goal = "ALL"):
        if goal == "ALL" or goal == "3D":
            for item in self.threeDwidget.items:
                if item not in [self.Grid_XoY,self.Grid_XoZ,self.Grid_YoZ]:
                    self.threeDwidget.removeItem(item)
        if goal == "ALL" or goal == "2D":
            self.widget_x.plotItem.clear()
            self.widget_y.plotItem.clear()
            self.widget_z.plotItem.clear()

    #辅助：将图像元素添加到对应的plot中进行绘图{暂时没有添加设计轨迹,只支持显示所有轨迹，没有添加自定义颜色功能}
    def printPlot(self):
        #if self.radioButton_showAll.isChecked():
        for key in self.DataItemDic_3D:
            self.threeDwidget.addItem(self.DataItemDic_3D[key])
            self.widget_x.plotItem.addItem(self.XplotDic[key])
            self.widget_y.plotItem.addItem(self.YplotDic[key])
            self.widget_z.plotItem.addItem(self.ZplotDic[key])

    #设置当前程序载入的主孔
    def setRootTrack(self,trackPath):
        global trackData
        trackData.loadData(trackPath)
        self.treeWidget.setTrackInfo(trackData.tree)
        for key in trackData.dataDic:
            # 这里要注意openGL内的坐标系为右手系，向左是X轴，向上是Y轴，垂直屏幕向外是Z轴。为匹配各方向投影的2D图像，
            # x轴为负的水平坐标，y轴为上下位移，z轴为左右位移
            dataCoordinate =np.vstack([-trackData.dataDic[key][dataHead[4]],
                                       trackData.dataDic[key][dataHead[6]],
                                       trackData.dataDic[key][dataHead[5]]]).transpose()
            d = pl.GLLinePlotItem(pos=dataCoordinate,color =pg.glColor('b'),width = 2,antialias=True)
            self.threeDwidget.addItem(d)
            xplot = self.widget_x.plotItem.plot()
            xplot.setData(x=trackData.dataDic[key][dataHead[4]].values,y=trackData.dataDic[key][dataHead[5]].values)
            yplot = self.widget_y.plotItem.plot()
            yplot.setData(x=trackData.dataDic[key][dataHead[6]].values,y=trackData.dataDic[key][dataHead[4]].values)
            zplot = self.widget_z.plotItem.plot()
            zplot.setData(x=trackData.dataDic[key][dataHead[6]].values,y=trackData.dataDic[key][dataHead[5]].values)

    #辅助：自动设置网面的长度和刻度
    def autoGridSet(self):
        global trackData
        Xmaxlist = np.array([])
        Ymaxlist = np.array([])
        Zmaxlist = np.array([])
        for frame in trackData.dataDic.values():
            print("MAX:x-{0};y-{1};z-{2}".format(np.abs(frame[dataHead[4]].values).max(axis=0),
                                                 np.abs(frame[dataHead[6]].values).max(axis=0),
                                                 np.abs(frame[dataHead[5]].values).max(axis=0)))
            Xmaxlist = np.append(Xmaxlist,np.abs(frame[dataHead[4]].values).max(axis=0))
            Ymaxlist = np.append(Ymaxlist,np.abs(frame[dataHead[6]].values).max(axis=0))
            Zmaxlist = np.append(Zmaxlist,np.abs(frame[dataHead[5]].values).max(axis=0))
        print("MAX2:x-{0};y-{1};z-{2}".format(Xmaxlist,Ymaxlist.max(axis=0),Zmaxlist.max(axis=0)))
        if Xmaxlist.max(axis=0) >= 7:
            Xmax = Xmaxlist.max(axis=0) + 3
        else:
            Xmax = 10
        if Ymaxlist.max(axis=0) >= 7:
            Ymax = Ymaxlist.max(axis=0) + 3
        else:
            Ymax = 10
        if Zmaxlist.max(axis=0) >= 7:
            Zmax = Zmaxlist.max(axis=0) + 3
        else:
            Zmax = 10
        print("SET:x-{0};y-{1};z-{2}".format(Xmax,Ymax,Zmax))
        self.Grid_XoY.setSize(Xmax,Zmax,Ymax)
        self.Grid_XoY.setSpacing(int(Xmax/10),int(Zmax/10),int(Ymax/10))
        self.Grid_YoZ.setSize(Zmax,Ymax,Xmax)
        self.Grid_YoZ.setSpacing(int(Zmax/10),int(Ymax/10),int(Xmax/10))
        self.Grid_XoZ.setSize(Xmax,Ymax,Zmax)
        self.Grid_XoZ.setSpacing(int(Xmax/10),int(Ymax/10),int(Zmax/10))

    #辅助：设置调节各网面位置的范围
    def setGridMoveRange(self,x = 10,y = 10,z = 10):
        self.horizontalSlider_referenceX.setMaximum(int(y))
        self.horizontalSlider_referenceX.setMinimum(int(-y))
        self.doubleSpinBox_referenceX.setMaximum(int(y))
        self.doubleSpinBox_referenceX.setMinimum(int(-y))

        self.horizontalSlider_referenceY.setMaximum(int(z))
        self.horizontalSlider_referenceY.setMinimum(int(z))
        self.doubleSpinBox_referenceY.setMaximum(int(z))
        self.doubleSpinBox_referenceY.setMaximum(int(-z))

        self.horizontalSlider_referenceZ.setMaximum(int(x))
        self.horizontalSlider_referenceZ.setMinimum(int(-x))
        self.doubleSpinBox_referenceZ.setMaximum(int(x))
        self.doubleSpinBox_referenceZ.setMaximum(int(-x))










if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = myWindow()
    w.show()
    sys.exit(app.exec_())
