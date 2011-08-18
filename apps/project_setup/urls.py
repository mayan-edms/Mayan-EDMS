from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('project_setup.views',
    url(r'^list/$', 'setup_list', (), 'setup_list'),
)
