from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('workflows.views',
    url(r'^setup/list/$', 'setup_workflow_list', (), 'setup_workflow_list'),
)
