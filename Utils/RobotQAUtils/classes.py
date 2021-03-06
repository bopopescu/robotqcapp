import xlrd
#from  numpy import *
from math import fabs
col_len = 8
import sys ,os
lib_path = os.path.abspath(r'E:\Tamuz\Utils\RobotQAUtils')
sys.path.append(lib_path)
import plateReader
import warnings
diffThreshold = 1.2
import copy

class Well(object):
    def __init__(self,_x,_y,_dilutionValue = None):
        self.x = _x
        self.y = _y
        if type(_dilutionValue) is unicode:
            self.dilutionValue =float( _dilutionValue.rstrip('\n'))
        elif type(_dilutionValue) is float:
            self.dilutionValue = _dilutionValue
    def printWell(self):
        print 'x='+str(self.x)
        print 'y='+str(self.y)
        print 'dilution value='+str(self.dilutionValue)
    def getIndex(self):
        return col_len*(self.x-1) + self.y
class Column(object):
    def __init__(self, _wells):
        self.wells= _wells
    def printCol(self):
        for well in self.wells:
            well.printWell()
    def getVariance(self):
        dils = self.getDilsList()
        a = array(dils)
        res = a.var()
        return res
    def getMean(self):
        dils = self.getDilsList()
        a = array(dils)
        res = a.mean()
        return res
    def getDilsList(self):
        dils = []
        for well in self.wells:
            dil = well.dilutionValue
            if not isnan(dil):
                dils.append(dil)
            else:
                dils.append(0)
        return dils
    def getUniqueWell(self):
        mean = self.getMean()
        maxDiff = 0
        resWell = None
        for well in self.wells:
            if fabs(mean - well.dilutionValue) > maxDiff:
                maxDiff =  fabs(mean - well.dilutionValue)
                resWell = well
        return resWell
    def getColUniqueWellsCompareToOutsideMean(self,outSideMean):
        maxDiff = outSideMean*diffThreshold - outSideMean
        resWells = []
        for well in self.wells:
            if fabs(outSideMean - well.dilutionValue) > maxDiff:
                maxDiff =  fabs(outSideMean - well.dilutionValue)
                resWells.append(well)
        return resWells
    def getDeviationPercent(self,mean):
        sum = 0.0
        for well in self.wells:
            sum += abs(well.dilutionValue - mean)
        res = float(sum)/float(len(self.wells))
        return res
    def getMaxDeviationPercent(self,mean):
        max = 0.0
        for well in self.wells:
            r = abs((mean -well.dilutionValue)/mean)
            if r > max:
                max = r
        return max
class ManualColumn(Column):
    def __init__(self, _wells, _dilute,_colorVolume = None,_liquidClass = None, _labwareType = None, _scriptType = None, _robotPlateName =None):
        Column.__init__(self,_wells)
        self.dilute = _dilute
        self.colorVolume = _colorVolume
        self.liquidClass = _liquidClass
        self.labwareType = _labwareType
        self.scriptType = _scriptType
        self.robotPlateName = _robotPlateName
    def getColorVolume(self):
        return self.colorVolume
    def printCol(self):
        print 'dilute = '+str(self.dilute)
        print 'color Volume ='+str(self.colorVolume)
        print 'liquid class ='+str(self.liquidClass)
        print 'labware type ='+str(self.labwareType)
        print 'script type ='+str(self.scriptType)
        super(ManualColumn,self).printCol()
    def getDilSupposeToBe(self):
        return self.dilute
    def getParams(self):
        res = []
        res.append(str(self.colorVolume))
        res.append( str(self.liquidClass))
        res.append(str(self.labwareType))
        res.append(str(self.scriptType))
        return res
class Plate:
    def __init__(self,_columns,_xlsSheet=None):
        self.xlsSheet = _xlsSheet
        self.columns = _columns
class WellsSpan:
    '''holds the path to the plate file and the range of relevant wells'''
    def __init__(self,_pathToPlateFile,_firstWell,_lastWell,_waterPlate):
        self.pathToPlateFile=_pathToPlateFile
        self.firstWell = _firstWell
        self.lastWell = _lastWell
        self.columns = []
        self.waterPlate = _waterPlate
        self.createColumns()
    def createColumns(self):
        try:
            wb = xlrd.open_workbook(self.pathToPlateFile)
            worksheets = wb.sheet_names()
            for worksheet_name  in worksheets:
                sh = wb.sheet_by_name(worksheet_name)
                break
            for i in  range(self.firstWell.x,self.lastWell.x + 1):#for each column in plate file
                col = plateReader.loadColumn(i,sh)
               # if self.waterPlate:
               #     col = plateReader.decreaseWaterFromCol(col,i,self.waterPlate)
                self.columns.append(col)
        except Exception as e:
            print 'from WellSpan.createColumns:'+str(e)+'\n'
class Pipetor:
    def __init__(self,_wells = [],_id = 0):
        self.wells = _wells
        self.id=_id
    def getMeans(self):
        sum = 0
        count = 0
        res = 0
        for w in self.wells:
            try:
                sum+=float(w.dilutionValue)
                count+=1
            except:
                pass
        if count:
            res =  float(sum)/float(count)
        else:
            res = 0
        return res


    def getAverageDeviationAboveZero(self,manualRead):
        sum = 0.0
        wellsCount = 0
        res = 0
        for w in self.wells:
            if w.dilutionValue >= manualRead:
               sum += w.dilutionValue-manualRead
               wellsCount+=1
        if wellsCount:
            res =  (float(sum)/float(wellsCount))
        return res
    def getAverageDeviationPercent(self,manualRead):
        sum = 0.0
        for w in self.wells:
            sum += abs(w.dilutionValue-manualRead)
        res = 100*(float(sum)/float(len(self.wells)))
        return res
    def getMaxDeviationPercent(self,read):
        max = 0.0
        for w in self.wells:
            r = abs((read-w.dilutionValue)/read)
            if r > max:
                max = r
        return max
    def getAverageDeviationBelowZero(self,manualRead):
        sum = 0.0
        wellsCount = 0
        res = 0
        for w in self.wells:
            if w.dilutionValue < manualRead:
                sum += w.dilutionValue-manualRead
                wellsCount+=1
        if wellsCount:
            res = -1*(float(sum)/float(wellsCount))
        return res
class DilutionStatistic:
    def __init__(self,_manualColumn,_wellSpans,_id = None,_name = None):
        self.manualColumn = _manualColumn
        self.wellSpans = _wellSpans
        self.id = _id
        self.name = _name
        self.pipetors = []
    def  loadPipetors(self):
        for ws in self.wellSpans:
            for i,col in enumerate(ws.columns):
                for j,well in enumerate(col.wells):
                    if not i:
                            p = Pipetor()
                            p.id = j
                            p.wells = []
                            p.wells.append(well)
                            self.pipetors.append(p)
                    else:
                        (self.pipetors[j]).wells.append(well)
    def getManualWellsCount(self):
        res = 0
        for well in self.manualColumn.wells:
            res+=1
        return res
    def getRobotWellsCount(self):
        res = 0
        for w in self.wellSpans:
            for c in w.columns:
                for well in c.wells:
                    res+=1
        return res
    def printVariants(self):
        mv = self.manualColumn.getVariance()
        mm = self.manualColumn.getMean()
        print 'manual variance = '+ str(mv)
        print 'manual mean = '+str(mm)
        print 'manual dilution suppose to be value= '+str(self.manualColumn.getDilSupposeToBe())
        for w in self.wellSpans:
            for col in w.columns:
                rv = col.getVariance()
                rm = col.getMean()
                print 'robot variance='+str(rv)
                print 'robot mean='+str(rm)
    def getRobotDelta(self,wellSpanIndex=0):
        wells =[]
        try:
            w = self.wellSpans[wellSpanIndex]
            for col in w.columns:
                wells.extend(col.wells)
            minVal = plateReader.getMinWell(wells)
            maxVal = plateReader.getMaxWell(wells)
            res = maxVal - minVal
        except Exception as e :
            print 'from DilutionStatistic.getRobotDelta: '+e.message
            res = 0
        return res
    def getRobotMin(self,wellSpanIndex=0):
        wells =[]
        try:
            w = self.wellSpans[wellSpanIndex]
            for col in w.columns:
                wells.extend(col.wells)
            minVal = plateReader.getMinWell(wells)
            res =  minVal
        except Exception as e :
            print 'from DilutionStatistic.getRobotMin: '+e.message
            res = 0
        return res
    def getManualMin(self):
        wells = self.manualColumn.wells
        res = plateReader.getMinWell(wells)
        return res
    def getManualDelta(self,):
        wells = self.manualColumn.wells
        minVal = plateReader.getMinWell(wells)
        maxVal = plateReader.getMaxWell(wells)
        res = maxVal - minVal
        return res
    def getRobotMean(self,wellSpanIndex = 0):
        vals =[]
        try:
            w = self.wellSpans[wellSpanIndex]
            for col in w.columns:
                vals.extend(col.getDilsList())
        except Exception as e :
            print 'from DilutionStatistic.getRobotMean: '+e.message
            vals.append(0)
        with warnings.catch_warnings(record=True) as f:
            a = array(vals)
            res = a.mean()
        if len(f):
            pass
        if isnan(res):
            res=0
        return res
    def getManualMean(self):
        return self.manualColumn.getMean()
    def getManualVariance(self):
        return self.manualColumn.getVariance()
    def getRobotVariance(self):
        vals =[]
        for w in self.wellSpans:
            for col in w.columns:
                vals.extend(col.getDilsList())
        a = array(vals)
        res = a.var()
        return res
    def getUniqueWells(self):
        ''''returns all unique wells of the class. manual and robot.'''
        res = []
        res.append(self.manualColumn.getUniqueWell())
        for w in self.wellSpans:
            for col in w.columns:
                res.append(col.getUniqueWell())
        return res
    def getUniqueWellsCompareToOutsideMean(self,outsideMean,rob=False):
        '''returns a list of unique wells compare to outside means. if rob the robot wells. else, manual wells.'''
        res = []
        if not rob:
            res.extend(self.manualColumn.getColUniqueWellsCompareToOutsideMean(outsideMean))
        else:
            for w in self.wellSpans:
                for col in w.columns:
                    res.extend(col.getColUniqueWellsCompareToOutsideMean(outsideMean))
        return res
    def getUniqueWellsCompareToOutsideMeanPercent(self,outsideMean,rob=False):
        '''returns a list of unique wells compare to outside means. if rob the robot wells. else, manual wells.'''
        wellList = []
        if not rob:
            wellList.extend(self.manualColumn.getColUniqueWellsCompareToOutsideMean(outsideMean))
            res =  (float(len(wellList))/float(self.getManualWellsCount()))*100
        else:
            for w in self.wellSpans:
                for col in w.columns:
                    wellList.extend(col.getColUniqueWellsCompareToOutsideMean(outsideMean))
            res =  (float(len(wellList))/float(self.getRobotWellsCount()))*100
        return res
    def getUniqueWellsIndexes(self):
        wells = self.getUniqueWells()
        res = []
        for well in wells:
            res.append(well.y)
        return res
    def getUniqueWellsIndexesCompareToOutsideMean(self,outsideMean,rob = False):
        '''returns the number of times a unique well appears in an expiriment'''
        wells = self.getUniqueWellsCompareToOutsideMean(outsideMean,rob)
        res = []
        for well in wells:
            if well is not None:
                res.append(self.id)
        return res
    def getUniqueWellsMean(self):
        uniqueWells = self.getUniqueWells()
        vals = []
        for well in uniqueWells:
            vals.append(well.y)
        a = array(vals)
        res = a.mean
        return res
    def getManualColorVolume(self):
        return self.manualColumn.getColorVolume()
    def getLiquidClass(self):
        return self.manualColumn.liquidClass
    def getManualDeviationPercent(self):
        '''return the average deviation above  manual mean,average deviation below  manual mean '''
        manualMean = self.getManualMean()
        totalSumUp=0
        totalSumDown = 0
        upCount = 0
        downCount = 0
        for well  in self.manualColumn.wells:
            s = well.dilutionValue-manualMean
            if s>0:
                totalSumUp +=s
                upCount +=1
            else:
                totalSumDown +=-s
                downCount+=1
        if upCount:
            upAverage = totalSumUp/upCount
        else:
            upAverage = 0
        if downCount:
            downAverage = totalSumDown/downCount
        else:
            downAverage = 0
        percentUp = (upAverage/manualMean)*100
        percentDown = (downAverage/manualMean)*100
        return percentUp,percentDown
    def getDeviationPercentCompareToRobotMean(self):
        robotMean = self.getRobotMean()
        totalSumUp=0
        totalSumDown = 0
        upCount = 0
        downCount = 0
        for column in self.wellSpans[0].columns:
            for well in column.wells:
                s = well.dilutionValue-robotMean
                if s>0:
                    totalSumUp +=s
                    upCount +=1
                else:
                    totalSumDown +=-s
                    downCount+=1
        if upCount:
            upAverage = totalSumUp/upCount
        else:
            upAverage = 0
        if downCount:
            downAverage = totalSumDown/downCount
        else:
            downAverage = 0
        if robotMean:
            percentUp = (upAverage/robotMean)*100
            percentDown = (downAverage/robotMean)*100
        else:
            percentUp =0
            percentDown = 0
        return percentUp,percentDown
    def getManualAndRobotDeviationPercent(self):
        manualMean = self.getManualMean()
        robotMean = self.getRobotMean()
        totalSumManual=0
        totalSumRobot = 0
        manualCount = 0
        robotCount = 0
        #getting the manual deviation percents of the experiment
        for well  in self.manualColumn.wells:
            s = well.dilutionValue-manualMean
            totalSumManual +=abs(s)
            manualCount +=1
        if manualCount:
            manualAverage = totalSumManual/manualCount
        else:
            manualAverage = 0
            #getting the robot deviation percents of the experiment
        for column in self.wellSpans[0].columns:
            for well in column.wells:
                s = well.dilutionValue-manualMean
                totalSumRobot +=abs(s)
                robotCount +=1
        if robotCount:
            robotAverage = totalSumRobot/robotCount
        else:
            robotAverage = 0
        percentManual = (manualAverage/manualMean)*100
        percentRobot = (robotAverage/robotMean)*100
        return percentManual,percentRobot



class RobotExperiment:
    def __init__(self,_manualPlate,_robotPlate,_blankPlate,_volume,_id = None,_name = None):
        self.manualPlate = _manualPlate
        self.robotPlate = _robotPlate
        if _blankPlate:
            self.blankPlate = _blankPlate
        self.volume = _volume
        self.id = _id
        self.name = _name
        self.pipetors = []
        #reducing water values
        if _blankPlate:
            self.manualPlate = self.reduceBlankValues(self.manualPlate)
            self.robotPlate = self.reduceBlankValues(self.robotPlate)
        self.loadPipetors()
    def  loadPipetors(self):
        for i,col in enumerate(self.robotPlate.columns):
                for j,well in enumerate(col.wells):
                    if not i:
                        p = Pipetor()
                        p.id = j
                        p.wells = []
                        p.wells.append(well)
                        self.pipetors.append(p)
                    else:
                        (self.pipetors[j]).wells.append(well)
    def reduceBlankValues(self,plate):
        blankMean = self.getPlateODMean(self.blankPlate)
        newPlate = copy.deepcopy(plate)
        for i,col in enumerate(plate.columns):
            for j,well in enumerate(col.wells):
                oldDilVal = well.dilutionValue
                newPlate.columns[i].wells[j].dilutionValue = oldDilVal - blankMean
        return newPlate
    def getPlateODMean(self,plate):
        sum = 0
        amount = 0
        for col in plate.columns:
            for well in col.wells:
                try:
                    sum+=well.dilutionValue
                except Exception as e:
                    sum+=0
                amount+=1
        res = sum/amount
        return res
    def getMeans(self,waterFactor):
        sum = 0
        count = 0
        for p in self.pipetors:
            sum+=plateReader.getVolumeFromReading(self.volume,self.getPlateODMean(self.manualPlate),p.getMeans(),waterFactor)
            count+=1
        res = float(sum)/float(count)
        return res