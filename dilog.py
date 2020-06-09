from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
#打开文件对话框
from UI.projectFileChooseDialog import Ui_Dialog
#选择钻场 对话框
import os
from UI.projectFileChooseDialog import Ui_Dialog
class projectFileChooseDialog(QDialog,Ui_Dialog):
    def __init__(self,tip = '请选择'):
        super().__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.setEvent()
        self.setMore()
        self.label_topTip.setText(tip)

    #其他设置
    def setMore(self):
        #表示是否已经选择
        self.choosed = False
        self.Path = ''
        #只显示文件夹
        self.treeView.myModel.setFilter(QDir.Dirs|QDir.NoDotAndDotDot)
        #测试时，向toolButton添加文子
        self.back_toolButton.setText("退后")
        self.desktop_toolButton.setText("桌面")
        self.disk_toolButton.setText("磁盘")

    #链接信号与动作
    def setEvent(self):
        self.treeView.clicked.connect(self.treeView_clicked_event)
        self.treeView.doubleClicked.connect(self.treeView_doubleClicked_evnet)
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_OK.clicked.connect(self.pushButton_OK_clicked_evevnt)
        self.back_toolButton.clicked.connect(self.back_toolButton_clicked_event)
        self.desktop_toolButton.clicked.connect(self.desktop_toolButton_clicked_event)
        self.disk_toolButton.clicked.connect(self.disk_toolButton_clicked_event)

    # 右上角图标按钮动作
    def back_toolButton_clicked_event(self):
        newPath = self.treeView.myModel.rootPath()
        if newPath != '':
            toPath = os.path.split(newPath)[0]
            self.treeView.setWorkPath(toPath)
            self.lineEdit_currentChoose.setText(toPath)

    #动作：从磁盘选择
    def disk_toolButton_clicked_event(self):
        self.treeView.setWorkPath('')
        self.lineEdit_currentChoose.setText('')

    #动作：从桌面选择
    def desktop_toolButton_clicked_event(self):
        path = os.path.join(os.path.expanduser('~'), 'Desktop')
        if os.path.exists(path):
            self.treeView.setWorkPath(path)
            self.lineEdit_currentChoose.setText(path)

    #确认按钮动作
    def pushButton_OK_clicked_evevnt(self):
        # 检查
        if os.path.exists(self.lineEdit_currentChoose.text()):
            if os.path.exists(os.path.join(self.lineEdit_currentChoose.text(), '.trackNote')):
                self.Path = self.lineEdit_currentChoose.text()
                self.choosed = True
                self.close()
            else:
                reply = QMessageBox.information(self, "提示", "这不是一个测斜钻场文件")
        else:
            reply = QMessageBox.warning(self, '错误', '输入路径错误！')

    #树控件 单击动作
    def treeView_clicked_event(self,index):
        #将值传入line控件
        path = self.treeView.myModel.filePath(index)
        self.lineEdit_currentChoose.setText(path)

    #树控件 双击动作
    def treeView_doubleClicked_evnet(self,index):
        if self.treeView.myModel.isDir(index):
            self.treeView.setWorkPath(self.treeView.myModel.filePath(index))

    #调用静态方法来快速创建选择项目的对话框，将返回选择项目的路径和是否确认选择的bool值
    @staticmethod
    def getOpenProject(parent = None):
        #返回选择项目的路径和是否已经选择
        myself = projectFileChooseDialog('请选择要打开的项目')
        myself.setWindowTitle('选择项目')
        myself.exec_()
        return (myself.Path,myself.choosed)

from UI.newProjectFileDialog import Ui_Dialog
class newProjectFileDialog(QDialog,Ui_Dialog):
    def __init__(self,tip = '请选择'):
        super().__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.setEvent()
        self.setMore()
        self.label_topTip.setText(tip)

    #其他设置
    def setMore(self):
        #表示是否已经选择
        self.choosed = False
        self.Path = ''
        #只显示文件夹
        self.treeView.myModel.setFilter(QDir.Dirs|QDir.NoDotAndDotDot)
        #测试时，向toolButton添加文子
        self.back_toolButton.setText("退后")
        self.desktop_toolButton.setText("桌面")
        self.disk_toolButton.setText("磁盘")

    #链接信号与动作
    def setEvent(self):
        self.treeView.clicked.connect(self.treeView_clicked_event)
        self.treeView.doubleClicked.connect(self.treeView_doubleClicked_evnet)
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_OK.clicked.connect(self.pushButton_OK_clicked_evevnt)
        self.back_toolButton.clicked.connect(self.back_toolButton_clicked_event)
        self.desktop_toolButton.clicked.connect(self.desktop_toolButton_clicked_event)
        self.disk_toolButton.clicked.connect(self.disk_toolButton_clicked_event)

    # 右上角图标按钮动作
    def back_toolButton_clicked_event(self):
        newPath = self.treeView.myModel.rootPath()
        if newPath != '':
            toPath = os.path.split(newPath)[0]
            self.treeView.setWorkPath(toPath)
            self.lineEdit_currentChoose.setText(toPath)

    #动作：从磁盘选择
    def disk_toolButton_clicked_event(self):
        self.treeView.setWorkPath('')
        self.lineEdit_currentChoose.setText('')

    #动作：从桌面选择
    def desktop_toolButton_clicked_event(self):
        path = os.path.join(os.path.expanduser('~'), 'Desktop')
        if os.path.exists(path):
            self.treeView.setWorkPath(path)
            self.lineEdit_currentChoose.setText(path)

    #确认按钮动作
    def pushButton_OK_clicked_evevnt(self):
        #检查选择路径是否存在，同时创建钻场文件
        if os.path.exists(self.lineEdit_currentChoose.text()):
            self.Path = os.path.join(self.lineEdit_currentChoose.text(),self.lineEdit_projectName.text())
            os.mkdir(self.Path)
            with open(os.path.join(self.Path,'.trackNote'),'w') as file:
                pass
            self.choosed = True
            self.close()
        else:
            reply = QMessageBox.warning(self,'错误','输入路径错误！')

    #树控件 单击动作
    def treeView_clicked_event(self,index):
        #将值传入line控件
        path = self.treeView.myModel.filePath(index)
        self.lineEdit_currentChoose.setText(path)

    #树控件 双击动作
    def treeView_doubleClicked_evnet(self,index):
        if self.treeView.myModel.isDir(index):
            self.treeView.setWorkPath(self.treeView.myModel.filePath(index))

    #调用静态方法来快速创建选择项目的对话框，将返回选择项目的路径和是否确认选择的bool值
    @staticmethod
    def getOpenProject(parent = None):
        #返回选择项目的路径和是否已经选择
        myself = projectFileChooseDialog('请选择要打开的项目')
        myself.setWindowTitle('选择项目')
        myself.exec_()
        return (myself.Path,myself.choosed)

from dataAnalisy import track
from UI.chooseRootTrack import Ui_Dialog
class chooseRootTrackDialog(QDialog,Ui_Dialog):
    '''
    主孔列表目前暂时使用stringModel，后期有需要可以改成IconModel显示图标和文字
    '''
    def __init__(self):
        super(chooseRootTrackDialog, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.setMore()
        self.setEvent()
    def setMore(self):
        self.choosed = False
        self.trackPath = None
        self.projectPath = None
        self.listModel = QStringListModel()
        self.listView_RootTrack.setModel(self.listModel)
        self.listView_RootTrack.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def setEvent(self):
        self.listView_RootTrack.doubleClicked.connect(self.selectRootTrack)
        self.pushButton_OK.clicked.connect(self.pushButton_OK_event)
        self.pushButton_Cancel.clicked.connect(self.close)
        self.toolButton_newRootTrack.clicked.connect(self.toolButton_newRootTrack_event)

    def setProjectPath(self,path : str):
        self.projectPath = path
        self.refreshlist()

    def refreshlist(self):
        l = os.listdir(self.projectPath)
        l.remove('.trackNote')
        self.listModel.setStringList(l)

    def selectRootTrack(self):
        rootTrack = self.listView_RootTrack.currentIndex().data()
        self.trackPath = os.path.join(self.projectPath,str(rootTrack))
        print(os.path.join(self.trackPath,'info.xml'))
        self.treeWidget_TrackBranch._loadTrackInfo(os.path.join(self.trackPath,'info.xml'))

    def pushButton_OK_event(self):
        if self.trackPath is not None:
            self.choosed = True
            self.close()
        else:
            reply = QMessageBox.information(self,"注意","当前未选择任何主孔！")

    def toolButton_newRootTrack_event(self):
        print(self.projectPath)
        newRootTrackDailog.Dialog_show(projectPath=self.projectPath)
        self.refreshlist()



    @staticmethod
    def Dialog_show(parent = None,projectPath = None):
        myself = chooseRootTrackDialog()
        if projectPath is not None:
            myself.setProjectPath(path=projectPath)
        myself.exec_()
        return (myself.trackPath,myself.choosed)

from UI.newRootTrackDailog import Ui_Dialog
class newRootTrackDailog(QDialog,Ui_Dialog):
    def __init__(self,path):
        super(newRootTrackDailog, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.projectPath = path
        self.setMore()
        self.setEvent()


    def setMore(self):
        self.checked = False


    def setEvent(self):
        self.pushButton_OK.clicked.connect(self.pushButton_OK_event)
        self.pushButton_Cancel.clicked.connect(self.pushButton_Cancel_event)

    def pushButton_Cancel_event(self):
        self.close()

    def pushButton_OK_event(self):
        targetPath = os.path.join(self.projectPath,self.lineEdit_Name.text())
        print(targetPath)
        if os.path.exists(targetPath):
            reply = QMessageBox.warning(self,'警告','已存在同名主孔！')
        else:
            print(self.doubleSpinBox_dipAngle.text()[:-1],self.doubleSpinBox_intensity.text()[:-2],
                  self.spinBox_designOrientation.text()[:-1],self.spinBox_angle.text()[:-1],
                  self.spinBox_orientation.text()[:-1])
            track().newRootTrack(self.projectPath,self.lineEdit_Name.text(),
                                 declination=self.doubleSpinBox_dipAngle.text()[:-1],
                                 intensity=self.doubleSpinBox_intensity.text()[:-2],
                                 targetOrientation=self.spinBox_designOrientation.text()[:-1],
                                 dipAngle=self.spinBox_angle.text()[:-1],
                                 orientation=self.spinBox_orientation.text()[:-1]
            )
            self.checked =True
            self.close()

    @staticmethod
    def Dialog_show(parent=None,projectPath=None):
        # 返回选择项目的路径和是否已经选择
        myself = newRootTrackDailog(projectPath)
        myself.exec_()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    dialog = newRootTrackDailog("./test/GammaTrack")
    dialog.show()
    sys.exit(app.exec_())