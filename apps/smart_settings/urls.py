from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('smart_settings.views',
    url(r'^list/(?P<app_name>\w+)/$', 'setting_list', (), 'setting_list'),
    url(r'^list/$', 'setting_list', (), 'setting_list'),
)
