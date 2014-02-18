# coding: utf-8
from __future__ import absolute_import
import os
from Utils.DBUtil.FilesIO.saveFileToModel import *
from django.core.files.storage import default_storage
import boto
from boto.s3.key import Key
from settings import *
import StringIO
def uploadFileFromWebClient(request,cust,destDir,key):
    '''input: request, to get the file from client, proj: to save the file to the Files model, DestDir, phisycal directory on the disc, key to get the file from the
    request.FILES dictionary'''
    #if not os.path.exists(destDir):
    #    os.makedirs(destDir)
    file = request.FILES[key]
   # with open(unicode(destDir)+unicode(file.name).encode('unicode_escape'), 'wb+') as destination:
    #    for chunk in file.chunks():
    #        destination.write(chunk)
        #save a Files model
    #uploadFileToS3(unicode(destDir)+unicode(file.name).encode('unicode_escape'))
    #downloadFileFromS3()
    #return saveFileToModel(cust,destDir,file.name,key,request.user)
    return uploadFileToS3(unicode(destDir),unicode(file.name).encode('unicode_escape'),request,key,cust)

def uploadFileToS3(destDir,fileName,request,_type,cust):
    bucket_name = BUCKET_NAME
    conn = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    bucket = conn.get_bucket(bucket_name)
    # create a key to keep track of our file in the storage
    k = Key(bucket)
    k.key = fileName
    #k.set_contents_from_filename(destDir+fileName)
    buffer = ''
    #output = StringIO(fileName)
    #fileName.save(output)
    #output.seek(0)
    #buffer = output.getvalue()
    f = request.FILES[_type]
    s = f.file.getvalue()
    k.set_metadata('original_filename', fileName)
    k.set_contents_from_filename(f,policy='public-read')
# we need to make it public so it can be accessed publicly
# using a URL like http://s3.amazonaws.com/bucket_name/key
    k.make_public()
    s3File = S3File(key = k,user = request.user,name = fileName,type=_type,customer = cust)
    s3File.save()
# remove the file from the web server
   # os.remove(destDir+fileName)
    return s3File
def downloadFileFromS3():
    conn = boto.connect_s3(AWS_ACCESS_KEY_ID,
        AWS_SECRET_ACCESS_KEY)
    bucket = conn.get_bucket(BUCKET_NAME)
    bucket_list = bucket.list()
    for l in bucket_list:
        keyString = str(l.key)
    # check if file exists locally, if not: download it
        if not os.path.exists(keyString):
            l.get_contents_to_filename(keyString)

