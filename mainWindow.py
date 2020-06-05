import sys
import numpy as np
import pyqtgraph as pg
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from UI.mainWindows import Ui_MainWindow
from dataAnalisy import *
trackData = track()

class myWindow(QMainWindow,Ui_MainWindow):
    global trackData
    def __init__(self):
        super(myWindow, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.setMore()

    def setMore(self):
        self.projectPath = None

    def setEvent(self):
        pass





if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = myWindow()
    w.show()
    sys.exit(app.exec_())
