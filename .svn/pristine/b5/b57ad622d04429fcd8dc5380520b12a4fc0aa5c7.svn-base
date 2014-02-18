from __future__ import with_statement
from xml.dom.minidom import parse, parseString
from google.appengine.api import files
from settings import PROJECT_PATH
import shutil
def clean_alphabet_string_from_garbage(alphabet_garbage, inputstring):
    outputstring = ''
    for character in inputstring:
        if character not in alphabet_garbage:
            outputstring+=character
    return outputstring

def dateTimeParserJson(date,action = 'date'):
    params = date.split(' ')
    if action == 'date':
        month = ''
        if params[1] == 'Jan':
            month = '01'
        day = params[2]
        year = params[3]
        res = year+'-'+month+'-'+day
    elif action == 'time':
        res = params[4]
    return res

def parseLiquidClasses(file,exp):
    data =file.read()
    data1 = data.decode('utf-8')
    beginIndex = data1.find(u"<LiquidClass name=\""+unicode(exp.liquidClass.name)+u"\" liquidName=")
    endIndex = data1[beginIndex:].find(u"</LiquidClass>")+beginIndex
    endIndex+=len(u"</LiquidClass>")
    lcStr =u'<?xml version="1.0" encoding="utf-8"?>\n'+ data1[beginIndex:endIndex]+u''
    lc_file = files.blobstore.create(mime_type='application/octet-stream')
    with files.open(lc_file, 'a') as f:
        f.write(lcStr)
    files.finalize(lc_file)
    # Get the file's blob key
    blob_key = files.blobstore.get_blob_key(lc_file)
    exp.blobkeyForLiquidClassInstance = blob_key

def replaceLiquidClass(liquidClassesFile,liquidClassFile,exp):
    #shutil.copy2(PROJECT_PATH+'/'+bigFileName, PROJECT_PATH+'/'+'backup_'+bigFileName)
    bigData=liquidClassesFile.read() # parse an XML file by name
    bigData1 = bigData.decode('utf-8')
    beginIndex = bigData1.find(u"<LiquidClass name=\""+unicode(exp.liquidClass.name)+u"\" liquidName=")
    endIndex = bigData1[beginIndex:].find(u"</LiquidClass>")+beginIndex
    endIndex+=len(u"</LiquidClass>")
    subStrToReplace = bigData1[beginIndex:endIndex]#got the  string I want to replace by the liquid class I got saved
    smallData =liquidClassFile.read()
    smallData1 = smallData.decode('utf-8')
    smallData1 = smallData1.replace(u'<?xml version="1.0" encoding="utf-8"?>\n',u'')
    bigData1 = bigData1.replace(subStrToReplace,smallData1)
    return bigData1