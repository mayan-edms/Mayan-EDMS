from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('maintenance.views',
    url(r'^$', 'maintenance_menu', (), 'maintenance_menu'),
    url(r'^execute/(?P<maintenante_tool_id>\w+)/$', 'maintenance_execute', (), 'maintenance_execute'),
)
