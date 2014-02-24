from django.db import models
from django.contrib.auth.models import User
from dbindexer.api import register_index
from settings import *
from Utils.RobotQAUtils.plateReader import *

TYPE_CHOICES = (
    ('zymo','zymo'),
    ('wet','wet'),
    ('plateReader','plateReader'),
    ('dilution','dilution'),
    ('phospho','phospho'),
    ('pcr','pcr'),
    ('gel','gel'),
    ('lambda','lambda'),
    ('elongation','elongation'),
    ('gibson','gibson'),
    ('unite','unite'))

class PlatePlastica(models.Model): #The plate's physical form. e.g. deepwell square
    description = models.CharField(max_length=30, blank=True)
    wells = models.IntegerField(default=96)
    class Meta:
        db_table = u'plateplastica'
    def __unicode__(self):
        return u"%s" % self.description

class LiquidClass(models.Model):
    name =  models.CharField(max_length=20, blank=True)
    class Meta:
        db_table = u'liquidclass'
    def __unicode__(self):
        return u"%s" % self.name
class Experiment(models.Model):
    name =      models.CharField(max_length=20, blank=True)
    type =  models.CharField(max_length=20, blank=True,choices=TYPE_CHOICES,null=True)
    user = models.ForeignKey(User)
    #od = models.FloatField(null=True,blank=True)
    volume = models.FloatField()
    description = models.CharField(max_length=100,blank=True)
    pipetingMode =  models.CharField(max_length=20, blank=True,choices=(
        ('KEEPTIP','KEEPTIP'),
        ('MULTIPIP','MULTIPIP'),
        ('DEFAULT','DEFAULT')))
    #plateReader =  models.CharField(max_length=20, blank=True,choices=(
    #    ('new','new'),
    #    ('old','old'),
     #   ))
    liquidClass = models.ForeignKey(LiquidClass,related_name='+',blank=True,null=True)
    #blobkeyForLiquidClassInstance = models.CharField(max_length=200,default=None,null=True)
    tipType = models.IntegerField(blank=True,choices=((10,10),(20,20),(50,50),
                                                      (100,100),
                                                      (200,200),
                                                      (1000,1000)))
    sourcePlastic = models.ForeignKey(PlatePlastica,related_name='+',blank=True,null=True)
    destPlastic = models.ForeignKey(PlatePlastica,related_name='+',blank=True,null=True)
    date = models.DateField(blank=True,null=True,auto_now_add = True)
    time = models.TimeField(blank=True,null=True,auto_now_add = True)
    manualFile =models.FileField(upload_to='uploads/%Y/%m/%d/%H/%M/%S/',blank=True,null=True)
    robotFile = models.FileField(upload_to='uploads/%Y/%m/%d/%H/%M/%S/',blank=True,null=True)
    scriptFile = models.FileField(upload_to='uploads/%Y/%m/%d/%H/%M/%S/',blank=True,null=True)
    liquidClassFile = models.FileField(upload_to='uploads/%Y/%m/%d/%H/%M/%S/',blank=True, null=True)
    grade = models.FloatField(default=0)
    waterFactor = models.FloatField(default=0)
    numOfPipetors = models.IntegerField(default=8)
    means = models.FloatField(blank = True,default=0)
    distance = models.FloatField(blank = True,default=0)
    def __unicode__(self):
        return u"%s" % self.name
    class Meta:
        db_table = u'experiment'
    def getMeans(self):
        if not self.means:
            mwb = xlrd.open_workbook(file_contents=self.manualFile.file.read())
            rwb = xlrd.open_workbook(file_contents=self.robotFile.file.read())
            try:
                manualPlate = loadPlates(mwb,manualPlate = False)
                robotPlate = loadPlates(rwb,manualPlate = False)
                robotExpiriment = RobotExperiment(_manualPlate=manualPlate[0],_robotPlate=robotPlate[0],_blankPlate=None,_volume=self.volume)
                res = robotExpiriment.getMeans(self.waterFactor)
            except:
                res = 1
            self.means = res
            self.save()
        else:
            res = self.means
        return res
    def getDistance(self):
        res = abs(self.getMeans()-self.volume)
        self.distance = res
        self.save()
        return res
class UploadModel(models.Model):
    description = models.CharField(null=True,blank=True,max_length=200)
    file = models.FileField(upload_to='uploads/%Y/%m/%d/%H/%M/%S/')

class ScriptType(models.Model):
    name = models.CharField(max_length=20)
class RobotScript(models.Model):
    user = models.ForeignKey(User)
    script_date = models.DateField(blank=True,null=True,auto_now_add = True)
    script_time = models.TimeField(blank=True,null=True,auto_now_add = True)
    type =  models.CharField(max_length=20, blank=True,choices=TYPE_CHOICES)
    script_description =  models.CharField(max_length=20, blank=True)
    scriptFile = models.FileField(upload_to='uploads/%Y/%m/%d/%H/%M/%S/')
class RobotScriptError(models.Model):
    robotscript = models.ForeignKey(RobotScript,related_name='+')
    description = models.CharField(max_length=200,blank=True,null=True)
    date = models.DateField(blank=True,null=True,auto_now_add = True)
    time = models.TimeField(blank=True,null=True,auto_now_add = True)
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    email = models.EmailField(max_length=40)
    title = models.CharField(max_length=45)
    def __str__(self):
        return "%s's profile" % self.user

class LiquidClassVolume(models.Model):
    liquidClass = models.ForeignKey(LiquidClass,related_name='+')
    volume = models.IntegerField(blank=True,null=True,default=0)

class RobotError(models.Model):
    msg_id = models.CharField(max_length=50)
    msg_value = models.CharField(max_length=50)
    timeStamp = models.DateTimeField(blank=True,null=True,auto_now_add = True)
