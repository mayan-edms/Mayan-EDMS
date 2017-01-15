from __future__ import unicode_literals

from django.conf.urls import url

from .views import (
    DocumentWorkflowInstanceListView, SetupWorkflowCreateView,
    SetupWorkflowDeleteView, SetupWorkflowDocumentTypesView,
    SetupWorkflowEditView, SetupWorkflowListView,
    SetupWorkflowStateCreateView, SetupWorkflowStateDeleteView,
    SetupWorkflowStateEditView, SetupWorkflowStateListView,
    SetupWorkflowTransitionListView, SetupWorkflowTransitionCreateView,
    SetupWorkflowTransitionDeleteView, SetupWorkflowTransitionEditView,
    WorkflowDocumentListView, WorkflowInstanceDetailView,
    WorkflowInstanceTransitionView
)

urlpatterns = [
    url(
        r'^document/(?P<pk>\d+)/workflows/$',
        DocumentWorkflowInstanceListView.as_view(),
        name='document_workflow_instance_list'
    ),
    url(
        r'^document/workflows/(?P<pk>\d+)/$',
        WorkflowInstanceDetailView.as_view(), name='workflow_instance_detail'
    ),
    url(
        r'^document/workflows/(?P<pk>\d+)/transition/$',
        WorkflowInstanceTransitionView.as_view(),
        name='workflow_instance_transition'
    ),

    url(
        r'^setup/all/$', SetupWorkflowListView.as_view(),
        name='setup_workflow_list'
    ),
    url(
        r'^setup/create/$', SetupWorkflowCreateView.as_view(),
        name='setup_workflow_create'
    ),
    url(
        r'^setup/(?P<pk>\d+)/edit/$', SetupWorkflowEditView.as_view(),
        name='setup_workflow_edit'
    ),
    url(
        r'^setup/(?P<pk>\d+)/delete/$', SetupWorkflowDeleteView.as_view(),
        name='setup_workflow_delete'
    ),
    url(
        r'^setup/(?P<pk>\d+)/documents/$',
        WorkflowDocumentListView.as_view(),
        name='setup_workflow_document_list'
    ),
    url(
        r'^setup/(?P<pk>\d+)/document_types/$',
        SetupWorkflowDocumentTypesView.as_view(),
        name='setup_workflow_document_types'
    ),
    url(
        r'^setup/(?P<pk>\d+)/states/$', SetupWorkflowStateListView.as_view(),
        name='setup_workflow_states'
    ),
    url(
        r'^setup/(?P<pk>\d+)/states/create/$',
        SetupWorkflowStateCreateView.as_view(),
        name='setup_workflow_state_create'
    ),
    url(
        r'^setup/(?P<pk>\d+)/transitions/$',
        SetupWorkflowTransitionListView.as_view(),
        name='setup_workflow_transitions'
    ),
    url(
        r'^setup/(?P<pk>\d+)/transitions/create/$',
        SetupWorkflowTransitionCreateView.as_view(),
        name='setup_workflow_transition_create'
    ),
    url(
        r'^setup/workflow/state/(?P<pk>\d+)/delete/$',
        SetupWorkflowStateDeleteView.as_view(),
        name='setup_workflow_state_delete'
    ),
    url(
        r'^setup/workflow/state/(?P<pk>\d+)/edit/$',
        SetupWorkflowStateEditView.as_view(),
        name='setup_workflow_state_edit'
    ),
    url(
        r'^setup/workflow/transitions/(?P<pk>\d+)/delete/$',
        SetupWorkflowTransitionDeleteView.as_view(),
        name='setup_workflow_transition_delete'
    ),
    url(
        r'^setup/workflow/transitions/(?P<pk>\d+)/edit/$',
        SetupWorkflowTransitionEditView.as_view(),
        name='setup_workflow_transition_edit'
    ),
]
