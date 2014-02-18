
import os
import time
import  thread

threadlockForFilesDel = thread.allocate_lock()
def deleteContentOfDownloads(timeStamp,downloadDir):
    '''delete all related files of a project after download is finished'''
    time.sleep(60)
    threadlockForFilesDel.acquire()
    for subdir, dirs, files in os.walk(downloadDir):
        for file in files:
            if str(file).find(timeStamp) != -1:
                os.remove(downloadDir+'/'+str(file))
    threadlockForFilesDel.release()