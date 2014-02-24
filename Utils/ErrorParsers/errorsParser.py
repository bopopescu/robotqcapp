import glob
from xml.dom.minidom import parse, parseString

ERROR_DICT = {"EVO_EVO_000_011":"No connection to the instrument.Retry?",
              "EVO_EVO_020_000":"Carrier <name> not found on grid",
              "EVO_EVO_007_001":"Error opening <file name>",
              "EVO_EVO_013_039":"Invalid operand",
              "EVO_EVO_000_031":"Checksum of <name> is missing or incorrect.Do you want to use it?",
              "EVO_EVO_003_002":"Error shutting down devices: <name>",
              "EVO_EVO_007_001":"Error opening <file name>",
              "EVO_EVO_012_002":"Invalid operand",
              "EVO_EVO_012_006":"Device not initialised",
              "EVO_EVO_008_006":"Script contains errors! For more information see the log file.",
              "EVO_EVO_023_000":"Instrument error <error number> (<error text>), device <name>, command <name>",
              "EVO_EVO_000_006":"Error writing <file name>",
              "EVO_EVO_003_001":"Error unloading device drivers: ",
              "EVO_EVO_013_004":"Arm is collided",
              "EVO_EVO_006_000":"Error initializing devices: <name>",
              "EVO_EVO_020_002":"<axis>-coordinate of ROMA vector ",
              "EVO_EVO_002_001":"DITI not dropped for tip<number>.Retry?",
              "EVO_EVO_013_013":"Arm is collided",
              "EVO_EVO_000_012":"Error loading device drivers: <file name>",
              "EVO_EVO_013_009":"Error in liquid sensor",
              "EVO_EVO_012_007":"Command Overflow",
              "EVO_EVO_005_009":"The selected script is empty! It cannot be executed!",
              "EVO_EVO_017_002":"Roma <number> not found!",
              "EVO_EVO_011_000":"The value for Grid has to be between <number> and <number>.",
              "EVO_EVO_024_001":"The resulting script contains invalid groups or loops. The action is canceled.",
              "EVO_EVO_007_010":"Operator query for process variables failed! The operator cancelled the query dialog.",
              "EVO_EVO_002_000":"Diluter <number> broken! Switching Diluter off!",
              "EVO_EVO_011_001":"The value for Site has to be ",
              "EVO_EVO_022_000":"Instrument has no LiHA ",
              "EVO_EVO_011_002":"The value for Position in labware has to be between <number> and <number>."}

class RobotError(object):
    def __init__(self, message,date):
        self.message = message
        self.date = date
class ErrorFinder(object):
    def __init__(self, dirPath):
        self.dirPath = dirPath
    def parseDir(self):
        msg_ids = set()
        unknown_msg_ids = set()
        output=open ('output.txt' , 'w')
        for j,file in enumerate(glob.glob(self.dirPath)):
            if j < 100000:
                try:
                    dom = parse(file)
                    logs = dom.getElementsByTagName("Log")
                    for log in logs:
                        message = log.getAttribute("Message")
                        l = [i for i in range(len(message)) if message.startswith('EVO_EVO_', i)]
                        if l:
                            for start in l:
                                end = start + len("EVO_EVO_006_000")
                            msg_id = message[start:end]
                            msg_value = ERROR_DICT.get(msg_id)
                            if not msg_value:
                                unknown_msg_ids.add(msg_id)
                            timeStamp = log.getAttribute("TimeStamp")
                            print "j = "+str(j)
                            print msg_id+' ### '+msg_value+' ### '+ timeStamp
                            output.write(msg_id+' ### '+msg_value+' ### '+ timeStamp+'\n')
                            msg_ids.add(msg_id)

                except Exception as e:
                    print
        output.close()
        for msg_id in unknown_msg_ids:
            print msg_id
    def getMessageParams(self,message):
        start = message.find('EVO_EVO_')
        end = start + len("EVO_EVO_006_000")
        msg_id = message[start:end]
        msg_value = ERROR_DICT.get(msg_id)
        return msg_id,msg_value
    def getScriptTimeStamp(self,message):
        timedict = {'year':4,'month':6,'day':8,
                    'hour':11,'minute':13,'second':15}
        year = message[0:timedict.get('year')]
        month = message[timedict.get('year'):timedict.get('month')]
        day =  message[timedict.get('month'):timedict.get('day')]
        hour =  message[timedict.get('day')+1:timedict.get('hour')]
        minute =  message[timedict.get('hour'):timedict.get('minute')]
        second =  message[timedict.get('minute'):timedict.get('second')]
        #2013-04-25 13:50:32.21428
        res = year+'-'+month+'-'+day+' '+hour+':'+minute+':'+second
        return res
    def getErrorTimeStamp(self,message):
        start = 2
        end = 2+len('16:25:00')
        time = message[start:end]
        return time
    def getScriptDate(self,message):
        timedict = {'year':4,'month':6,'day':8,
                    'hour':11,'minute':13,'second':15}
        year = message[0:timedict.get('year')]
        month = message[timedict.get('year'):timedict.get('month')]
        day =  message[timedict.get('month'):timedict.get('day')]
        res = year+'-'+month+'-'+day
        return res
    def parseTextLogDir(self):
        unknown_msg_ids = set()
        output=open ('output.txt' , 'w')
        for j,file in enumerate(glob.glob(self.dirPath)):
            if j < 100000 and file.find('EVO_') != -1:
                f = open(file)
                for i , message in enumerate(f.readlines()):
                    if i == 1:
                        scriptTimeStamp =  self.getScriptTimeStamp(message)
                        scriptDate = self.getScriptDate(message)
                    if message.find('EVO_EVO_') != -1:
                        msg_id,msg_value = self.getMessageParams(message)
                        msg_time = scriptDate+' '+self.getErrorTimeStamp(message)
                        if not msg_value:
                            unknown_msg_ids.add(msg_id)
                        delimeter = ' ### '
                        #msg_id, msg_value,script_time_stamp,msg_time
                        try:
                            res = msg_id+delimeter+msg_value+delimeter+ scriptTimeStamp+delimeter+msg_time+'\n'
                            print res
                            output.write(res)
                        except Exception as e:
                            print e
        output.close()
        for msg_id in unknown_msg_ids:
            print msg_id
def main():
    e = ErrorFinder(dirPath = r"C:\ProgramData\Tecan\EVOware\AuditTrail\log\*")
    e.parseTextLogDir()

if __name__ == "__main__":
    main()
