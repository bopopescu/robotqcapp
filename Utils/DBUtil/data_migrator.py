from kioskApp.models import *
import xlrd
from filetransfers.api import serve_file

def liquid_class_import():
	for line in open('/home/ehud/Desktop/code/robotQC/Utils/DBUtil/liquid_classes','r').readlines():
		liquidclass,created = LiquidClass.objects.get_or_create(name = line)
		liquidclass.save()
def plate_plastica_import():
	for line in open('/home/ehud/Desktop/code/robotQC/Utils/DBUtil/plate_plastica','r').readlines():
		parts = line.split()
		description = ''
		wells = ''
		for i,part in enumerate(parts):
			if i < len(parts) - 1:
				if not i:
					description+=part
				else:
					description+= ' '+part
			else:
				wells = part
		plateplastica,created = PlatePlastica.objects.get_or_create(description = description,wells=int(wells))
		plateplastica.save()
def script_type_import():
    #for line in open('C:\Users\ehud1\Desktop\code\robotQC\Utils\DBUtil\scriptTypes','r').readlines():
    for line in open(PROJECT_PATH+'\Utils\DBUtil\scriptTypes','r').readlines():
        liquidclass,created = ScriptType.objects.get_or_create(name = line)
        liquidclass.save()



# -*- coding: utf-8 -*-
def download_handler(request, pk):
    file = UploadModel.objects.get( id=pk)
    return serve_file(request, file.file)

def readErrors(request):
    #wb = xlrd.open_workbook(r'C:\Users\ehud\Desktop\code\robotQC\Utils\DBUtil\FilesIO\errors_scripts.xls')
    #wb = xlrd.open_workbook(download_handler(request,48001))
    #uploadmodel = UploadModel.objects.get(pk=48001)
    uploadmodel = UploadModel.objects.get(pk=48001)
    wb = xlrd.open_workbook(file_contents=uploadmodel.file.file.read())
    sh = wb.sheet_by_index(0)
    for rownum in range(sh.nrows):
        if rownum > 0:
            description = sh.cell(rownum,1).value
            type = sh.cell(rownum,3).value
            date = sh.cell(rownum,5).value
            script = RobotScript()
            script.type = type
            script.user = request.user
            #script.script_date =date
            #script.script_description = description
            script.save()
            error = RobotScriptError()
            error.robotscript = script
            error.description = description
            #error.date = date
            error.save()


