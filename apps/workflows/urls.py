from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('workflows.views',
    url(r'^setup/workflow/list/$', 'setup_workflow_list', (), 'setup_workflow_list'),
    url(r'^setup/workflow/create/$', 'setup_workflow_create', (), 'setup_workflow_create'),
    url(r'^setup/workflow/(?P<workflow_pk>\d+)/edit/$', 'setup_workflow_edit', (), 'setup_workflow_edit'),
    url(r'^setup/workflow/(?P<workflow_pk>\d+)/delete/$', 'setup_workflow_delete', (), 'setup_workflow_delete'),

    url(r'^setup/state/list/$', 'setup_state_list', (), 'setup_state_list'),
    url(r'^setup/state/create/$', 'setup_state_create', (), 'setup_state_create'),
    url(r'^setup/state/(?P<state_pk>\d+)/edit/$', 'setup_state_edit', (), 'setup_state_edit'),
    url(r'^setup/state/(?P<state_pk>\d+)/delete/$', 'setup_state_delete', (), 'setup_state_delete'),
)
