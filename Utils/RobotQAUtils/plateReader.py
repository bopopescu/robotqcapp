import xlrd
import re
#from  numpy import *

from classes import *

col_len = 8


def decreaseWaterFromCol(col,colIndex,waterPlate):
    waterVal = getPlateMean(waterPlate)
    for i, well   in enumerate(col.wells):
        val = well.dilutionValue
       # waterVal = waterPlate.columns[colIndex].wells[i].dilutionValue
        newVal =  val  -waterVal
        col.wells[i].dilutionValue = newVal
    return col
def getFileName(file):
    res = None
    lastDirIndex = str(file).rfind('/')
    if lastDirIndex == -1:
        res = str(file)
    else:
        res = str(file)[lastDirIndex+1:len(str(file))]
    return res
def getFileNameWithoutMime(file):
    res = None
    name = getFileName(file)
    res = name[:name.rfind('.')]
    return res
def getFileDir(file):
    res = None
    lastDirIndex = str(file).rfind('/')
    res = str(file)[0:lastDirIndex+1]
    return res


def findDiluteForCol(columnIndex,xlsSheet):
    firstRowIndex = findFirstWellsRowIndexInSheet(xlsSheet)
    cell = xlsSheet.cell(findAtrributeRowIndex(xlsSheet,'dil'),columnIndex).value
    substrings = re.findall(r'\d:\d', cell)
    strDil = substrings[0]
    numerator = float(strDil.split(':')[0])
    denominator =  float(strDil.split(':')[1])
    res = numerator/denominator
    return res

def loadManualColumn(columnIndex,xlsSheet):
    wells = []
    plateRowBegin = findFirstWellsRowIndexInSheet(xlsSheet)
    dil = findDiluteForCol(columnIndex,xlsSheet)
    for i in range(plateRowBegin,plateRowBegin+col_len):#for each well in column
        well = Well(_x=columnIndex,_y=i-plateRowBegin+1,_dilutionValue=xlsSheet.cell(i,columnIndex).value)
        wells.append(well)
    colorVolume = xlsSheet.cell(findAtrributeRowIndex(xlsSheet,'volume'),columnIndex).value
    liquidClass = xlsSheet.cell(findAtrributeRowIndex(xlsSheet,'liquid class'),columnIndex).value
    labwareType = xlsSheet.cell(findAtrributeRowIndex(xlsSheet,'plate'),columnIndex).value
    scriptType = xlsSheet.cell(findAtrributeRowIndex(xlsSheet,'script'),columnIndex).value
    robotPlateName =  xlsSheet.cell(findAtrributeRowIndex(xlsSheet,'robot'),columnIndex).value
    manualColumn = ManualColumn(_wells=wells,_dilute=dil,_colorVolume=colorVolume,_liquidClass = liquidClass,_labwareType=labwareType,_scriptType=scriptType,_robotPlateName = robotPlateName)
    return manualColumn
def loadColumn(columnIndex,xlsSheet):
    wells = []
    plateRowBegin = findFirstWellsRowIndexInSheet(xlsSheet)
    for i in range(plateRowBegin,plateRowBegin + 8):#for each well in column
        well = Well(_x=columnIndex,_y=i-plateRowBegin+1,_dilutionValue=xlsSheet.cell(i,columnIndex).value)#converting reading to volume from aqution
        wells.append(well)
    col = Column(_wells=wells)
    return col
def loadRobotColumn(columnIndex,xlsSheet,lastRowIndex = None):
    wells = []
    plateRowBegin = findFirstWellsRowIndexInSheet(xlsSheet)
    #print 'plateRowBegin='+str(plateRowBegin)
    if lastRowIndex is None:
        r =  range(plateRowBegin,8)
    else:
        r =  range(plateRowBegin,plateRowBegin+lastRowIndex)
    for i in r:#for each well in column
        well = Well(_x=columnIndex,_y=i-plateRowBegin+1,_dilutionValue=xlsSheet.cell(i,columnIndex).value)
        wells.append(well)
    robotColumn = Column(_wells=wells)
    return robotColumn


def findWellsSpans(columnIndex,sh,dir,waterPlate):
    '''gets column index ,  xls sheet, working directory and a water plate.
    returns a list of wellSpans for this column.'''
    wellSpans=[]
    i = findAtrributeRowIndex(sh,'robot')
    while True and i != -1:
        try:
             cell = sh.cell(i,columnIndex).value
        except Exception as e:
            break
        match =re.search("(\w+[:]\s*[a-zA-Z][0-9][+]\d+)",str(cell))
        if match is None:
            break
        pattern =(re.findall("(\w+[:]\s*[a-zA-Z][0-9][+]\d+)",str(cell)))[0]
        plateName = pattern.split(':')[0]
        wells =  pattern.split(':')[1]
        wellBeginStr = wells.split('+')[0]
        wellBeginStr = wellBeginStr.strip()
        wellEndStr = wells.split('+')[1]
        wellEndStr = wellEndStr.strip()
        wellBegin = createWellFromString(wellBeginStr)
        #wellEnd = createWellFromIndex(int(wellEndStr))
        endInd = wellBegin.getIndex() + int(wellEndStr) -1
        wellEnd = createWellFromIndex(endInd)
        pathToPlateFile = dir+plateName+'.xls'
        ws = WellsSpan(_firstWell=wellBegin,_lastWell=wellEnd, _pathToPlateFile=pathToPlateFile,_waterPlate=waterPlate)
        wellSpans.append(ws)
        i+=1
    return wellSpans
def convert_char(old):
    if len(old) != 1:
        return 0
    new = ord(old)
    if 65 <= new <= 90:
        # Upper case letter
        return new - 64
    elif 97 <= new <= 122:
        # Lower case letter
        return new - 96
        # Unrecognized character
    return 0
def createWellFromString(instr):
    rowStr=instr[0]
    row = convert_char(rowStr)
    col = int(instr[1])
    res = Well(_x=col,_y=row)
    return res
def createWellFromIndex(index):
    col = float(index)/8.0
    colInt = int(index)/8
    if col - colInt:
        col+=1
    col = int(col)
    row = int(index)%8
    if not row:
        row = 8
    res = Well(_x=col,_y=row)
    return res



def createRowLabels(length,name):
    res = []
    for i in range(0,length):
        res.append(name+str(i+1))
    return res
def cutStringsLength(params,length):
    for i, paramList in enumerate(params):
        for j,s in enumerate(paramList):
            if len(s)>length:
                s = s[:length]
                paramList[j] = s
                params[i] = paramList
    return  params
def getExpVolumes(dilutionStatistics):
    vals = []
    for d in dilutionStatistics:
        vals.append(d.getManualColorVolume())
    return vals
def getExpLiquidClasses(dilutionStatistics):
    vals = []
    for d in dilutionStatistics:
        vals.append(d.getLiquidClass())
    return vals
def getManualMeansTupple(dilutionStatistics):
    vals = []
    for d in dilutionStatistics:
        vals.append(d.getManualMean())
    res = tuple(vals)
    return res
def getManualVarianceTupple(dilutionStatistics):
    vals = []
    for d in dilutionStatistics:
        vals.append(d.getManualVariance())
    res = tuple(vals)
    return res
def getManualMeans(dilutionStatistics):
    vals = []
    for d in dilutionStatistics:
        vals.append(d.getManualMean())
    a = array(vals)
    res = a.mean()
    return res
def getRobotMeansTupple(dilutionStatistics,wellSpanIndex = 0):
    vals = []
    for d in dilutionStatistics:
        vals.append(d.getRobotMean(wellSpanIndex))
    res = tuple(vals)
    return res
def getRobotVarTupple(dilutionStatistics):
    vals = []
    for d in dilutionStatistics:
        vals.append(d.getRobotVariance())
    res = tuple(vals)
    return res
def getRobotDeltaTupple(dilutionStatistics):
    vals = []
    for d in dilutionStatistics:
        vals.append(d.getRobotDelta())
    res = tuple(vals)
    return res
def getRobotMinList(dilutionStatistics):
    vals = []
    for d in dilutionStatistics:
        vals.append(d.getRobotMin())
    return vals
def getManualMinList(dilutionStatistics):
    vals = []
    for d in dilutionStatistics:
        vals.append(d.getManualMin())
    return vals
def getManualDeltaTupple(dilutionStatistics):
    vals = []
    for d in dilutionStatistics:
        vals.append(d.getManualDelta())
    res = tuple(vals)
    return res
def getManualVarTupple(dilutionStatistics):
    vals = []
    for d in dilutionStatistics:
        vals.append(d.getManualVariance())
    res = tuple(vals)
    return res
def getUniqueWellsIndexes(dilutionStatistics):
    vals = []
    for d in dilutionStatistics:
        vals.extend(d.getUniqueWellsIndexes())
    return vals
def getUniqueWellsIndexesOutSideMean(dilutionStatistics,manual = True):
    '''returns a list of unique wells compare to manual means if manual. compare to robot means,else.'''
    vals = []
    for d in dilutionStatistics:
        if manual:
            mean = d.getManualMean()
        else:
            mean = d.getRobotMean()
        vals.extend(d.getUniqueWellsIndexesCompareToOutsideMean(mean,rob=True))
    return vals
def getUniqueWellsIndexesOutSideMeanManual(dilutionStatistics,manual = True):
    vals = []
    for d in dilutionStatistics:
        if manual:
            mean = d.getManualMean()
        else:
            mean = d.getRobotMean
        vals.extend(d.getUniqueWellsIndexesCompareToOutsideMean(mean,rob = False))
    return vals
def getColumnsParams(dilutionStatistics):
    vals = []
    for d in dilutionStatistics:
        vals.append(d.manualColumn.getParams())
    return vals
def findEndOfRowValuesIndex(sh):
    plateRowBegin = findFirstWellsRowIndexInSheet(sh)
    ind = -1
    curr_row_len= len(sh.row_values(plateRowBegin))
    curr_cell = 0
    while curr_cell <  curr_row_len :
        curr_cell+=1
        try:
            cell_type = sh.cell_type(plateRowBegin, curr_cell)
        except Exception as e:
            #print e.message
            ind = curr_cell
            break
        # Cell Types: 0=Empty, 1=Text, 2=Number, 3=Date, 4=Boolean, 5=Error, 6=Blank
        if cell_type != 2 and curr_cell > 1:
            ind = curr_cell
            break
    return ind
def loadPlate(sh,manualPlate = False):
    cols = []
    numOfPlateCols = findEndOfRowValuesIndex(sh)
    for i in  range(1,numOfPlateCols):#for each column
        if not manualPlate:
            col = loadColumn(i,sh)
        else:
            col = loadManualColumn(i,sh)
        cols.append(col)
    p = Plate(_columns=cols,_xlsSheet=sh)
    return p
def loadSheet(pathToFile,sheetName):
    wb = xlrd.open_workbook(pathToFile)
    sh = wb.sheet_by_name(sheetName)
    return sh
def decreaseWaterMeasurments(waterPlate,regularPlate):
    waterMean = getPlateMean(waterPlate)
    for i , col in enumerate(regularPlate.columns):
        for j, well in enumerate(col.wells):
            try:

                #val = well.dilutionValue - waterPlate.columns[i].wells[j].dilutionValue
                val = well.dilutionValue -waterMean
            except Exception as e:
                #print e.message
                break
            regularPlate.columns[i].wells[j].dilutionValue = val
    return regularPlate
def getPlateMean(plate):
    vals = []
    for col in plate.columns:
        for well in col.wells:
            vals.append(well.dilutionValue)
    a = array(vals)
    res = a.mean()
    return res
def isSheetValid(sh):
    res = False
    try:
        cell = sh.cell(0,0)
    except :
        cell = None
        val = None
    if cell is not None:
        val = sh.cell(0,0).value
    if val and len(val) > 0 and val.find('Application: Tecan i-control' )> -1:
        res = True
    return res
def loadPlates(wb,manualPlate = False):
    plates = []
    worksheets = wb.sheet_names()
    for worksheet_name  in worksheets:
        worksheet = wb.sheet_by_name(worksheet_name)
        if isSheetValid(worksheet):
            p = loadPlate(worksheet,manualPlate)
            plates.append(p)
    return plates
def findFirstWellsRowIndexInSheet(sh):
    num_rows = sh.nrows - 1
    num_cells = sh.ncols - 1
    curr_row = -1
    res = -1
    while curr_row < num_rows:
        curr_row += 1
        row = sh.row(curr_row)
        curr_cell = -1
        while curr_cell < num_cells:
            curr_cell += 1
            # Cell Types: 0=Empty, 1=Text, 2=Number, 3=Date, 4=Boolean, 5=Error, 6=Blank
            cell_type = sh.cell_type(curr_row, curr_cell)
            cell_value = sh.cell_value(curr_row, curr_cell)
            if cell_value == 'A':
                try:
                    next_cell_type = sh.cell_type(curr_row, curr_cell+1)
                except Exception as e:
                    e.message
                if next_cell_type == xlrd.XL_CELL_NUMBER or   next_cell_type == xlrd.XL_CELL_TEXT:
                    res = curr_row
    return res
def findAtrributeRowIndex(sh,atrrName):
    num_rows = sh.nrows - 1
    curr_row = -1
    ind = -1
    while curr_row < num_rows:
        curr_row += 1
        row = sh.row(curr_row)
        cell_value = sh.cell_value(curr_row, 0)
        if cell_value == atrrName:
            ind = curr_row
            break
    return ind
def getMaxWell(wells):
    max = 0
    for well in wells:
        if well.dilutionValue > max:
            max = well.dilutionValue
    return max
def getMinWell(wells):
    min = wells[0].dilutionValue
    for well in wells:
        if well.dilutionValue <min:
            min = well.dilutionValue
    return min
def getDeviationPercentTupple(dilutionStatistics):
    '''returns a tupple of mean(dilutionValue-manualMean)/manual mean'''
    valsUp = []
    valsDown = []
    for d in dilutionStatistics:
        manualMean = d.getManualMean()
        totalSumUp=0
        totalSumDown = 0
        upCount = 0
        downCount = 0
        for column in d.wellSpans[0].columns:
            for well in column.wells:
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
        valsUp.append(percentUp)
        valsDown.append(percentDown)
    resUp = tuple(valsUp)
    resDown = tuple(valsDown)
    return resUp,resDown
def getManualDeviationPercentTupple(dilutionStatistics):
    '''returns a tupple of mean(dilutionValue-manualMean)/manual mean'''
    valsUp = []
    valsDown = []
    for d in dilutionStatistics:
        manualMean = d.getManualMean()
        totalSumUp=0
        totalSumDown = 0
        upCount = 0
        downCount = 0
        for well  in d.manualColumn.wells:
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
        valsUp.append(percentUp)
        valsDown.append(percentDown)
    resUp = tuple(valsUp)
    resDown = tuple(valsDown)
    return resUp,resDown
def getManualAndRobotDeviationPercentTupples(dilutionStatistics):
    '''returns a tupple of mean(dilutionValue-manualMean)/manual mean
    and a tupple of mean(dilutionValue-robotMean)/robot mean'''
    valsManual = []
    valsRobot = []
    for d in dilutionStatistics:
        manualMean = d.getManualMean()
        robotMean = d.getRobotMean()
        totalSumManual=0
        totalSumRobot = 0
        manualCount = 0
        robotCount = 0
        #getting the manual deviation percents of the experiment
        for well  in d.manualColumn.wells:
            s = well.dilutionValue-manualMean
            totalSumManual +=abs(s)
            manualCount +=1
        if manualCount:
            manualAverage = totalSumManual/manualCount
        else:
            manualAverage = 0
        #getting the robot deviation percents of the experiment
        for column in d.wellSpans[0].columns:
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
        valsManual.append(percentManual)
        valsRobot.append(percentRobot)
    resManual = tuple(valsManual)
    resRobot = tuple(valsRobot)
    return resManual,resRobot
def getDeviationPercentTuppleCompareToRobotMean(dilutionStatistics):
    '''returns a tupple of mean(dilutionValue-RobotMean)/robot mean'''
    valsUp = []
    valsDown = []
    for d in dilutionStatistics:
        robotMean = d.getRobotMean()
        totalSumUp=0
        totalSumDown = 0
        upCount = 0
        downCount = 0
        for column in d.wellSpans[0].columns:
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
        valsUp.append(percentUp)
        valsDown.append(percentDown)
    resUp = tuple(valsUp)
    resDown = tuple(valsDown)
    return resUp,resDown

def getVolumeFromReading(expectedVolume,manualRead,robotRead,waterFactor = 0.04):
    deviationFactor = (robotRead - waterFactor)/(manualRead - waterFactor)
    return expectedVolume*deviationFactor

def getReadingFromVolume(volume):#by calibration chart
    reading = (volume+1.0938)/79.051
    return reading
def normalizeVolumeByManualRead(manualVolume,volumeSupposeToBe,actualVolume):
    res = (volumeSupposeToBe/manualVolume)*actualVolume
    return res
def getCV(wells,mean):
    sum = 0.0
    for  w in wells:
        try:
            sum+=(w.dilutionValue-mean)**2
        except Exception:
            sum+=0
    sum/=len(wells)
    sum **=1.0/2.0
    if mean !=0:
        sum/=mean
    return sum
def newCompareManualToRobotReader( manualExcelFile = r'S:\pie\Shiran\RobotTest\16082012\MANUAL_1A.xls',pathToWaterFile = r'S:\pie\Shiran\RobotTest\16082012\blank_oldRobot_allPlate.xls'):
    #loading the regular plate and decreasing the water value from the wells
    mwb = xlrd.open_workbook(manualExcelFile)
    regularPlates = loadPlates(mwb,manualPlate = True)
    wwb = xlrd.open_workbook(pathToWaterFile)
    waterPlates =  loadPlates(wwb)
    dilutionStatistics = []
   # for i,plate in enumerate(regularPlates):
    #    regularPlates[i] = decreaseWaterMeasurments(waterPlates[0],regularPlates[i])
    #loading robotWellSpans for each manual plate and creating DilutionStatistic classes
    for i, p in  enumerate(regularPlates):
        for j,col in enumerate(p.columns):
            manualExcelFile = manualExcelFile.replace('\\','/')
            dir = getFileDir(manualExcelFile)
            manualExcelFile = manualExcelFile.replace('/','\\')
            robotWellSpans = findWellsSpans(j+1,p.xlsSheet,dir,waterPlates[0])
            for rw in robotWellSpans:
                d =  DilutionStatistic(_manualColumn=col,_wellSpans=[rw])
                dilutionStatistics.append(d)
    #giving id for each dilutionStistic
    for i,d in enumerate(dilutionStatistics):
        d.id = i
        d.loadPipetors()
        #printPipetorsCV(d)
            #printing graphs

def getPipetorsCVForWebbApp(robotExperiment,manualExcelFile,exp = None,plateReaderUsed = 'old'):
    #manualRead = plateReader.getVolumeFromReading(robotExperiment.getPlateODMean(robotExperiment.manualPlate),plateReaderUsed)
    manualVolume= exp.volume
    manualRead = robotExperiment.getPlateODMean(robotExperiment.manualPlate)
    N = len(robotExperiment.pipetors)
    means = []
    manualWellList = []
    for col in robotExperiment.manualPlate.columns:
        manualWellList.extend(col.wells)
    cv = [plateReader.getCV(manualWellList,robotExperiment.getPlateODMean(robotExperiment.manualPlate))]
    sum = 0
    count = 0
    for p in robotExperiment.pipetors:
        means.append(plateReader.getVolumeFromReading(exp.volume,manualRead,p.getMeans(),exp.waterFactor))
        sum+= plateReader.getVolumeFromReading(exp.volume,manualRead,p.getMeans(),exp.waterFactor)
        count+=1
        cv.append(plateReader.getCV(p.wells,p.getMeans()))
    if exp:
        exp.means = float(sum)/float(count)
        exp.save
    ys1 =[manualVolume]
    ys1.extend(means)#ys1 holds all means, first index is manual, the rest are robot
    ys2=cv#ys2 holds all the cv values. first is manual
    dilsList = [['volume','pipeting operation']]
    for i,col in enumerate(robotExperiment.manualPlate.columns):#populating the manual column
        for j,well in enumerate(col.wells):
            dils = []
            dils.append(i)
            dils.append(getVolumeFromReading(exp.volume, manualRead, well.dilutionValue,exp.waterFactor))
            dilsList.append(dils)
    dilsListForLineChart = [['well', 'tip1', 'tip2','tip3','tip4','tip5','tip6','tip7','tip8']]
    for i in range(len(robotExperiment.pipetors[0].wells)):
        dils = ['well'+str(i+1)]
        for j , p in enumerate(robotExperiment.pipetors):
            dils.append(getVolumeFromReading(exp.volume,manualRead, p.wells[i].dilutionValue,exp.waterFactor))
        dilsListForLineChart.append(dils)
    for i, p in enumerate(robotExperiment.pipetors):#populationg the robot columns
      for j,w in enumerate(p.wells):
         dils = []
         dils.append(i+1)
         dils.append(getVolumeFromReading(exp.volume,manualRead,p.wells[j].dilutionValue,exp.waterFactor))
         dilsList.append(dils)
    cvAndMean = []
    minilist = ['pipetor type','means','cv']
    cvAndMean.append(minilist)
    for i,y in enumerate(ys1):
        if not i:
            minilist = ['manual',y,ys2[i]*100]
        else:
            minilist = ['tip'+str(i),y,ys2[i]*100]
        cvAndMean.append(minilist)
    return dilsList, cvAndMean,dilsListForLineChart

def compareManualToRobotReaderForWebApp( manualExcelFile = '',robotExcelFile = '',waterFile = '',experiment = None,plateReaderUsed = 'old'):
    #loading the regular plate and decreasing the water value from the wells
    mwb = xlrd.open_workbook(file_contents=manualExcelFile.read())
    rwb = xlrd.open_workbook(file_contents=robotExcelFile.read())
    wwb = None
    waterPlate = None
    manualPlate = loadPlates(mwb,manualPlate = False)
    robotPlate = loadPlates(rwb,manualPlate = False)
    robotExpiriment = RobotExperiment(_manualPlate=manualPlate[0],_robotPlate=robotPlate[0],_blankPlate=None,_volume=experiment.volume)
    pipetorsCV = getPipetorsCVForWebbApp(robotExpiriment,manualExcelFile,experiment,plateReaderUsed)
    return pipetorsCV

