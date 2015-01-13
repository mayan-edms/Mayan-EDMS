from django.conf.urls import patterns, url

from .views import (SetupWorkflowCreateView, SetupWorkflowDeleteView,
                    SetupWorkflowEditView, SetupWorkflowListView,
                    SetupWorkflowStateListView, SetupWorkflowStateCreateView,
                    SetupWorkflowTransitionListView, SetupWorkflowTransitionCreateView,
                    DocumentWorkflowListView)

urlpatterns = patterns('',
    url(r'^setup/all/$', SetupWorkflowListView.as_view(), name='setup_workflow_list'),
    url(r'^setup/create/$', SetupWorkflowCreateView.as_view(), name='setup_workflow_create'),
    url(r'^setup/(?P<pk>\d+)/edit/$', SetupWorkflowEditView.as_view(), name='setup_workflow_edit'),
    url(r'^setup/(?P<pk>\d+)/delete/$', SetupWorkflowDeleteView.as_view(), name='setup_workflow_delete'),
    url(r'^setup/(?P<pk>\d+)/states/$', SetupWorkflowStateListView.as_view(), name='setup_workflow_states'),
    url(r'^setup/(?P<pk>\d+)/states/create/$', SetupWorkflowStateCreateView.as_view(), name='setup_workflow_states_create'),

    url(r'^setup/(?P<pk>\d+)/transitions/$', SetupWorkflowTransitionListView.as_view(), name='setup_workflow_transitions'),
    url(r'^setup/(?P<pk>\d+)/transitions/create/$', SetupWorkflowTransitionCreateView.as_view(), name='setup_workflow_transitions_create'),

    url(r'^document/(?P<pk>\d+)/workflows/$', DocumentWorkflowListView.as_view(), name='document_workflow_list'),
)

urlpatterns += patterns('document_states.views',
    url(r'^setup/(?P<pk>\d+)/document_types/$', 'setup_workflow_document_types', name='setup_workflow_document_types'),
)


