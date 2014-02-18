from  kioskApp.models import *
from  django.core.files import File

def saveFileToModel(cust,workingDir,infile,key,_user):
    '''gets a project, a working directory and a file name with or without full path. saves a Files model and returns it.'''
    print '################in saveFileToModel##################'
    f = open(unicode(workingDir)+unicode(infile).encode('unicode_escape'),'rb')
    djangoFile = File(f)
    filesModel = Files(customer = cust,name = unicode(infile).encode('unicode_escape'),file = djangoFile,dir=workingDir,type = key,user=_user)
    print 'filesModel = '+str(filesModel.file)
    filesModel.save()
    f.close()
    return filesModel