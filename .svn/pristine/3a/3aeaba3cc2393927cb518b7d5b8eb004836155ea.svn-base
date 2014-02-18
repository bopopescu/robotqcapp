
from  numpy import *
import matplotlib.pyplot as plt
import textwrap
import drawTable
import sys ,os
lib_path = os.path.abspath(r'E:\Tamuz\Utils\RobotQAUtils')
sys.path.append(lib_path)
from Utils.RobotQAUtils.plateReader import *
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
col_len = 8


def printMeanGraph3DVolumes(dilutionStatistics,wellSpanIndex = 0):
    N = len(dilutionStatistics)
    manualMeans = plateReader.getManualMeansTupple(dilutionStatistics)
    robotMeans = plateReader.getRobotMeansTupple(dilutionStatistics,wellSpanIndex)
    #converting nans to zeros
    robotVariance = plateReader.getRobotVarTupple(dilutionStatistics)
    manualVariance = plateReader.getManualVarianceTupple(dilutionStatistics)
    robotDelta = plateReader.getRobotDeltaTupple(dilutionStatistics)
    manualDelta = plateReader.getManualDeltaTupple(dilutionStatistics)
    robotMin = plateReader.getRobotMinList(dilutionStatistics)
    manualMin = plateReader.getManualMinList(dilutionStatistics)
    width = 0.35       # the width of the bars
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    colorVolumes = plateReader.getExpVolumes(dilutionStatistics)
    #for c, z in zip(['r', 'g', 'b', 'y'], [30, 20, 10, 0]):
    for idx,vol in enumerate(colorVolumes):
        xs = range(N)
        xsForRobot = [x+width for x in range(N)]
        #get only the appropriate ys with the matching volume
        ys = []
        ysForRobot = []
        ysForManualDelta = []
        ysForRobotDelta = []
        bottomsForManualDelta = []
        bottomsForRobotDelta = []
        for d in dilutionStatistics:
            if vol == d.getManualColorVolume():
                ys.append(manualMeans[idx])
                ysForRobot.append(robotMeans[idx])
                ysForManualDelta.append(manualDelta[idx])
                ysForRobotDelta.append(robotDelta[idx])
                bottomsForManualDelta.append(manualMin[idx])
                bottomsForRobotDelta.append(robotMin[idx])
            else:
                ys.append(0)
                ysForRobot.append(0)
                ysForManualDelta.append(0)
                ysForRobotDelta.append(0)
                bottomsForManualDelta.append(0)
                bottomsForRobotDelta.append(0)
        cs = ['r'] * len(ys)
        csForRobot = ['y'] * len(ysForRobot)
        csForManualDelta=  ['b'] * len(ysForManualDelta)
        csForRobotDelta=  ['b'] * len(ysForRobotDelta)
        manualMeansBar =   ax.bar(xs, ys, zs=vol, zdir='y', color=cs,width=width,align='center')
        robotMeansBar =   ax.bar(xsForRobot, ysForRobot, zs=vol, zdir='y', color=csForRobot,width=width,align='center')
        manualDeltaBar =   ax.bar(xs, ysForManualDelta, zs=vol, zdir='y', color=csForManualDelta,width=0.1,bottom=bottomsForManualDelta,align='center')
        robotDeltaBar =   ax.bar(xsForRobot, ysForRobotDelta, zs=vol, zdir='y', color=csForRobotDelta,width=0.1,bottom=bottomsForRobotDelta,align='center')
    ax.set_title('a graph of manual and robot means reading and the delta betwin highest and lowest reading in each experiment.')
    red_proxy = plt.Rectangle((0, 0), 1, 1, fc="r")
    yellow_proxy = plt.Rectangle((0, 0), 1, 1, fc="y")
    blue_proxy = plt.Rectangle((0, 0), 1, 1, fc="b")
    ax.legend([red_proxy,yellow_proxy,blue_proxy,blue_proxy],['manual means','robot means','manual volume  delta','robot  voume delta'])
    ax.set_xlabel('X - expiriment number')
    ax.set_ylabel('Y - volume')
    ax.set_zlabel('Z - means')

    plt.show()






def printVarianceGraph(dilutionStatistics,wellSpanIndex = 0):
    N = len(dilutionStatistics)
    robotVar = plateReader.getRobotVarTupple(dilutionStatistics)
    manualVar = plateReader.getManualVarianceTupple(dilutionStatistics)
    width = 0.35       # the width of the bars
    fig = plt.figure()
    ax = fig.add_subplot(111)
    rects1 = ax.bar(range(N), robotVar, width, color='y',align='center')
    rects2 = ax.bar([x+width for x in range(N)], manualVar, width, color='r',align='center')
# add some
    ax.set_ylabel('Variance of robot  and manual')
    ax.set_xlabel('rows')
    ax.set_title('Variance  of robot and manual pipeting')
    #labels= getColumnsLabels(dilutionStatistics)
    ax.legend( (rects1[0], rects2[0]), ('Robot', 'Manual') )
    params = plateReader.getColumnsParams(dilutionStatistics)
    params =plateReader.cutStringsLength(params,15)
    rowLabels =plateReader.createRowLabels(len(params),'exp')
    rowLabels=[textwrap.fill(text,15) for text in rowLabels]
    plt.xticks(range(N),rowLabels)
    plt.show()


