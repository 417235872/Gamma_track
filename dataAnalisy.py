import numpy as np
import pandas as pd
import os
import serial.tools.list_ports as sl
from PyQt5.QtCore import QObject,pyqtSignal
import serial,time,re,struct,threading
dataHead = (
    "孔深，m",
    "倾角，°",
    "方位，°",
    "工具面，°",
    "水平位移，m",
    "左右位移，m",
    "上下位移，m",
    "左右偏差，m",
    "上下偏差，m",
    "地层信息",
    "距顶板，m",
    "距底板，m",
    "电池电压，V",
    "校验和",
    "磁场强度，μT",
    "温度，℃","测量时间",
    "测量日期"
               )
#自动搜索并返还可用端口的名称，若无可用的端口，将提示端口不存在或端口被占用
def search_available_port():
    plist = list(sl.comports())
    port_name = ""
    for i in range(len(plist)):
        plist_i = list(plist[i])
        try:
            ser = pd.serial.Serial(port=plist_i[0],baudrate=9600,bytesize=8,parity="N",stopbits=1,timeout=0.5)
            if not ser.isOpen():
                ser.open()
        except:
            continue
        else:
            port_name = plist_i[0]
            ser.close()
            break
    if port_name == "":
        print("Port is not existed or busy.")
    else:
        print("Port is:",port_name)
    return port_name

#从串口接收数据
class dataIO(QObject):
    #信号：接收数据
    receiveSignal = pyqtSignal(int)

    def __init__(self,parent = None):
        super().__init__()
        self.startDepth = 0#都是从零开始的
        print('dataIO')
        self.linkPort()#初始化端口
        self.chacked = True#停止接收线程标志
        self.dataHead = ['Depth','dip angle', 'direction angle', 'tool face angle','checksum',
                         'magnetic field intensity','temperature','cell voltage']
        self.refrashRate = 13#读取数据的频率
        self.myDataFrame = pd.DataFrame(columns = self.dataHead)
        self.dataDic = {'index': 0, 'data_0': None, 'data_1': None, 'data_2': None, 'data_3': None, 'data_4': None}

    #连接端口
    def linkPort(self):
        self.port = serial.Serial(port = 'COM7', baudrate=9600, bytesize=8, parity="N", stopbits=1, timeout=0.5)

    #从端口获取数据，将以dict形式返回
    def port_readData(self):
        print('IO_port_inWait',self.port.in_waiting)
        if self.port.in_waiting >= 31:
            data_source = self.port.read(31)#从端口中读取31bytes数据
            if data_source[:2] == b'\xaa\x55':#校验数据包包头
                data_unpack = struct.unpack('>'+'f'*7,data_source[2:-1])
                return data_unpack
            else:
                print('package head is not match')
                return None
        else:
            return None

    #数据接收模拟
    def dataReceive(self):
        time.sleep(2)
        while self.chacked:
            self.port.write(b'\x2a\xa2\xcc')
            time.sleep(1)
            dataList = self.port_readData()
            print(dataList)
            if self.dataDic['index'] < 5 and dataList != None:
                i = 'data_' + str(self.dataDic['index'])
                self.dataDic[i]= dataList
                self.dataDic['index'] += 1
            self.receiveSignal.emit(self.dataDic['index'])
            time.sleep(self.refrashRate)
        self.port.write(b'\x2a\xb2\xdc')

    # 导入数据进入dataFrom
    def getData(self, input):
        try:
            if self.dataDic['index'] == 0:
                return None
            else:
                data = self.dataDic['data_0']
                self.dataDic['index'] += -1
                for i in range(self.dataDic['index']):
                    self.dataDic['data_' + str(i)] = self.dataDic['data_' + str(i + 1)]
            if len(self.myDataFrame.index) == 0:
                depth = self.startDepth
                self.startDepth = 0
            else:
                depth = self.myDataFrame['Depth'].values[-1] + input
            se = pd.Series(data=[depth], name='Depth')
            dataPd = pd.DataFrame(data).join(se, sort=False,how='left')
            self.myDataFrame = self.myDataFrame.append(dataPd)
            self.receiveSignal.emit(self.dataDic['index'])
        except:
            import traceback
            traceback.print_exc()

    #向端口发送开始传输数据指令
    def start(self):
        self.receiveThreading = threading.Thread(target=self.dataReceive)
        self.receiveThreading.start()



import xml.etree.ElementTree as ET
#主孔/分支孔数据存储格式
'''
存储方案：
孔的分支信息存储在info.xml中；
数据存储在data.xlsx中，各个孔的数据放在不同的sheet中。
读取方案：
孔分支信息的info.xml读取为xml.etre.ElementTree。
数据根据孔分支信息载入孔路径（str）来从Excel文件中的对应sheet中载入数据。
===============主要参数============
path    track文件夹的位置
dataPath    track数据（Excel）的位置
infoPath    track分支信息（xml）位置
tree    以etree形式读取track分支信息（xml）
dataDic 以字典形式存储各分支的DataFrame，key为tree中的path信息
writer  pd.ExcelWriter(self.dataPath),用于DataFrame分sheet存储在Excel中
'''
class track(QObject):
    def __init__(self):
        super(track, self).__init__()
        self.path = None
        self.dataPath = None
        self.infoPath = None
        self.tree = None
        self.dataDic = {}
        self.writer = None

    #清除tree，writer和dataDic
    def clear(self):
        self.tree = None
        self.dataDic = {}
        self.writer = None

    #从目标路径中载入track
    def loadData(self,path : str):
        global dataHead
        #update path and data source
        self.clear()
        self.path = path
        self.infoPath = os.path.join(path,"info.xml")
        self.dataPath = os.path.join(path,"data.xlsx")
        self.writer = pd.ExcelWriter(self.dataPath)
        self.tree = ET.parse(self.infoPath)
        #load DataFrame from disk to memory.
        reader = pd.ExcelFile(self.dataPath)
        for i in self.tree.iter():
            j = i.find('index')
            if j is not None:
                self.dataDic[j.text] = reader.parse(sheet_name=j.text).set_index(dataHead[0])
        reader.close()

    #向目标路径中创建一个以那么参数为名的track，同时当前track转换到这个新的track
    #可以接收新track的的一些设计参数和辅助参数
    def creatRootTrack(self,path : str,name : str,**kwargs):
        global dataHead
        #create new data and infomation of track
        dataBase = pd.DataFrame(columns=dataHead).set_index(dataHead[0])
        with open("info_base.xml",'r') as file:
            infoText = file.read()
        baseTrack = ET.fromstring(infoText)
        baseTrack.find("./name").text = kwargs.get("name","RootTrack")
        baseTrack.find("./index").text = kwargs.get("name","RootTrack")
        baseTrack.find("./auxiliary/declination").text = str(kwargs.get("declination",0))
        baseTrack.find("./auxiliary/intensity").text = str(kwargs.get("intensity",0))
        baseTrack.find("./design/targetOrientation").text = str(kwargs.get("targetOrientation",0))
        baseTrack.find("./design/dipAngle").text = str(kwargs.get("dipAngle",0))
        baseTrack.find("./design/orientation").text = str(kwargs.get("orientation",0))
        #unpdate path and data source
        self.clear()
        self.path = os.path.join(path,name)
        self.infoPath = os.path.join(self.path,'info.xml')
        self.dataPath = os.path.join(self.path,"data.xlsx")
        self.tree = ET.ElementTree(element=baseTrack)
        self.writer = pd.ExcelWriter(self.dataPath)
        self.dataDic[kwargs.get("name","RootTrack")] = dataBase
        #save them
        os.mkdir(self.path)
        self.saveall()

    #将当前memory中的track数据保存到disk中
    def saveall(self):
        self.tree.write(self.infoPath)
        for key in self.dataDic:
            self.dataDic[key].to_excel(excel_writer=self.writer, sheet_name=key)
        self.writer.save()

    #在trackParent下创建一个名为trackName新的分支track
    #将会在etree中添加track节点，同时向dataDic中添加一个新的数据表
    def newTrackBranch(self,trackName : str,trackParent : ET.Element):
        branch = trackParent.find('branch')
        track = ET.SubElement(branch,"track")
        name = ET.SubElement(track,"name")
        index = ET.SubElement(track,'index')
        ET.SubElement(track,'note')
        ET.SubElement(track,"branch")
        name.text = trackName
        index.text = trackParent.find('path').text + "/" + trackName
        dataBase = pd.DataFrame(columns=dataHead).set_index(dataHead[0])
        self.dataDic[index.text] = dataBase
        return track

    #删除trackParent下的分支track
    #将从dataDic中删除track及其下的所有分支对应的数据表，同时从etree中删除该节点
    def removeTrackBranch(self,track : ET.Element,trackParent : ET.Element):
        for i in track.iter():
            index = i.find("index")
            if index is not None:
                self.dataDic.pop(index.text)
        trackParent.remove(track)


if __name__ == '__main__':
    track = track()
    track.loadData('test\\trackRoot')
    print(track.dataDic['RootTrack'].index)


