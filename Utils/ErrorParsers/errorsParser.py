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
			   "EVO_EVO_011_000":"The value for Grid has to be between <number> and <number>."}
			   
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

def main():
    e = ErrorFinder(dirPath = r"C:\ProgramData\Tecan\LoggingServer\LogFiles\2.3\*")
    e.parseDir()

if __name__ == "__main__":
    main()
