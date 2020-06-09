import pyqtgraph.examples
pyqtgraph.examples.run()
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import pyqtgraph as pg
import numpy as np
import pandas as pd
#load data as narray
# data = pd.read_excel("A:\工作\实验室\测斜软件\钻探所软件\钻探所软件\\导出实钻数据2017-02-17.xls")
# x = data['Unnamed: 5'][2:56].values
# y = data['Unnamed: 6'][2:56].values
# z = data['Unnamed: 7'][2:56].values

#initialize Qt mudel
app = QtGui.QApplication([])
w = gl.GLViewWidget()
w.setBackgroundColor(pg.mkColor("#B9B3A3"))
w.opts['distance'] = 40
w.show()
w.setWindowTitle('pyqtgraph example: GLLinePlotItem')

# add reference plane (x,y,z)
# gx = gl.GLGridItem()
# gx.rotate(90, 0, 1, 0)
# gx.translate(-10, 0, 0)
# #gx.setSize(x.max(),y.max(),z.max())
# w.addItem(gx)
# gy = gl.GLGridItem()
# gy.rotate(90, 1, 0, 0)
# gy.translate(0, -10, 0)
# #gy.setSize(x.max(),y.max(),z.max())
# w.addItem(gy)
# gz = gl.GLGridItem()
# gz.translate(0, 0, -10)
# #gz.setSize(x.max(),y.max(),z.max())
# w.addItem(gz)

# add aix for (x,y,z)
aix = gl.GLAxisItem()
aix.setSize(100,100,100,size=QtGui.QVector3D(50,50,50))
w.addItem(aix)

def fn(x, y):
    return np.cos((x ** 2 + y ** 2) ** 0.5)


n = 51
y = np.linspace(-10, 10, n)
x = np.linspace(-10, 10, 100)
for i in range(n):
    yi = np.array([y[i]] * 100)
    d = (x ** 2 + yi ** 2) ** 0.5
    z = 10 * np.cos(d) / (d + 1)
    pts = np.vstack([x, yi, z]).transpose()
    print("vstack",np.vstack([x, yi, z]))
    print("transpose",pts)
    plt = gl.GLLinePlotItem(pos=pts, color=pg.glColor((i, n * 1.3)), width=(i + 1) / 10., antialias=True)
    w.addItem(plt)

# pts = np.vstack([x, y, z]).transpose()
# plt = gl.GLLinePlotItem(pos=pts, color=pg.glColor("#FFD773"), width=10, antialias=True)
# w.addItem(plt)

## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()