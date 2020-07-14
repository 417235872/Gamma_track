import numpy as np
import pandas as pd
from PyQt5.QtWidgets import QDialog
from myItem import pandasModel
from UI.designTrackTable import Ui_Dialog
from dataAnalisy import designHead
class designTrackTableDialog(QDialog,Ui_Dialog):
    def __init__(self):
        super(designTrackTableDialog, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.setMore()
        self.setEvent()

    def setMore(self):
        self.data = pd.DataFrame()
        self.OK = False

    def setEvent(self):
        self.pushButton_addRow.clicked.connect(self.addRow)
        self.pushButton_deletRow.clicked.connect(self.deletRow)
        self.pushButton_Cancel.clicked.connect(self.close)
        self.pushButton_OK.clicked.connect(self.pushButton_OK_event)

    def pushButton_OK_event(self):
        self.OK = True
        self.close()

    def addRow(self):
        if self.data.shape[0] != 0:
            result = addDesignRowDialog.openDailog(*self.data.reset_index().iloc[-1].values)
        else:
            result = addDesignRowDialog.openDailog()
        if result[0]:
            datadic = {}
            for index in range(0,len(designHead),1):
                datadic[designHead[index]] = [result[index+1]]
            data = pd.DataFrame(datadic).set_index(designHead[0])
            self.data = self.data.append(data)
            self.setData(self.data)

    def deletRow(self):
        if self.data.shape[0] > 0:
            self.data = self.data.drop(self.data.index[-1])
            self.setData(self.data)

    def setData(self,data : pd.DataFrame):
        self.data = data
        self.dataModel = pandasModel(data=data)
        self.tableView.setModel(self.dataModel)

    @staticmethod
    def openDailog(data):
        dailog = designTrackTableDialog()
        dailog.setData(data)
        dailog.exec_()
        return dailog.OK,dailog.data
        



from UI.addDesignRowDialog import Ui_Dialog
class addDesignRowDialog(Ui_Dialog,QDialog):
    def __init__(self):
        super(addDesignRowDialog, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.setMore()
        self.setEvent()

    def setMore(self):
        self.choose = False

    def setEvent(self):
        self.pushButton_OK.clicked.connect(self.PushButton_OK_event)
        self.pushButton_Cancel.clicked.connect(self.PushButton_Cancel_event)

    def PushButton_OK_event(self):
        self.choose = True
        self.close()

    def PushButton_Cancel_event(self):
        self.close()


    @staticmethod
    def openDailog(*args):
        dailog = addDesignRowDialog()
        if len(args) == 5:
            dailog.spinBox_deep.setValue(args[0]+6)
            dailog.doubleSpinBox_designAngle.setValue(args[1])
            dailog.doubleSpinBox_designDirction.setValue(args[2])
            dailog.spinBox_top.setValue(args[3])
            dailog.spinBox_bottom.setValue(args[4])
        dailog.spinBox_deep.setMinimum(args[0]+6)
        dailog.exec_()
        return dailog.choose,dailog.spinBox_deep.value(),dailog.doubleSpinBox_designAngle.value(),\
               dailog.doubleSpinBox_designDirction.value(),dailog.spinBox_top.value(),dailog.spinBox_bottom.value()

import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QTableView
from PyQt5.QtCore import QAbstractTableModel, Qt
from dataAnalisy import track
if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = designTrackTableDialog()
    myTrack = track()
    myTrack.loadData("A:\\工作\\实验室\\测斜软件\\Gamma_track\\test\GammaTrack\\mytrack")
    view.setData(myTrack.designDic["RootTrack"])
    view.show()
    sys.exit(app.exec_())
