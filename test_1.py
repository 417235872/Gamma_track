import numpy as np
import pandas as pd
from dataAnalisy import track,designHead
depth_ = 0
def trans(depth,dipAngle,dirAngle):
    global depth_
    if depth - depth_ >= 0:
        i = depth - depth_
        depth_ = depth
    else:
        i = 0
        depth_ = depth

    z = i*np.cos(dipAngle)
    xOy = i*np.sin(dipAngle)
    x = xOy*np.sin(dirAngle)
    y = xOy*np.cos(dirAngle)
    print(i,dipAngle,dirAngle,np.sin(dirAngle))
    return x,y,z
def AngelToCoor(design : pd.DataFrame):
    depth_ = design.index.values[0]
    diff = np.append(depth_,design.index.values[1:] - design.index.values[:-1])
    tempLen = diff * np.cos(design[designHead[1]]/180 * np.pi)
    x = np.cumsum(tempLen * np.cos(design[designHead[2]]/180 * np.pi))
    y = np.cumsum(tempLen * np.sin(design[designHead[2]]/180 * np.pi))
    z = np.cumsum(diff * np.sin(design[designHead[1]]/180 * np.pi))

    #
    # temlen = depth_*np.sin(o)
    # x = np.array([temlen*np.sin(design[designHead[2]].loc(depth_))])
    # y = np.array([temlen*np.cos(design[designHead[2]].loc(depth_))])
    # z = np.array([depth_ * np.cos(design[designHead[1]].loc(depth_))])
    # for i in design.index.values[1:]:
    #     depth = i - depth_
    #     depth_ = i
    #     z = np.append(z,depth * np.cos(design[designHead[1]].loc(i)) + z[-1])
    #     temlen = depth * np.sin(design[designHead[1]].loc(i))
    #     x = np.append(x,temlen * np.sin(design[designHead[2]].loc(i)) + x[-1])
    #     y = np.append(y,temlen * np.cos(design[designHead[2]].loc(i)) + y[-1])
    return pd.DataFrame({"X":x,"Y":y,"Z":z,"depth":design.index.values}).set_index("depth")

myTrack = track()
myTrack.loadData("A:\\工作\\实验室\\测斜软件\\Gamma_track\\test\\GammaTrack\\mytrack")
for i in myTrack.designDic.keys():
    print(designHead)
    print(i)
    print(myTrack.designDic[i])
    print(AngelToCoor(myTrack.designDic[i]))