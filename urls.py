from django.conf.urls.defaults import *


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^simplebtt/', include('simplebtt.foo.urls')),
    (r'^announce/$', 'simplebtt.tracker.announce.main'),
    (r'^$', 'simplebtt.tracker.views.torrent_list'),
    (r'^info/(\d{1,4})$', 'simplebtt.tracker.views.torrent_info'),


#    (r'^add/$','simplebtt.tracker.views.upload_torrent'),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     (r'^admin/(.*)', admin.site.root),
)
