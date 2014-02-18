import textwrap
import sys
import os
import matplotlib.pyplot as plt
lib_path = os.path.abspath(r'E:\Tamuz\Utils\RobotQAUtils')
sys.path.append(lib_path)
from Utils.RobotQAUtils.plateReader import *
from Utils.RobotQAUtils.classes  import *
width = 0.35
def printRobotDeviationPercents(robotDeviationPercentTuppleUp,robotDeviationPercentTuppleDown,title = None):
    width = 0.35
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax1 = fig.add_subplot(111)
    rowLabels =plateReader.createRowLabels(len(robotDeviationPercentTuppleUp),'exp')
    rowLabels=[textwrap.fill(text,15) for text in rowLabels]
    plt.xticks(range(len(robotDeviationPercentTuppleUp)),rowLabels)
    rects1 = ax.bar(range(len(robotDeviationPercentTuppleUp)), robotDeviationPercentTuppleUp, width, color='y',align='center')
    rects2 = ax.bar([x+width for x in range(len(robotDeviationPercentTuppleDown))], robotDeviationPercentTuppleDown, width, color='r',align='center')
    ax.set_ylabel('percent')
    ax.set_xlabel('expiriments')
    if not title:
        ax.set_title('deviation percent')
    else:
        ax.set_title(title)
    ax.legend( (rects1[0], rects2[0]), ('up', 'down') )
    plt.show()
def printRobotDeviationPercentsLiquidClass3D(robotDeviationPercentTuppleUp,robotDeviationPercentTuppleDown,title = None ,ds=None,legendLabels = None):
    '''
     X: prints the expiriment number
     Y: prints the liquid class name
     Z: prints the average of the deviation percents above robot mean and below robot mean. prints the volume as well'''
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    liquidClasses = plateReader.getExpLiquidClasses(ds)
    #remove duplicates from liquid classes
    newLiquidClasses = []
    for c in liquidClasses:
        if c not in newLiquidClasses:
            newLiquidClasses.append(c)
    liquidClasses = newLiquidClasses
    rowLabels =plateReader.createRowLabels(len(robotDeviationPercentTuppleUp),'')
    rowLabels=[textwrap.fill(text,15) for text in rowLabels]
    plt.xticks(range(len(robotDeviationPercentTuppleUp)),rowLabels)
    yLabels = []
    for idx,l in enumerate(liquidClasses):# iterating through all liquid classes
        #creating labels for y axis
        xsUp = range(len(robotDeviationPercentTuppleUp))
        xsDown = [x+width for x in range(len(robotDeviationPercentTuppleDown))]
        xsVol = [x+width+0.2 for x in range(len(robotDeviationPercentTuppleDown))]
        ysUp = []
        ysDown = []
        ysVol = []
        for i, d in enumerate(ds):#iterating through all expiriments to see which has the same liquid class as l.
            if l == d.getLiquidClass():
                ysUp.append(robotDeviationPercentTuppleUp[i])
                ysDown.append(robotDeviationPercentTuppleDown[i])
                ysVol.append(d.getManualColorVolume())#appending the volume of the liquid class to shows in the bar
            else:
                ysUp.append(0)
                ysDown.append(0)
                ysVol.append(0)
        csUp = ['r'] * len(ysUp)
        csDown = ['y'] * len(ysDown)
        csVol = ['b']*len(ysVol)
        upBar =   ax.bar(xsUp, ysUp, zs=idx, zdir='y', color=csUp,width=width,align='center')
        downBar =   ax.bar(xsDown, ysDown, zs=idx, zdir='y', color=csDown,width=width,align='center')
        volumeBar =   ax.bar(xsVol, ysVol, zs=idx, zdir='y', color=csVol,width=0.1,align='center')
        ax.set_xlabel('X - expiriment number')
        ax.set_ylabel('Y - liquid class')
        ax.set_zlabel('Z - deviation + volume')
    if not title:
        ax.set_title('deviation percent')
    else:
        ax.set_title(title)
    red_proxy = plt.Rectangle((0, 0), 1, 1, fc="r")
    yellow_proxy = plt.Rectangle((0, 0), 1, 1, fc="y")
    blue_proxy = plt.Rectangle((0, 0), 1, 1, fc="b")
    if legendLabels is None:
        ax.legend([red_proxy,yellow_proxy,blue_proxy],['deviation percent  above average','deviation percent below average','volume of color in exp'])
    else:
        ax.legend([red_proxy,yellow_proxy,blue_proxy],legendLabels)
    yLabels=[textwrap.fill(text,15) for text in liquidClasses]
    plt.yticks(range(len(yLabels)),yLabels)
def printRobotCompareToManualDeviationPercentsLiquidClass3D(robotDeviationPercentTupple,manualDeviationPercentTupple,title = None ,ds=None , legendRectangles = None,legendLabels = None):
    '''
    gets a tupple of robot deviation percents average, manual deviation percents average and a list of dilutionStatistics at the same order of the tupples.
     X: prints the expiriment number
     Y: prints the liquid class name
     Z: prints the average of the deviation percents of the robot  and the deviation percents of the hand. prints the volume as well'''
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    liquidClasses = plateReader.getExpLiquidClasses(ds)
    #remove duplicates from liquid classes
    newLiquidClasses = []
    for c in liquidClasses:
        if c not in newLiquidClasses:
            newLiquidClasses.append(c)
    liquidClasses = newLiquidClasses
    rowLabels =plateReader.createRowLabels(len(robotDeviationPercentTuppleUp),'')
    rowLabels=[textwrap.fill(text,15) for text in rowLabels]
    plt.xticks(range(len(robotDeviationPercentTuppleUp)),rowLabels)
    yLabels = []
    for idx,l in enumerate(liquidClasses):# iterating through all liquid classes
        #creating labels for y axis
        xsUp = range(len(robotDeviationPercentTuppleUp))
        xsDown = [x+width for x in range(len(robotDeviationPercentTuppleDown))]
        xsVol = [x+width+0.2 for x in range(len(robotDeviationPercentTuppleDown))]
        ysUp = []
        ysDown = []
        ysVol = []
        for i, d in enumerate(ds):#iterating through all expiriments to see which has the same liquid class as l.
            if l == d.getLiquidClass():
                ysUp.append(robotDeviationPercentTuppleUp[i])
                ysDown.append(robotDeviationPercentTuppleDown[i])
                ysVol.append(d.getManualColorVolume())#appending the volume of the liquid class to shows in the bar
            else:
                ysUp.append(0)
                ysDown.append(0)
                ysVol.append(0)
        csUp = ['r'] * len(ysUp)
        csDown = ['y'] * len(ysDown)
        csVol = ['b']*len(ysVol)
        upBar =   ax.bar(xsUp, ysUp, zs=idx, zdir='y', color=csUp,width=width,align='center')
        downBar =   ax.bar(xsDown, ysDown, zs=idx, zdir='y', color=csDown,width=width,align='center')
        volumeBar =   ax.bar(xsVol, ysVol, zs=idx, zdir='y', color=csVol,width=0.1,align='center')
        ax.set_xlabel('X - expiriment number')
        ax.set_ylabel('Y - liquid class')
        ax.set_zlabel('Z - deviation + volume')
    if not title:
        ax.set_title('deviation percent')
    else:
        ax.set_title(title)
    red_proxy = plt.Rectangle((0, 0), 1, 1, fc="r")
    yellow_proxy = plt.Rectangle((0, 0), 1, 1, fc="y")
    blue_proxy = plt.Rectangle((0, 0), 1, 1, fc="b")
    if legendLabels is None:
        ax.legend([red_proxy,yellow_proxy,blue_proxy],['deviation percent  above average','deviation percent below average','volume of color in exp'])
    else:
        ax.legend([red_proxy,yellow_proxy,blue_proxy],legendLabels)
    yLabels=[textwrap.fill(text,15) for text in liquidClasses]
    plt.yticks(range(len(yLabels)),yLabels)
def printRobotDeviationPercentsVolume3D(robotDeviationPercentTuppleUp,robotDeviationPercentTuppleDown,title = None ,ds=None):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    rowLabels =plateReader.createRowLabels(len(robotDeviationPercentTuppleUp),'')
    rowLabels=[textwrap.fill(text,15) for text in rowLabels]
    plt.xticks(range(len(robotDeviationPercentTuppleUp)),rowLabels)
    colorVolumes = plateReader.getExpVolumes(ds)
    for idx,vol in enumerate(colorVolumes):
        xsUp = range(len(robotDeviationPercentTuppleUp))
        xsDown = [x+width for x in range(len(robotDeviationPercentTuppleDown))]
        ysUp = []
        ysDown = []
        for i, d in enumerate(ds):
            if vol == d.getManualColorVolume():
                ysUp.append(robotDeviationPercentTuppleUp[i])
                ysDown.append(robotDeviationPercentTuppleDown[i])
            else:
                ysUp.append(0)
                ysDown.append(0)
        csUp = ['r'] * len(ysUp)
        csDown = ['y'] * len(ysDown)
        upBar =   ax.bar(xsUp, ysUp, zs=vol, zdir='y', color=csUp,width=width,align='center')
        downBar =   ax.bar(xsDown, ysDown, zs=vol, zdir='y', color=csDown,width=width,align='center')
    ax.set_xlabel('X - expiriment number')
    ax.set_ylabel('Y - volume')
    ax.set_zlabel('Z - deviation')
    if not title:
        ax.set_title('deviation percent')
    else:
        ax.set_title(title)
    red_proxy = plt.Rectangle((0, 0), 1, 1, fc="r")
    yellow_proxy = plt.Rectangle((0, 0), 1, 1, fc="y")
    blue_proxy = plt.Rectangle((0, 0), 1, 1, fc="b")
    ax.legend([red_proxy,yellow_proxy],['deviation percent  above average','deviation percent below average'])
