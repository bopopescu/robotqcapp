
from  numpy import *
import matplotlib.pyplot as plt
import textwrap
import drawTable
import sys ,os
lib_path = os.path.abspath(r'E:\Tamuz\Utils\RobotQAUtils')
sys.path.append(lib_path)
#import plateReader
from Utils.RobotQAUtils.plateReader import *
col_len = 8


def printMeanGraph(dilutionStatistics,wellSpanIndex = 0):
    N = len(dilutionStatistics)
    manualMeans = plateReader.getManualMeansTupple(dilutionStatistics)
    robotMeans = plateReader.getRobotMeansTupple(dilutionStatistics,wellSpanIndex)
    robotVariance = plateReader.getRobotVarTupple(dilutionStatistics)
    manualVariance = plateReader.getManualVarianceTupple(dilutionStatistics)
    robotDelta = plateReader.getRobotDeltaTupple(dilutionStatistics)
    manualDelta = plateReader.getManualDeltaTupple(dilutionStatistics)
    robotMin = plateReader.getRobotMinList(dilutionStatistics)
    manualMin = plateReader.getManualMinList(dilutionStatistics)
    width = 0.35       # the width of the bars
    fig = plt.figure()
    ax = fig.add_subplot(111)
    rects1 = ax.bar(range(N), manualMeans, width, color='r',align='center',yerr=manualVariance)
    rects2 = ax.bar([x+width for x in range(N)], robotMeans, width, color='y',align='center',yerr=robotVariance)
    rects3 = ax.bar(range(N), manualDelta, 0.1, color='b',align='center',bottom=manualMin)
    rects4 = ax.bar([x+width for x in range(N)], robotDelta, 0.1, color='b',align='center',bottom=robotMin)
# add some
    ax.set_ylabel('Means')
    ax.set_xlabel('expiriments')
    ax.set_title('Means  of robot and manual pipeting')
    #labels= getColumnsLabels(dilutionStatistics)
    ax.legend( (rects1[0], rects2[0],rects3[0],rects4[0]), ('Manual mean', 'Robot mean', 'manual Delta','Robot Delta') )
    params = plateReader.getColumnsParams(dilutionStatistics)
    params =plateReader.cutStringsLength(params,15)
    rowLabels =plateReader.createRowLabels(len(params),'exp')
    rowLabels=[textwrap.fill(text,15) for text in rowLabels]
    plt.xticks(range(N),rowLabels)
    colLabels = ['volume','liquid class','labware type','scriptType']
    drawTable.printLegend(rowLabels,colLabels,params)
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