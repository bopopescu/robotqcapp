from django.conf.urls.defaults import patterns, include, url
import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    ### Index Main Page ###
    (r'^$', 'kioskApp.views.index'),
    (r'^plate/$','kioskApp.views.plate'),
    url(r'^helloworld/', 'rpctest.core.views.hello_world_service'),
    (r'^new_experiment/$','kioskApp.views.new_experiment'),
    (r'^tutorial/$','kioskApp.views.tutorial'),
    (r'^experiments/download_exp_files/(?P<exp_id>\d+)$','kioskApp.views.downloadExperimentFiles'),
    (r'^new_plate_plastica/$','kioskApp.views.new_plateplastica'),
    (r'^fileTest/$','kioskApp.views.fileTest'),
    (r'^experiments/$','kioskApp.views.experimentsPage'),
    (r'^experiments/(?P<exp_id>\d+)$','kioskApp.views.experimentpage'),
    (r'^experiments/experiment/(?P<expId>\d+)/$','kioskApp.views.downloadExperimentFiles'),
    (r'^log/$','kioskApp.views.log_handler'),
    (r'^new_user/$','kioskApp.views.new_user'),
   # (r'^robot_scripts_page/$','kioskApp.views.scriptsIndex'),
    (r'^robot_scripts_page/$','kioskApp.views.scripts_page'),
    (r'^robot_scripts_page/scripts_report/$','kioskApp.views.scripts_report'),
    (r'^robot_scripts_page/(?P<script_id>\d+)$','kioskApp.views.script_page'),
    (r'^robot_scripts_page/robotscript/(?P<error_id>\d+)$','kioskApp.views.error_page'),
    (r'^logout/$','kioskApp.views.logout_view'),
    (r'^search_name$','kioskApp.views.search_name'),
    (r'^liquid_class_volume_chart/$','kioskApp.views.viewLiquidClassChart'),
    (r'^post_liquid_class_volume_chart/$','kioskApp.views.postViewLiquidClassChart'),
    ### Admin
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^dojango/', include('dojango.urls')),

    #media
    url(r'^download/(?P<pk>\d+)$','kioskApp.views.download_handler'),
    url(r'^download_as_txt/(?P<pk>\d+)$','kioskApp.views.download_as_txt_handler'),
    url(r'^download_as_xls/(?P<pk>\d+)$','kioskApp.views.download_as_xls_handler'),
    url(r'^upload/$','kioskApp.views.upload_handler'),
)
