from django.conf.urls.defaults import *
#from captcha import urls


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^simplebtt/', include('simplebtt.foo.urls')),
    (r'^announce/$', 'simplebtt.tracker.announce.main'),

    (r'^$', 'simplebtt.tracker.views.torrent_list'),
    (r'^(?P<page>\d{1,3})/$', 'simplebtt.tracker.views.torrent_list'),
    (r'^category/(?P<category>\w{1,50})/$', 'simplebtt.tracker.views.torrent_list'),
    (r'^category/(?P<category>\w{1,50})/(?P<page>\d{1,3})/$', 'simplebtt.tracker.views.torrent_list'),

    (r'^info/(\d{1,4})/$', 'simplebtt.tracker.views.torrent_info'),
    (r'^search/', 'simplebtt.tracker.views.search'),
    (r'^add/$','simplebtt.tracker.views.torrent_add'),

    #(r'^auth/', include('simplebtt.account.urls')),
#    (r'tracker/', include('simplebtt.tracker.urls') ),



    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     (r'^admin/(.*)', admin.site.root),
)
