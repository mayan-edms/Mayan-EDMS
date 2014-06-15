from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('project_tools.views',
    url(r'^list/$', 'tools_list', (), 'tools_list'),
)
