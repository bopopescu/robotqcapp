import textwrap
import sys
import os
import matplotlib.pyplot as plt

lib_path = os.path.abspath(r'E:\Tamuz\Utils\RobotQAUtils')
sys.path.append(lib_path)
from Utils.RobotQAUtils.plateReader import *
tinyNum =  0.000001
def printUniqueWellsHistogramCompare(robotVals = None,manualVals=None,labels = None,ds = None,title = None):
    '''for each expiriment prints a rectangle  of percent of wells deviating 20 percent  or more  then the mean.
    the mean is calculated for robot and manual seperatly'''
    width = 0.35
    fig = plt.figure()
    ax = fig.add_subplot(111)
    nRobot = getUniqueWellsPercentList(robotVals,ds,man = False)
    nManual = getUniqueWellsPercentList(manualVals,ds ,man=True)
    rowLabels =plateReader.createRowLabels(len(nRobot),'exp')
    rowLabels=[textwrap.fill(text,15) for text in rowLabels]
    plt.xticks(range(len(nRobot)),rowLabels)
    rects1 = ax.bar(range(len(nRobot)), nRobot, width, color='y',align='center')
    rects2 = ax.bar([x+width for x in range(len(nManual))], nManual, width, color='r',align='center')
    ax.set_ylabel('percent of unique wells')
    ax.set_xlabel('expiriments')
    if not title:
        ax.set_title('unique  wells count of robot and manual pipeting more then 20%')
    else:
        ax.set_title(title)
    ax.legend( (rects1[0], rects2[0]), ('Robot uniqe wells', 'Manual Unique wells') )
    plt.show()

def getUniqueWellsPercentList(wellsIndexes,ds , man = False):
    '''gets a list of indexes  in the ds list of unique wells and a list of dilutinStatistics and returns a list of deviation percent.
    each value in the list contains (number of unique wells for the expiriment/number of wells in the expiriment)*100'''
    #populating the list with unique wells count
    res = []
    for d in ds:
        res.append(0)
    for num in wellsIndexes:
        res[num]+=1
    #taking care of the edges of the list to have some value above zero
    for idx,d in enumerate(ds):
        if man and d.getManualWellsCount() > 0:
            res[idx] = (res[idx]/d.getManualWellsCount())*100 # getting the manual percent
        elif man:
            res[idx] = 0
        elif not man and d.getRobotWellsCount() >0:
            res[idx] = (float(res[idx])/float(d.getRobotWellsCount()))*100 # getting the robot percent
        else:
            res[idx] = 0
    if not  res[0]:
        res[0] =tinyNum
    if not  res[len(res)-1]:
        res[len(res)-1] =tinyNum
    return res

def printUniqueWellsHistogramCompareVolumes3D(robotVals = None,manualVals=None,labels = None,ds = None,title = None):
    '''for each expiriment prints a rectangle  of percent of wells deviating 20 percent  or more  then the mean.
    the mean is calculated for robot and manual seperatly'''
    width = 0.35
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    colorVolumes = plateReader.getExpVolumes(ds)
    for idx,vol in enumerate(colorVolumes):
        nRobot = getUniqueWellsPercentList(robotVals,ds,man = False)
        nManual = getUniqueWellsPercentList(manualVals,ds ,man=True)
        rowLabels =plateReader.createRowLabels(len(nRobot),'exp')
        rowLabels=[textwrap.fill(text,15) for text in rowLabels]
        plt.xticks(range(len(nRobot)),rowLabels)
        manualYs = []
        robotYs = []
        xs = range(len(nRobot))
        for idx, d in enumerate(ds):
            if vol == d.getManualColorVolume():
                manualYs.append(nManual[idx])
                robotYs.append(nRobot[idx])
            else:
                manualYs.append(0)
                robotYs.append(0)
        csForManual = ['r'] * len(manualYs)
        csForRobot = ['y'] * len(robotYs)
        manualBar =   ax.bar(xs, manualYs, zs=vol, zdir='y', color=csForManual,width=width,align='center')
        robotBar =   ax.bar(xs, robotYs, zs=vol, zdir='y', color=csForRobot,width=width,align='center')
    ax.set_ylabel('percent of unique wells')
    ax.set_xlabel('expiriments')
    if not title:
        ax.set_title('unique  wells count of robot and manual pipeting more then 20%')
    else:
        ax.set_title(title)
    red_proxy = plt.Rectangle((0, 0), 1, 1, fc="r")
    yellow_proxy = plt.Rectangle((0, 0), 1, 1, fc="y")
    ax.legend([red_proxy,yellow_proxy],['manual unique wells percent','robot unique wells percent'])
    ax.set_xlabel('X - expiriment number')
    ax.set_ylabel('Y - volume')
    ax.set_zlabel('Z - unique wells percent')
    plt.show()
def printUniqueWellsHistogramCompareLiquidClass3D(robotVals = None,manualVals=None,labels = None,ds = None,title = None):
    '''for each expiriment prints a rectangle  of percent of wells deviating 20 percent  or more  then the mean.
    the mean is calculated for robot and manual seperatly'''
    width = 0.35
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    colorVolumes = plateReader.getExpVolumes(ds)
    for idx,vol in enumerate(colorVolumes):
        nRobot = getUniqueWellsPercentList(robotVals,ds,man = False)
        nManual = getUniqueWellsPercentList(manualVals,ds ,man=True)
        rowLabels =plateReader.createRowLabels(len(nRobot),'')
        rowLabels=[textwrap.fill(text,15) for text in rowLabels]
        plt.xticks(range(len(nRobot)),rowLabels)
        manualYs = []
        manualZeroYs=[]
        robotYs = []
        robotZeroYs = []
        xs = range(len(nRobot))
        for i, d in enumerate(ds):
            if vol == d.getManualColorVolume():
                manualYs.append(nManual[i])
                robotYs.append(nRobot[i])
                if  nManual[i] < 1:
                    manualZeroYs.append(5)
                else:
                    manualZeroYs.append(0)
                if nRobot[i] < 1:
                    robotZeroYs.append(5)
                else:
                    robotZeroYs.append(0)
            else:
                manualYs.append(0)
                robotYs.append(0)
                manualZeroYs.append(0)
                robotZeroYs.append(0)
        csForManual = ['r'] * len(manualYs)
        csForRobot = ['y'] * len(robotYs)
        csForZeroManual = ['b'] * len(manualYs)
        csForZeroRobot = ['g'] * len(robotYs)
        manualBar =   ax.bar(xs, manualYs, zs=vol, zdir='y', color=csForManual,width=width,align='center')
        robotBar =   ax.bar( [x+width for x in range(len(xs))], robotYs, zs=vol, zdir='y', color=csForRobot,width=width,align='center')
        manualZeroBar =   ax.bar(xs, manualZeroYs, zs=vol, zdir='y', color=csForZeroManual,width=width,align='center')
        robotZeroBar =   ax.bar( [x+width for x in range(len(xs))], robotZeroYs, zs=vol, zdir='y', color=csForZeroRobot,width=width,align='center')
    ax.set_ylabel('percent of unique wells')
    ax.set_xlabel('expiriments')
    if not title:
        ax.set_title('unique  wells count of robot and manual pipeting more then 20%')
    else:
        ax.set_title(title)
    red_proxy = plt.Rectangle((0, 0), 1, 1, fc="r")
    yellow_proxy = plt.Rectangle((0, 0), 1, 1, fc="y")
    blue_proxy =  plt.Rectangle((0, 0), 1, 1, fc="b")
    green_proxy =  plt.Rectangle((0, 0), 1, 1, fc="g")
    ax.legend([red_proxy,yellow_proxy,blue_proxy,green_proxy],['manual unique wells percent','robot unique wells percent','manual zero values','robot zero values'])
    ax.set_xlabel('X - expiriment number')
    ax.set_ylabel('Y - volume')
    ax.set_zlabel('Z - unique wells percent')
    plt.show()