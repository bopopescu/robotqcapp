# Initialize App Engine and import the default settings (DB backend, etc.).
# If you want to use a different backend you have to remove all occurences
# of "djangoappengine" from this file.
from djangoappengine.settings_base import *

import os
MEDIA_ROOT = ''
MEDIA_URL = ''
# Activate django-dbindexer for the default database
DATABASES['native'] = DATABASES['default']
DATABASES['default'] = {'ENGINE': 'dbindexer', 'TARGET': 'native'}
AUTOLOAD_SITECONF = 'indexes'
EMAIL_BACKEND ='appengine_emailbackend.EmailBackend'
#EMAIL_BACKEND = 'appengine_emailbackend.async.EmailBackend'
SECRET_KEY = '=r-$b*8hglm+858&9t043hlm6-&6-3d3vfc4((7yd0dbrakhvi'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'ehudmagal@gmail.com'
EMAIL_HOST_PASSWORD = 'eithan2013'
SERVE_FILE_BACKEND = 'filetransfers.backends.default.serve_file'
INSTALLED_APPS = (
    #    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'djangotoolbox',
    'autoload',
    'dbindexer',
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    # djangoappengine should come last, so it can override a few manage.py commands
    'djangoappengine',
    'dojango',
    'datable',
    'kioskApp',
    'appengine_emailbackend',
    'filetransfers',
    'suds',
    'spyne',
    'pytz',
    'lxml',
    'rpctest',
    )

MIDDLEWARE_CLASSES = (
    # This loads the index definitions, so it has to come first
    'autoload.middleware.AutoloadMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    )
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #     'django.template.loaders.eggs.Loader',
    )

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    )

# This test runner captures stdout and associates tracebacks with their
# corresponding output. Helps a lot with print-debugging.
TEST_RUNNER = 'djangotoolbox.test.CapturingTestSuiteRunner'

ADMIN_MEDIA_PREFIX = '/media/admin/'
PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))
TEMPLATE_DIRS = (#os.path.join(os.path.dirname(__file__), 'templates'),
                 #os.path.join(os.path.dirname(__file__), '/kioskApp/templates/'),
                 #os.path.join(os.path.dirname(__file__), '/kioskApp/templatetags/'),
                 #os.path.join(os.path.dirname(__file__), '/dojango/templates/'),
                 #os.path.join(os.path.dirname(__file__), '/dojango/templatetags/'))
                 PROJECT_PATH + '/dojango/templates/',
                 PROJECT_PATH + '/dojango/templatetags/',
                 PROJECT_PATH + '/kioskApp/templatetags/',
                 PROJECT_PATH + '/kioskApp/templates/',
    )

ROOT_URLCONF = 'urls'
