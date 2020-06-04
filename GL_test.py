from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtOpenGL import QGLWidget
import sys
from OpenGL.GL import *
from OpenGL.WGL import *
import win32ui
from numpy import sin,cos


class MainWindow(QMainWindow):
    """docstring for Mainwindow"""

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.basic()
        splitter_main = self.split_()
        self.setCentralWidget(splitter_main)

    # 窗口基础属性
    def basic(self):
        # 设置标题，大小，图标
        self.setWindowTitle("GT")
        self.resize(1100, 650)
        self.setWindowIcon(QIcon("./image/Gt.png"))
        # 居中显示
        screen = QDesktopWidget().geometry()
        self_size = self.geometry()
        self.move((screen.width() - self_size.width()) / 2, (screen.height() - self_size.height()) / 2)

    # 分割窗口
    def split_(self):
        splitter = QSplitter(Qt.Vertical)
        s = OpenGLWidget()  # 将opengl例子嵌入GUI
        splitter.addWidget(s)
        # testedit = QTextEdit()
        # splitter.addWidget(testedit)
        # splitter.setStretchFactor(0, 3)
        # splitter.setStretchFactor(1, 2)
        splitter_main = QSplitter(Qt.Horizontal)
        # textedit_main = QTextEdit()
        #splitter_main.addWidget(textedit_main)
        splitter_main.addWidget(splitter)
        splitter_main.setStretchFactor(0, 1)
        splitter_main.setStretchFactor(1, 4)
        return splitter_main


class OpenGLWidget(QGLWidget):
    window = 0
    base = None
    cnt1 = 0
    cnt2 = 0
    def initializeGL(self):
        pass
        # glShadeModel(GL_SMOOTH)  # Enables Smooth Color Shading
        # glClearColor(0.0, 0.0, 122, 0.5)  # This Will Clear The Background Color To Black
        # glClearDepth(1.0)  # Enables Clearing Of The Depth Buffer
        # glEnable(GL_DEPTH_TEST)  # Enables Depth Testing
        # glDepthFunc(GL_LEQUAL)  # The Type Of Depth Test To Do
        # glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)  # Really Nice Perspective Calculations
        # #self.BuildFont()

    def paintGL(self):
        self.BuildTran()
        #self.DrawGLScene()
        # ---------------------------------------------------------------
        glFlush()  # 清空缓冲区，将指令送往硬件立即执行


    def BuildFont(self):
        print('buildFont')
        wgldc = wglGetCurrentDC()
        hDC = win32ui.CreateDCFromHandle(wgldc)

        self.base = glGenLists(96)  # // Storage For 96 Characters, plus 32 at the start...
        print("base",type(self.base))
        # CreateFont () takes a python dictionary to specify the requested font properties.
        font_properties = {"name": "Courier New",
                           "width": 0,
                           "height": -24,
                           "weight": 800
                           }
        font = win32ui.CreateFont(font_properties)
        print("font",type(font))
        # // Selects The Font We Want
        oldfont = hDC.SelectObject(font)
        # // Builds 96 Characters Starting At Character 32
        wglUseFontBitmaps(wgldc, 32, 96, self.base + 32)
        # // reset the font
        hDC.SelectObject(oldfont)
        # // Delete The Font (python will cleanup font for us...)

    def BuildTran(self):
        glBegin(GL_LINES)  # 开始绘制线段（世界坐标系）

        # 以红色绘制x轴
        glColor4f(1.0, 0.0, 0.0, 1.0)  # 设置当前颜色为红色不透明
        glVertex3f(-0.8, 0.0, 0.0)  # 设置x轴顶点（x轴负方向）
        glVertex3f(0.8, 0.0, 0.0)  # 设置x轴顶点（x轴正方向）

        # 以绿色绘制y轴
        glColor4f(0.0, 1.0, 0.0, 1.0)  # 设置当前颜色为绿色不透明
        glVertex3f(0.0, -0.8, 0.0)  # 设置y轴顶点（y轴负方向）
        glVertex3f(0.0, 0.8, 0.0)  # 设置y轴顶点（y轴正方向）

        # 以蓝色绘制z轴
        glColor4f(0.0, 0.0, 1.0, 1.0)  # 设置当前颜色为蓝色不透明
        glVertex3f(0.0, 0.0, -0.8)  # 设置z轴顶点（z轴负方向）
        glVertex3f(0.0, 0.0, 0.8)  # 设置z轴顶点（z轴正方向）

        glEnd()  # 结束绘制线段

        # ---------------------------------------------------------------
        glBegin(GL_TRIANGLES)  # 开始绘制三角形（z轴负半区）

        glColor4f(1.0, 0.0, 0.0, 1.0)  # 设置当前颜色为红色不透明
        glVertex3f(-0.5, -0.366, -0.5)  # 设置三角形顶点
        glColor4f(0.0, 1.0, 0.0, 1.0)  # 设置当前颜色为绿色不透明
        glVertex3f(0.5, -0.366, -0.5)  # 设置三角形顶点
        glColor4f(0.0, 0.0, 1.0, 1.0)  # 设置当前颜色为蓝色不透明
        glVertex3f(0.0, 0.5, -0.5)  # 设置三角形顶点

        glEnd()  # 结束绘制三角形
        self.renderText(0.5,0.5,0.5,"151")




    def KillFont(self):
        """ // Delete The Font List
        """
        # // Delete All 96 Characters
        glDeleteLists(self.base, 32 + 96)

    def glPrint(self,s:str):
        """ // Custom GL "Print" Routine
        """

        # // If THere's No Text Do Nothing
        if (s == None):
            return
        if (s == ""):
            return
        glPushAttrib(GL_LIST_BIT)  # // Pushes The Display List Bits
        try:
            glListBase(self.base) # // Sets The Base Character to 32
            glCallLists(s)  # // Draws The Display List Text
            print(s)
            print(self.base)
        finally:
            glPopAttrib()  # // Pops The Display List Bits
        return




    # The main drawing function.
    def DrawGLScene(self):

        # // Clear The Screen And The Depth Buffer
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslate(-1,0,0)

        glLoadIdentity()  # // Reset The Current Modelview Matrix
        glTranslatef(0.0, 0.0, -1.0)  # // Move One Unit Into The Screen

        # // Pulsing Colors Based On Text Position
        glColor3f(225, 225, 225)
        # // Position The Text On The Screen
        glRasterPos2f(-0.45 + 0.05 * cos(self.cnt1), 0.32 * sin(self.cnt2))
        self.glPrint("Active OpenGL Text With NeHe - {:7.2f}".format(self.cnt1))  # // Print GL Text To The Screen
        self.cnt1 += 0.051  # // Increase The First Counter
        self.cnt2 += 0.005  # // Increase The First Counter
        return True


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
