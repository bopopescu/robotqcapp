from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
admin.autodiscover()
import kioskApp.views
import settings
urlpatterns = patterns('',
    (r'^$', kioskApp.views.login_user),
    (r'^contact/$',kioskApp.views.contact_form),
    (r'^customers/$',kioskApp.views.customersPage),
    (r'^new_customer/$',kioskApp.views.new_customer),
    (r'^new_user/$',kioskApp.views.new_user),
    (r'^logout/$',kioskApp.views.logout_view),
    (r'^customers/(?P<cust_id>\d+)$',kioskApp.views.customer_page),
    (r'^customers/(?P<cust_id>\d+)/transactionPost$',kioskApp.views.submitTransaction),
    (r'^customers/getVilageDebt/$',kioskApp.views.customersPage),
    #media
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),
    # (r'^s3FileDownload/(?P<s3FileId>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),
    (r'^s3FileDownload/(?P<s3FileId>.*)$', kioskApp.views.s3FileDownload),
)