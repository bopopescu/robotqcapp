import matplotlib.pyplot as plt
import sys
import os
import textwrap
#from TamuzApp.models import *
import gc
lib_path = os.path.abspath(r'E:\Tamuz\Utils\RobotQAUtils')
sys.path.append(lib_path)
from Utils.RobotQAUtils.plateReader import *
from  Utils.RobotQAUtils.classes import *
from Utils.DBUtil.FilesIO.saveFileToModel import *
from matplotlib.font_manager import FontProperties
width = 0.35
plt.ioff()
fig = None

def printPipetorsReport(dilutionStatistic):
    manualRead = dilutionStatistic.manualColumn.getMean()
    robotRead =dilutionStatistic.getRobotMean()
    N = len(dilutionStatistic.pipetors)
    means = []
    maxDeviation = []
    for p in dilutionStatistic.pipetors:
        means.append(p.getMeans())
        maxDeviation.append(p.getMaxDeviationPercent(robotRead))
    fig = plt.figure()
    #fig.subplots_adjust(right=0.75)
    ax = fig.add_subplot(111)
    #par1 = ax.twinx()
    #par1.spines["right"].set_position(("axes", float(1)))
    #make_patch_spines_invisible(par1)
    #par1.spines["right"].set_visible(True)
    #par1.set_ylim(0, 100)
    #ys1 =[manualRead]
    #ys1.extend([0]*N)
    #xs1 = range(N+1)
    #ys1[:] = [x*100 for x in ys1]
    #rects1 = ax.bar(xs1,ys1, width, color='g',align='center')
    ys2 = [0]
    ys2.extend(means)
    #ys2[:] = [x*100 for x in ys2]
    rects2 = ax.bar(xs1, ys2, width, color='y',align='center')
    ys3 = [dilutionStatistic.manualColumn.getMaxDeviationPercent(manualRead)]
    ys3.extend(maxDeviation)
    xs3 = [x+width for x in range(N+1)]
    #ys3[:] = [x/10.0 for x in ys3]
    for idx,dev in enumerate(ys3):# normalize deviation values of the deviation percent to the size of manual reading
        ys3[idx] = float(robotRead)*float(ys3[idx])
    rects3 = ax.bar(xs3, ys3, width, color='r',align='center')
    #rects4 = ax.bar([x+width for x in range(N)], deviationPercentDown, 0.1, color='b',align='center')
    for i, w in enumerate(dilutionStatistic.pipetors[0].wells):
        dils = []
        dils.append(dilutionStatistic.manualColumn.wells[i].dilutionValue)
        for  p in dilutionStatistic.pipetors:
            dils.append(p.wells[i].dilutionValue)
        #dils[:] = [x*100 for x in dils]
        p=plt.plot(range(N+1),dils, 'ro', label='dilution values')
    ax.set_ylabel('reading')
    ax.set_xlabel('pipetors')
    ax.set_title('readings  and volume of pipetors with '+str(dilutionStatistic.manualColumn.colorVolume)+' volume')
    #labels= getColumnsLabels(dilutionStatistics)
    rowLabels = plateReader.createRowLabels(length =N+1,name = '')
    rowLabels.insert(0,'manual')
    rowLabels=[textwrap.fill(text,15) for text in rowLabels]
    rowLabels2 = []
    for ind, num in enumerate(ys3):
        n = round(num*100/robotRead)#unNormalize
        rowLabels2.append(str(n)+' %')
    plt.xticks(range(N+1),rowLabels)
    plt.xticks( [x+width for x in range(N+1)],rowLabels2)
    ax.legend( (rects1[0], rects2[0],rects3[0],p[0]), ('reading  in manual pipeting', 'reading in robot pipeting','maximum  deviation  percent','dilution values') )
    plt.show()

def printPipetorsCV(dilutionStatistic):
    manualRead = plateReader.getVolumeFromReading(dilutionStatistic.manualColumn.getMean())
    N = len(dilutionStatistic.pipetors)
    means = []
    cv = [plateReader.getCV(dilutionStatistic.manualColumn.wells,dilutionStatistic.manualColumn.getMean())]
    for p in dilutionStatistic.pipetors:
        means.append(plateReader.getVolumeFromReading(p.getMeans()))
        cv.append(plateReader.getCV(p.wells,p.getMeans()))
    #normalize all reads by manual read
    #for i,m in enumerate(means):
     #   means[i] = plateReader.normalizeVolumeByManualRead(manualVolume=manualRead,volumeSupposeToBe =dilutionStatistic.manualColumn.colorVolume,actualVolume=m)
    #manualRead = dilutionStatistic.manualColumn.colorVolume
    fig = plt.figure()
    ax = fig.subplot()
    ys1 =[manualRead]
    ys1.extend([0]*N)
    xs1 = range(N+1)
    rects1 = ax.bar(xs1,ys1, width, color='g',align='center')
    ys2 = [0]
    ys2.extend(means)
    rects2 = ax.bar(xs1, ys2, width, color='y',align='center')
    #ys3 = [plateReader.getCV(dilutionStatistic.manualColumn.wells,dilutionStatistic.manualColumn.getMean())]
    ys3=cv
    xs3 = [x+width for x in range(N+1)]
    #for idx,c in enumerate(ys3):
     #   ys3[idx] = float(100*robotRead)*float(ys3[idx])
    rects3 = ax.bar(xs3, ys3, width, color='r',align='center')
    #rects4 = ax.bar([x+width for x in range(N)], deviationPercentDown, 0.1, color='b',align='center')
    manvol =plateReader.getVolumeFromReading(dilutionStatistic.manualColumn.getMean())
    volsupposeToBe = dilutionStatistic.manualColumn.colorVolume
    normVal =volsupposeToBe - manvol
    for i, w in enumerate(dilutionStatistic.pipetors[0].wells):
        manvol =plateReader.getVolumeFromReading(dilutionStatistic.manualColumn.getMean())
        volsupposeToBe = dilutionStatistic.manualColumn.colorVolume
        normVal =volsupposeToBe - manvol
        dils = []
        dils.append(plateReader.getVolumeFromReading(dilutionStatistic.manualColumn.wells[i].dilutionValue))
        #dils.append(plateReader.getVolumeFromReading(dilutionStatistic.manualColumn.wells[i].dilutionValue))
        for  j,p in enumerate(dilutionStatistic.pipetors):
            robvol =means[j]
            volsupposeToBe = dilutionStatistic.manualColumn.colorVolume
            normVal =volsupposeToBe - robvol
            dils.append(plateReader.getVolumeFromReading(p.wells[i].dilutionValue))
            #dils.append(plateReader.getVolumeFromReading(p.wells[i].dilutionValue))
        p=plt.plot(range(N+1),dils, 'ro', label='dilution values')
    ax.set_ylabel('volume')
    ax.set_xlabel('pipetors')
    ax.set_title('readings  and volume of pipetors with '+str(dilutionStatistic.manualColumn.colorVolume)+' volume')
    #labels= getColumnsLabels(dilutionStatistics)
    rowLabels = plateReader.createRowLabels(length =N+1,name = '')
    rowLabels.insert(0,'manual')
    rowLabels=[textwrap.fill(text,15) for text in rowLabels]
    rowLabels2 = []
    for ind, num in enumerate(ys3):
       # n = round(num/robotRead)#unNormalize
        rowLabels2.append(str(round(num*100)))
    plt.xticks(range(N+1),rowLabels)
    plt.xticks( [x+width for x in range(N+1)],rowLabels2)
    ax.legend( ( rects2[0],rects3[0],p[0]), ( 'reading in robot pipeting','cv value','dilution values'))
    plt.show()


def printPipetorsCVForWebbApp(robotExperiment,manualExcelFile,exp = None,plateReaderUsed = 'old'):
    global fig
    manualRead = plateReader.getVolumeFromReading(robotExperiment.getPlateODMean(robotExperiment.manualPlate),plateReaderUsed)
    N = len(robotExperiment.pipetors)
    means = []
    manualWellList = []
    for col in robotExperiment.manualPlate.columns:
        manualWellList.extend(col.wells)
    cv = [plateReader.getCV(manualWellList,robotExperiment.getPlateODMean(robotExperiment.manualPlate))]
    for p in robotExperiment.pipetors:
        means.append(plateReader.getVolumeFromReading(p.getMeans()))
        cv.append(plateReader.getCV(p.wells,p.getMeans()))
    if not fig:
        fig = plt.figure()
    ax = fig.add_subplot(111)
    #ax = plt.subplot()
    ys1 =[manualRead]
    ys1.extend([0]*N)
    xs1 = range(N+1)
    rects1 = plt.bar(xs1,ys1, width, color='g',align='center')
    ys2 = [0]
    ys2.extend(means)
    rects2 = plt.bar(xs1, ys2, width, color='y',align='center')
    #ys3 = [plateReader.getCV(dilutionStatistic.manualColumn.wells,dilutionStatistic.manualColumn.getMean())]
    ys3=cv
    xs3 = [x+width for x in range(N+1)]
    rects3 = plt.bar(xs3, ys3, width, color='r',align='center')
    for i, w in enumerate(robotExperiment.pipetors[0].wells):
        dils = []
        if i < len(manualWellList):
            dils.append(plateReader.getVolumeFromReading(manualWellList[i].dilutionValue))
        else:
            dils.append(manualRead)
        for  j,p in enumerate(robotExperiment.pipetors):
            dils.append(plateReader.getVolumeFromReading(p.wells[i].dilutionValue))
        p=plt.plot(range(N+1),dils, 'ro', label='dilution values')
    plt.ylabel('volume')
    plt.xlabel('pipetors')
    plt.title('readings  and volume of pipetors with '+str(robotExperiment.volume)+' volume')
    rowLabels = plateReader.createRowLabels(length =N+1,name = '')
    rowLabels.insert(0,'manual')
    rowLabels=[textwrap.fill(text,15) for text in rowLabels]
    rowLabels2 = []
    for ind, num in enumerate(ys3):
    # n = round(num/robotRead)#unNormalize
        rowLabels2.append(str(round(num*100)))
    plt.xticks(range(N+1),rowLabels)
    plt.xticks( [x+width for x in range(N+1)],rowLabels2)
    plt.legend( ( rects2[0],rects3[0],p[0]), ( 'reading in robot pipeting','cv value','dilution values'),bbox_to_anchor=(1, 0.5))
    dir = getFileDir(str(manualExcelFile))
    plt.savefig(dir+'/report.png',dpi=600)
    saveFileToModel(exp,dir,'report.png',key = 'report1')
    plt.close(fig)
    plt.cla()
    plt.clf()
    gc.collect()
    return dir+'report.png'
#    plt.show()

def printSingleWellsPipetors(robotExperiment,manualExcelFile,exp = None,plateReaderUsed = 'old'):
    global fig
    manualWellList = []
    for col in robotExperiment.manualPlate.columns:
        manualWellList.extend(col.wells)
    if not fig:
        fig = plt.figure()
    ax = fig.add_subplot(110)
    #ax = plt.subplot()
    matrix = []
    ps = []
    for i,p in enumerate(robotExperiment.pipetors):
        matrix.append([])
        for w in p.wells:#iterating each pipotor's well list
            matrix[i].append(plateReader.getVolumeFromReading(w.dilutionValue,plateReaderUsed))
        ps.append(plt.plot(range(len(matrix[i])),matrix[i], '-',label='p'+str(i+1)))
    ax.set_ylabel('volume')
    #plt.ylabel('volume')
    #plt.xlabel('wells')
    ax.set_xlabel('wells')
    ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), mode="expand", borderaxespad=0.,loc=3,ncol=8)
    #plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), mode="expand", borderaxespad=0.,loc=3,ncol=8)
    dir = getFileDir(str(manualExcelFile))
    #fig.savefig(dir+'/pipetorsReport.png')
    plt.savefig(dir+'/pipetorsReport.png')
    saveFileToModel(exp,dir,'pipetorsReport.png',key = 'report2')
    plt.close(fig)
    plt.cla()
    plt.clf()
    gc.collect()
    return dir+'pipetorsReport.png'
