from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('workflows.views',
    url(r'^setup/workflow/list/$', 'setup_workflow_list', (), 'setup_workflow_list'),
    url(r'^setup/workflow/create/$', 'setup_workflow_create', (), 'setup_workflow_create'),
    url(r'^setup/workflow/(?P<workflow_pk>\d+)/edit/$', 'setup_workflow_edit', (), 'setup_workflow_edit'),
    url(r'^setup/workflow/(?P<workflow_pk>\d+)/delete/$', 'setup_workflow_delete', (), 'setup_workflow_delete'),
    url(r'^setup/workflow/(?P<workflow_pk>\d+)/state/list/$', 'setup_workflow_states_list', (), 'setup_workflow_states_list'),
    url(r'^setup/workflow/(?P<workflow_pk>\d+)/state/create/$', 'setup_workflow_state_add', (), 'setup_workflow_state_add'),
    url(r'^setup/workflow/state/(?P<workflow_state_pk>\d+)/edit/$', 'setup_workflow_state_edit', (), 'setup_workflow_state_edit'),
    url(r'^setup/workflow/state/(?P<workflow_state_pk>\d+)/remove/$', 'setup_workflow_state_remove', (), 'setup_workflow_state_remove'),

    url(r'^setup/state/list/$', 'setup_state_list', (), 'setup_state_list'),
    url(r'^setup/state/create/$', 'setup_state_create', (), 'setup_state_create'),
    url(r'^setup/state/(?P<state_pk>\d+)/edit/$', 'setup_state_edit', (), 'setup_state_edit'),
    url(r'^setup/state/(?P<state_pk>\d+)/delete/$', 'setup_state_delete', (), 'setup_state_delete'),
    
    url(r'^setup/transition/list/$', 'setup_transition_list', (), 'setup_transition_list'),
    url(r'^setup/transition/create/$', 'setup_transition_create', (), 'setup_transition_create'),
    url(r'^setup/transition/(?P<transition_pk>\d+)/edit/$', 'setup_transition_edit', (), 'setup_transition_edit'),
    url(r'^setup/transition/(?P<transition_pk>\d+)/delete/$', 'setup_transition_delete', (), 'setup_transition_delete'),
    
)
