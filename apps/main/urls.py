from django.conf.urls.defaults import *


urlpatterns = patterns('main.views',
    url(r'^$', 'home', (), 'home'),
    url(r'^check_settings/$', 'check_settings', (), 'check_settings'),
    url(r'^tools_menu/$', 'blank_menu', (), 'tools_menu')
)
