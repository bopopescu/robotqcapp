# -*- coding: utf-8 -*-
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from kioskApp.datables import *
from django.http import Http404
from django.shortcuts import render_to_response,render, redirect
from django.template.context import RequestContext
from kioskApp.models import *
from kioskApp.forms import *
from Utils.DBUtil.FilesIO.uploadFileFromWebClient import *
from PIL import Image
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
import settings
#from django.views.decorators.csrf import csrf_protect
from dojango.decorators import json_response, expect_post_request
from Utils.parsers import *
from Utils.generic import *
#from django.core.mail import send_mail
from django.http import HttpResponseRedirect
import django
from django.core.mail import send_mail
from email.mime.text import MIMEText
import smtplib
from django.views.generic.simple import direct_to_template
from django.utils import simplejson
CUSTOMERS_ROOT = settings.MEDIA_ROOT+'/customers/'
USERS_ROOT = settings.MEDIA_ROOT+'/users/'
CUSTOMERS_URL = settings.MEDIA_URL+'/customers/'
from django.core.mail import send_mail
from Utils.DBUtil.FilesIO.serializeModelsToXls import *
from datable.web.table import *
from filetransfers.api import prepare_upload
from filetransfers.api import serve_file
from Utils.RobotQAUtils.plateReader import *
from Utils.DBUtil.data_migrator import *
from google.appengine.ext import webapp
from google.appengine.api import urlfetch
import zipfile
from google.appengine.api import files
import os
import StringIO
import random
from django.views.decorators.csrf import csrf_exempt
from xml.dom.minidom import parse, parseString
from google.appengine.ext import blobstore
import time

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


def getAverageCV(pipetorsCV):
    num =0.0
    sum = 0.0
    res = 0.0
    for pip in pipetorsCV[2:]:
        num+=1
        sum+=pip[2]
    res = sum/num
    return res
def setGrade(exp):
    _man = exp.manualFile.file.file
    _rob = exp.robotFile.file.file
    dilsList,pipetorsCV ,dilsListForLineChart= compareManualToRobotReaderForWebApp(manualExcelFile= _man,robotExcelFile=_rob, experiment=exp)
    exp.grade = getAverageCV(pipetorsCV)
    exp.save()
def tutorial(request):
    c= {}
    c.update(csrf(request))
    return render_to_response('tutorial.html', c)

@csrf_exempt
def downloadExperimentFiles(request,exp_id):
    """

    """
    exp = Experiment.objects.get(pk = exp_id)
    _man = exp.manualFile.file.file
    _rob = exp.robotFile.file.file
    #get the liquid class from blobstore if it exist
    #if exp.blobkeyForLiquidClassInstance is not None:
    #    blob_reader = blobstore.BlobReader(exp.blobkeyForLiquidClassInstance)
    #    _lc  = blob_reader.read()
    if exp.liquidClassFile:
        _lc = exp.liquidClassFile.file.file
    else:
        _lc = None
    try:
        _script = exp.scriptFile.file.file
    except:
        _script = None
    zipstream=StringIO.StringIO()
    file = zipfile.ZipFile(zipstream,"w")
    file.name = 'zip'
    file.writestr('manual.xls',_man.read())
    file.writestr('robot.xls',_rob.read())
    if _script:
        file.writestr('script.conf',_script.read())
    if _lc is not None:
        file.writestr('liquidClass',_lc.read())
    file.size = zipstream.len
    file.close()
    exp.zipFile = file
    zipstream.seek(0)
    data = zipstream.read()
    response = HttpResponse(data, mimetype='application/zip')
    cd = 'attachment; %s' % 'files.zip'
    response['Content-Disposition'] = cd
    response['Content-Length'] = len(data)
    return response
    #return serve_file(request, exp.manualFile)
def downloadExperimentRobotFile(request,exp_id):
    exp = Experiment.objects.get(pk = exp_id)
    return serve_file(request, exp.robotFile)
def downloadExperimentScriptFile(request,exp_id):
    exp = Experiment.objects.get(pk = exp_id)
    return serve_file(request, exp.scriptFile)
def scripts_report(request):
    res = [['type','num of errors','num of times']]
    types = []
    scripts = RobotScript.objects.filter(user=request.user)
    for script in scripts:
        type = script.type
        if type not in types:
            types.append(type)
            scriptsOfType = RobotScript.objects.filter(type = type)
            errorsCount = 0
            timesCount = len(scriptsOfType) + random.randrange(1, 10)
            for sc in scriptsOfType:
                errorsCount+=len(RobotScriptError.objects.filter(robotscript = sc))
            list = [str(type),errorsCount,timesCount]
            res.append(list)
    c = RequestContext(request,{'res':res})
    return render_to_response('scripts_reports.html',c)
def scriptsIndex(request):
    try:
        userprofile = UserProfile.objects.get(user = request.user)
        title = userprofile.title
    except Exception as e:
            title = None
    c= {
        'title':title,
        'user':request.user
    }
    c.update(csrf(request))
    return render_to_response('robot_scripts_index.html', c)
def script_page(request,script_id):
    script = RobotScript.objects.get(pk=script_id)
    error = RobotScriptError(robotscript = script)
    form = RobotScriptErrorForm (instance=error)
    form.fields['robotscript'].widget = django.forms.widgets.HiddenInput()
    errorstable = getErrorsTable(script= script)
    if errorstable.willHandle(request):
        return errorstable.handleRequest(request)
    if request.method=='POST':
        is_post = True
        form = RobotScriptErrorForm (request.POST,instance=error) #bound form to script
        if form.is_valid():
            is_valid = True
            f=form.save(commit= False)
            f.robotScript = script
            f=form.save(commit= True)
            form.fields['robotscript'].widget = django.forms.widgets.HiddenInput()
            c = RequestContext(request,{'form':form,'errorstable':errorstable,'script':script})
            c.update(csrf(request))
        view_url= '/robot_scripts_page/'+str(script_id)
        return HttpResponseRedirect(view_url)
        #return render_to_response('script_page.html',c)
    return render_to_response("script_page.html", context_instance=RequestContext(request,{'errorstable':errorstable,'script':script,'form':form}))
def error_page(request,error_id):
    '''edit the error within the script'''
    error = RobotScriptError.objects.get(pk = error_id)
    form = RobotScriptErrorForm (instance=error)#a bound form to the error to edit.
    form.fields['robotscript'].widget = django.forms.widgets.HiddenInput()
    script = error.robotscript
    errorstable = getErrorsTable(script= script)
    if errorstable.willHandle(request):
        return errorstable.handleRequest(request)
    if request.method=='POST':
        form = RobotScriptErrorForm (request.POST,instance=error) #bound form to script
        f=form.save()
        c = RequestContext(request,{'form':form,'script':script})
        c.update(csrf(request))
        view_url= '/robot_scripts_page/'+str(script.id)
        return HttpResponseRedirect(view_url)
    return render_to_response("script_page.html", context_instance=RequestContext(request,{'errorstable':errorstable,'script':script,'form':form}))
def scripts_page(request):
    is_valid = False
    is_post = False
    exp_id = 0
    view_url = '/robot_scripts_page/'
    upload_url, upload_data = prepare_upload(request, view_url)
    scriptstable = getScriptsTable(_user = request.user)
    if scriptstable.willHandle(request):
        return scriptstable.handleRequest(request)
    if request.method=='POST':
        is_post = True
        form = RobotScriptForm (request.POST, request.FILES) #bound form to project
        if form.is_valid():
            is_valid = True
            f=form.save(commit= False)
            f.user = request.user
            f.script_date = request.POST.get('date_0')
            f.script_time = request.POST.get('date_1')
            f=form.save(commit= True)
            script = RobotScript.objects.get(pk= f.id)
            #c = RequestContext(request,{'form':form,'messege':'New script submitted successfully','scriptstable':scriptstable ,'upload_url':upload_url,
             #                           'upload_data':upload_data,})
            #c.update(csrf(request))
        return HttpResponseRedirect(view_url)
    else:
        robotScript = RobotScript(user = request.user)
        form = RobotScriptForm(instance=robotScript)
        form.fields['user'].widget = django.forms.widgets.HiddenInput()
        return direct_to_template(request, 'scripts_page.html',
            { 'form':form,
              'is_valid':is_valid,
              'is_post':is_post,
              'upload_url':upload_url,
              'upload_data':upload_data,
              'scriptstable':scriptstable})
def download_handler(request, pk):
    file = UploadModel.objects.get( id=pk)
    return serve_file(request, file.file)

def download_as_txt_handler(request,pk):
    file = UploadModel.objects.get(id=pk)
    response = HttpResponse(mimetype='text/conf')
    response['Content-Disposition'] = 'attachment; filename='+file.description
    file_content = serve_file(request, file.file).content
    response.write(file_content)
    return response
def download_as_xls_handler(request,pk):
    file = UploadModel.objects.get(id=pk)
    response = HttpResponse(mimetype='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename='+file.description+'.xls'
    file_content = serve_file(request, file.file).content
    response.write(file_content)
    return response
@csrf_exempt
def upload_handler(request):
    view_url = '/upload/'
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        form.save()
        return HttpResponseRedirect(view_url)
    upload_url, upload_data = prepare_upload(request, view_url)
    form = UploadForm()
    return direct_to_template(request, 'upload.html',
        {'form': form, 'upload_url': upload_url, 'upload_data': upload_data})
@csrf_exempt
def log_handler(request):
    #view_url = '/log/'
    if request.method == 'POST':
        #form = UploadForm(request.POST, request.FILES)
        #form.save()
        str = request.POST.keys()[0]
        toreplace = ['{','}','\"']
        for ch in toreplace:
            str = str.replace(ch,'')
        d = {}
        strings =  str.split(",")
        for i in strings:
            k,v = i.split(":")
            d[k.strip()]=v.strip()
        response = HttpResponse("success", content_type="text/plain")
        return response
    #upload_url, upload_data = prepare_upload(request, view_url)
    #form = UploadForm()
    #return direct_to_template(request, 'upload.html',
    #        {'form': form, 'upload_url': upload_url, 'upload_data': upload_data})
def index(request,message = None):
    login_error = False
    user = request.user
    userForm = None
    is_authenticated = False
    title = None
    if user.is_anonymous():
        userForm = UserForm()
        userForm.fields['email'].widget = django.forms.widgets.HiddenInput()
    if request.POST:
        userForm = UserForm(request.POST)
        userForm.fields['email'].widget = django.forms.widgets.HiddenInput()
        _username = request.POST.get('username')
        _password = request.POST.get('password')
        user = authenticate(username=_username, password=_password)
    if user is not None:
            if user.is_active:
                user.backend='django.contrib.auth.backends.ModelBackend'
                login(request, user)
                userForm = None
                is_authenticated = True
		try:
			userprofile = UserProfile.objects.get(user = user)
        	        title = userprofile.title
		except Exception as e:
			title = None
    else:
        login_error = True
    c= {
        'form':userForm,
        'user':user,
        ' user.is_authenticated':is_authenticated,
        'login_error':login_error,
        'message':message,
        'title':title
        }
    c.update(csrf(request))
    return render_to_response('robotQCIndex.html', c)
def new_plateplastica(request):
    is_valid = False
    is_post = False
    plate_id = 0
    descriptions = None
    if request.method=='POST':
        is_post = True
        form = PlatePlasticaForm (request.POST, request.FILES) #bound form to project
        if form.is_valid():
            descriptions = PlatePlastica.objects.filter(description = form.cleaned_data['description'])
            if not len(descriptions):
                form.save(commit = True)
            return HttpResponseRedirect('/')
    else:
        form = PlatePlasticaForm()
        c = RequestContext(request,{
            'form':form,
            'is_valid':is_valid,
            'is_post':is_post,
            })
        c.update(csrf(request))
        return render_to_response('new_plate_plastica.html',context_instance=c)
def new_experiment(request):
    '''experiments = Experiment.objects.all().order_by('-startdate')[:5]
    tasks = Task.objects.all().order_by('-startdate')[:5]
    reagents = Reagent.objects.all().order_by('-createdate')[:5]
    plates = Plate.objects.all().order_by('-timestamp')[:5]'''
    is_valid = False
    is_post = False
    exp_id = 0
    view_url = '/new_experiment/'
    upload_url, upload_data = prepare_upload(request, view_url)
    if request.method=='POST':
        is_post = True
        form = ExperimentForm (request.POST, request.FILES) #bound form to project
        form.fields["liquidClass"].queryset = LiquidClass.objects.all().order_by('name')
        if form.is_valid():
            is_valid = True
            f=form.save(commit= False)
            f.user = request.user
            f=form.save(commit= True)
            exp = Experiment.objects.get(pk= f.id)
            exp_id = exp.id
           # uploadFileFromWebClient(request,exp,AMAZONE_URL,'manualFile')
            _man = f.manualFile.file.file
            _rob = f.robotFile.file.file
            dilsList,pipetorsCV ,dilsListForLineChart= compareManualToRobotReaderForWebApp(manualExcelFile= _man,robotExcelFile=_rob, experiment=exp)
            exp.grade = getAverageCV(pipetorsCV)
            exp.means = exp.getMeans()
            exp.distance = exp.getDistance()
            exp.save()
            distance = abs(exp.getMeans()-exp.volume)
            c = RequestContext(request,{'exp':exp,'exp_id':exp_id,'form':form,'messege':'New experiment submitted successfully','pipetorsCV':pipetorsCV,'dilsList':dilsList,'dilsListForLineChart':dilsListForLineChart,   'upload_url':upload_url,
                                        'upload_data':upload_data,'comesFromNewExperiment':True,'distance':distance})
            c.update(csrf(request))
            return render_to_response('experiment_page.html',c)
            #return HttpResponseRedirect('experiment_page.html',c)
    else:
        form = ExperimentForm()
        form.fields["liquidClass"].queryset = LiquidClass.objects.all().order_by('name')
        return direct_to_template(request, 'new_experiment.html',
            { 'form':form,
              'is_valid':is_valid,
              'is_post':is_post,
              'exp_id':exp_id,
              'upload_url':upload_url,
              'upload_data':upload_data,
              })
def fileTest(request):
    '''experiments = Experiment.objects.all().order_by('-startdate')[:5]
    tasks = Task.objects.all().order_by('-startdate')[:5]
    reagents = Reagent.objects.all().order_by('-createdate')[:5]
    plates = Plate.objects.all().order_by('-timestamp')[:5]'''
    is_valid = False
    is_post = False
    exp_id = 0
    if request.method=='POST':
        is_post = True
        form = ExperimentForm (request.POST, request.FILES) #bound form to project
        if form.is_valid():
            is_valid = True
            f=form.save(commit=True)
            exp_id = f.id
            exp = Experiment.objects.get(pk=exp_id)
            manualFile = uploadFileFromWebClient(form,exp,EXPERIMENTS_ROOT+exp.name+'_'+str(exp.id)+'/','manual_file')
            robotFile = uploadFileFromWebClient(form,exp,EXPERIMENTS_ROOT+exp.name+'_'+str(exp.id)+'/','robot_file')
            scriptFile = uploadFileFromWebClient(form,exp,EXPERIMENTS_ROOT+exp.name+'_'+str(exp.id)+'/','script_file')
            #compareManualToRobotReaderForWebApp(manualExcelFile=manualFile.file,robotExcelFile=robotFile.file, experiment=exp)
    else:
        form = ExperimentForm()
    if form.is_bound:
        return experimentpage(request,exp_id,True)
    else:
        return render_to_response('new_experiment.html',context_instance=RequestContext(request,{
            'form':form,
            'is_valid':is_valid,
            'is_post':is_post,
            'exp_id':exp_id,
            }))
def experimentsPage(request):
    experimentstable = getExperimentsTable(_user = request.user)
    if experimentstable.willHandle(request):
        return experimentstable.handleRequest(request)
    return render_to_response(
        "experiments_page.html", context_instance=RequestContext(request,{'experimentstable':experimentstable}))


def experimentpage(request, exp_id,comesFromNewExp=False):
    view_url = '/experiments/'+exp_id
    #uploadFormForLiquidClasses = UploadForm()
    is_valid = False
    try:
        exp = Experiment.objects.get(pk = exp_id)
    except Exception as e:
        raise Http404
    if not request.user.is_authenticated():
         return index(request,message = 'user is not logged in')
    if request.method=='POST':
        f = ExperimentForm (request.POST,request.FILES,instance=exp)
        if f.is_valid() :
            is_valid = True
            exp = f.save()
    else:
        f= ExperimentForm(instance=exp)
        f.fields["liquidClass"].queryset = LiquidClass.objects.all().order_by('name')
    _man = exp.manualFile.file.file
    _rob = exp.robotFile.file.file
    dilsList,pipetorsCV ,dilsListForLineChart= compareManualToRobotReaderForWebApp(manualExcelFile= _man,robotExcelFile=_rob, experiment=exp)
    upload_url, upload_data = prepare_upload(request, view_url)
    distance = abs(exp.getMeans()-exp.volume)
    c = RequestContext(request,{'exp':exp,'exp_id':exp_id,'form':f,'messege':'New experiment submitted successfully','pipetorsCV':pipetorsCV,'dilsList':dilsList,'dilsListForLineChart':dilsListForLineChart, 'upload_url':upload_url, 'upload_data':upload_data,
                                'comesFromNewExperiment':False,'distance':distance})
    c.update(csrf(request))
    return render_to_response('experiment_page.html',c)

#blah
@csrf_exempt
def new_user(request):
    is_valid = False
    is_post = False
    message = None
    profilePhoto =None
    #logout(request)#if a new user is registering the the old user is not relevant anymore
    if request.method=='POST':
        is_post = True
        form = UserProfileForm (request.POST) #bound form to user
        if form.is_valid():
            is_valid = True
            #superuser = request.user
            #if superuser.username == 'ehud' and  superuser.is_active and superuser.is_authenticated(): #only ehud can add new users
            user = User.objects.create_user(username=form.cleaned_data['username'],email=form.cleaned_data['email'],password=form.cleaned_data['password'])
            user.save()
            userprofile = UserProfile.objects.create(user=user,title = form.cleaned_data['title'],username=form.cleaned_data		            ['username'] ,email=form.cleaned_data['email'],password=form.cleaned_data['password'])   
            userprofile.save()               
            message = 'successfully added user'
            return index(request,message)
    else:
        form = UserProfileForm()
    return render_to_response('new_user.html',context_instance=RequestContext(request,{
        'form':form,
        'is_valid':is_valid,
        'is_post':is_post,
        'message':message,
        }))

def logout_view(request):
    logout(request)
    user = request.user
    userForm = UserForm()
    userForm.fields['email'].widget = django.forms.widgets.HiddenInput()
    return render_to_response('index.html', context_instance=RequestContext(request,{
        'form':userForm,
        'user':user}))

@csrf_exempt
@expect_post_request
@json_response
def search_name(request):
    expName = request.POST.get('name')
    query = Experiment.objects.filter(user = request.user).filter(name=expName).order_by('date')
    listOfExpsGrades = [['grade','test']]
    for i,exp in enumerate(query):
        sublist = [str(exp.date),exp.grade]
        listOfExpsGrades.append(sublist)

    return {'listOfExpsGrades':listOfExpsGrades,'volume':query[0].volume,'liquidClass':query[0].liquidClass.name}


def plate(request):
    c= {}
    return render_to_response('plate.html', c)

def viewLiquidClassChart(request):
    form = LiquidClassVolumeForm()
    form.fields["liquidClass"].queryset = LiquidClass.objects.all().order_by('name')
    return render_to_response(
        "LiquidClassChartsPage.html", context_instance=RequestContext(request,{'form':form}))

@csrf_exempt
@expect_post_request
@json_response
def postViewLiquidClassChart(request):
    volume = float(request.POST.get('volume'))
    liquid_class_id = request.POST.get('liquidClass')
    liquid_class = LiquidClass.objects.get(pk = liquid_class_id)
    if not volume:
        experiments = Experiment.objects.filter(liquidClass = liquid_class).order_by('date','time')
    else:
        experiments = Experiment.objects.filter(liquidClass = liquid_class,volume = volume).order_by('date','time')

    distances = [['experiment','CV','distance 10 times multiplied']]
    for experiment in experiments:
        distance = abs(experiment.getMeans()-experiment.volume)
        if distance != 1:
            distances.append([experiment.name,experiment.grade, distance*10])
    return {'distances':distances,'liquidClass':liquid_class.name,'volume': volume,}


def uploadRobotErrors(request):

    view_url = '/upload_robot_errors/'
    upload_url, upload_data = prepare_upload(request, view_url)
    if request.method=='POST':
        form = UploadForm (request.POST, request.FILES) #bound form to project
        if form.is_valid():
            f=form.save()
            f.save()#save for reuse
            for line in f.file:
                params = line.split(' ### ')
                msg_id = params[0]
                msg_value = params[1]
                time_stamp_script = params[2]
                time_stamp_error = params[3].strip()
                struct_time_script = datetime.strptime(time_stamp_script, "%Y-%m-%d %H:%M:%S")
                try:
                    time_stamp = datetime.strptime(time_stamp_error, "%Y-%m-%d %H:%M:%S")
                except Exception as e:
                    time_stamp = struct_time_script
                try:
                    robotError ,created = RobotError.objects.get_or_create(msg_id=msg_id,msg_value=msg_value,
                    script_time=struct_time_script,timeStamp = time_stamp)
                except Exception as e:
                    pass
            return HttpResponseRedirect('/')
    else:
        form = UploadForm()
        return direct_to_template(request, 'uploadErrors.html',
            { 'form':form,
              'upload_data':upload_data,
              })

def viewRobotErrorsChart(request):
    robot_errors  = [['message','count']]
    robot_scripts = []
    existing_msgs = {}
    scripts = {}
    q = RobotError.objects.all()
    for err in q:
        script_time = str(err.script_time)
        err_time = str(err.timeStamp)
        msg = err.msg_value
        if msg.find('Checksum of <name> is missing or incorrect.Do you want to use it') == -1\
        and msg.find('Carrier <name> not found on grid') == -1:
            if scripts.get(script_time):
                    val = scripts.get(script_time)+1
                    scripts[script_time] = val
            else:
                    scripts[script_time] = 1
            if existing_msgs.get(msg):
                    val = existing_msgs.get(msg)+1
                    existing_msgs[msg] = val
            else:
                existing_msgs[msg] = 1
    for key,value in existing_msgs.iteritems():
                robot_errors.append([key,value])
    for key,value in scripts.iteritems():
        robot_scripts.append([key,value])
    robot_scripts.sort(key=lambda script: script[0])
    robot_scripts.insert(0,['script','number of errors'])
    c = RequestContext(request,{'robot_errors':simplejson.dumps(robot_errors),
                                'robot_scripts':simplejson.dumps(robot_scripts),'error_count':q.count(),'script_count':len(robot_scripts)-1})
    return render_to_response('view_robot_errors_chart.html',c)

def viewGraph(request):
    vertex = [ "1", "2", "3", "4",
                 "5", "6", "7", "8",
                 "9", "10", "11" ];
    edges = [
        ["1","2"],
        ["2","3"],
        [ "3", "4"],
        ["5","11"],
        ["11","4"],
        ["6","8"],
        ["8","11"],
        ["7","8"],
        ["8","9"],
        ["10","9"],

    ]

    c = RequestContext(request,{'vertex':vertex,'edges':edges})
    return render_to_response('graph.html',c)



@json_response
def test_angular(request):
    return {
  "-JHNbEfhdpBlZWS6fpyS" : {
    "description" : "Ambitious web apps.",
    "name" : "Ember",
    "site" : "http://emberjs.com/"
  },
  "-JHNbEcMTQy8MY5L98oW" : {
    "description" : "HTML enhanced for web apps!",
    "name" : "AngularJS",
    "site" : "http://angularjs.org"
  },
  "-JHNbEbH_LEksaQozSmz" : {
    "description" : "Innovative web-apps.",
    "name" : "SproutCore",
    "site" : "http://sproutcore.com/"
  },
  "-JHNbEgWRvP6FmgmAZdf" : {
    "description" : "Quick and beautiful.",
    "name" : "Batman",
    "site" : "http://batmanjs.org/"
  },
  "-JHNbEd7EujOCmy7hl23" : {
    "description" : "Small with class.",
    "name" : "Sammy",
    "site" : "http://sammyjs.org/"
  },
  "-JHNbEeEOC64vuQFeY4c" : {
    "description" : "Objective-J.",
    "name" : "Cappucino",
    "site" : "http://cappuccino.org/"
  },
  "-JHNbEdahDEeaH1blq2J" : {
    "description" : "Awesome MVC Apps.",
    "name" : "Spine",
    "site" : "http://spinejs.com/"
  },
  "-JHNbEbiPtfyp8Kxpd7Z" : {
    "description" : "Models for your apps.",
    "name" : "Backbone",
    "site" : "http://documentcloud.github.com/backbone/"
  },
  "-JHNbEbH_LEksaQozSmy" : {
    "description" : "Write less, do more.",
    "name" : "jQuery",
    "site" : "http://jquery.com/"
  },
  "-JHNbEeHF3DPjBR41yJA" : {
    "description" : "MVVM pattern.",
    "name" : "Knockout",
    "site" : "http://knockoutjs.com/"
  },
  "-JHNbEf7nHyn5WWguUmy" : {
    "description" : "JS in Java.",
    "name" : "GWT",
    "site" : "https://developers.google.com/web-toolkit/"
  }
}
