from __future__ import unicode_literals

from django.conf.urls import url

from .api_views import (
    APIDocumentTypeWorkflowListView, APIWorkflowDocumentTypeList,
    APIWorkflowDocumentTypeView, APIWorkflowInstanceListView,
    APIWorkflowInstanceView, APIWorkflowInstanceLogEntryListView,
    APIWorkflowListView, APIWorkflowStateListView, APIWorkflowStateView,
    APIWorkflowTransitionListView, APIWorkflowTransitionView, APIWorkflowView
)
from .views import (
    DocumentWorkflowInstanceListView, SetupWorkflowCreateView,
    SetupWorkflowDeleteView, SetupWorkflowDocumentTypesView,
    SetupWorkflowEditView, SetupWorkflowListView,
    SetupWorkflowStateActionCreateView, SetupWorkflowStateActionDeleteView,
    SetupWorkflowStateActionEditView, SetupWorkflowStateActionListView,
    SetupWorkflowStateActionSelectionView, SetupWorkflowStateCreateView,
    SetupWorkflowStateDeleteView, SetupWorkflowStateEditView,
    SetupWorkflowStateListView, SetupWorkflowTransitionListView,
    SetupWorkflowTransitionCreateView, SetupWorkflowTransitionDeleteView,
    SetupWorkflowTransitionEditView,
    SetupWorkflowTransitionTriggerEventListView, ToolLaunchAllWorkflows,
    WorkflowDocumentListView, WorkflowInstanceDetailView,
    WorkflowImageView, WorkflowInstanceTransitionView, WorkflowListView,
    WorkflowPreviewView, WorkflowStateDocumentListView, WorkflowStateListView,
)
from .views.workflow_views import SetupDocumentTypeWorkflowsView

urlpatterns_workflows = [
    url(
        regex=r'^document_type/(?P<pk>\d+)/workflows/$',
        view=SetupDocumentTypeWorkflowsView.as_view(),
        name='document_type_workflows'
    ),
]

urlpatterns = [
    url(
        regex=r'^document/(?P<pk>\d+)/workflows/$',
        view=DocumentWorkflowInstanceListView.as_view(),
        name='document_workflow_instance_list'
    ),
    url(
        regex=r'^document/workflows/(?P<pk>\d+)/$',
        view=WorkflowInstanceDetailView.as_view(),
        name='workflow_instance_detail'
    ),
    url(
        regex=r'^document/workflows/(?P<pk>\d+)/transition/$',
        view=WorkflowInstanceTransitionView.as_view(),
        name='workflow_instance_transition'
    ),
    url(
        regex=r'^setup/all/$', view=SetupWorkflowListView.as_view(),
        name='setup_workflow_list'
    ),
    url(
        regex=r'^setup/create/$', view=SetupWorkflowCreateView.as_view(),
        name='setup_workflow_create'
    ),
    url(
        regex=r'^setup/workflow/(?P<pk>\d+)/edit/$',
        view=SetupWorkflowEditView.as_view(), name='setup_workflow_edit'
    ),
    url(
        regex=r'^setup/workflow/(?P<pk>\d+)/delete/$',
        view=SetupWorkflowDeleteView.as_view(), name='setup_workflow_delete'
    ),
    url(
        regex=r'^setup/workflow/(?P<pk>\d+)/documents/$',
        view=WorkflowDocumentListView.as_view(),
        name='setup_workflow_document_list'
    ),
    url(
        regex=r'^setup/workflow/(?P<pk>\d+)/document_types/$',
        view=SetupWorkflowDocumentTypesView.as_view(),
        name='setup_workflow_document_types'
    ),
    url(
        regex=r'^setup/workflow/(?P<pk>\d+)/states/$',
        view=SetupWorkflowStateListView.as_view(),
        name='setup_workflow_state_list'
    ),
    url(
        regex=r'^setup/workflow/(?P<pk>\d+)/states/create/$',
        view=SetupWorkflowStateCreateView.as_view(),
        name='setup_workflow_state_create'
    ),
    url(
        regex=r'^setup/workflow/(?P<pk>\d+)/transitions/$',
        view=SetupWorkflowTransitionListView.as_view(),
        name='setup_workflow_transition_list'
    ),
    url(
        regex=r'^setup/workflow/(?P<pk>\d+)/transitions/create/$',
        view=SetupWorkflowTransitionCreateView.as_view(),
        name='setup_workflow_transition_create'
    ),
    url(
        regex=r'^setup/workflow/(?P<pk>\d+)/transitions/events/$',
        view=SetupWorkflowTransitionTriggerEventListView.as_view(),
        name='setup_workflow_transition_events'
    ),
    url(
        regex=r'^setup/workflow/state/(?P<pk>\d+)/delete/$',
        view=SetupWorkflowStateDeleteView.as_view(),
        name='setup_workflow_state_delete'
    ),
    url(
        regex=r'^setup/workflow/state/(?P<pk>\d+)/edit/$',
        view=SetupWorkflowStateEditView.as_view(),
        name='setup_workflow_state_edit'
    ),
    url(
        regex=r'^setup/workflow/state/(?P<pk>\d+)/actions/$',
        view=SetupWorkflowStateActionListView.as_view(),
        name='setup_workflow_state_action_list'
    ),
    url(
        regex=r'^setup/workflow/state/(?P<pk>\d+)/actions/selection/$',
        view=SetupWorkflowStateActionSelectionView.as_view(),
        name='setup_workflow_state_action_selection'
    ),
    url(
        regex=r'^setup/workflow/state/(?P<pk>\d+)/actions/(?P<class_path>[a-zA-Z0-9_.]+)/create/$',
        view=SetupWorkflowStateActionCreateView.as_view(),
        name='setup_workflow_state_action_create'
    ),
    url(
        regex=r'^setup/workflow/state/actions/(?P<pk>\d+)/delete/$',
        view=SetupWorkflowStateActionDeleteView.as_view(),
        name='setup_workflow_state_action_delete'
    ),
    url(
        regex=r'^setup/workflow/state/actions/(?P<pk>\d+)/edit/$',
        view=SetupWorkflowStateActionEditView.as_view(),
        name='setup_workflow_state_action_edit'
    ),
    url(
        regex=r'^setup/workflow/transitions/(?P<pk>\d+)/delete/$',
        view=SetupWorkflowTransitionDeleteView.as_view(),
        name='setup_workflow_transition_delete'
    ),
    url(
        regex=r'^setup/workflow/transitions/(?P<pk>\d+)/edit/$',
        view=SetupWorkflowTransitionEditView.as_view(),
        name='setup_workflow_transition_edit'
    ),
    url(
        regex=r'^tools/workflow/all/launch/$',
        view=ToolLaunchAllWorkflows.as_view(),
        name='tool_launch_all_workflows'
    ),
    url(
        regex=r'all/$',
        view=WorkflowListView.as_view(),
        name='workflow_list'
    ),
    url(
        regex=r'^(?P<pk>\d+)/documents/$',
        view=WorkflowDocumentListView.as_view(),
        name='workflow_document_list'
    ),
    url(
        regex=r'^(?P<pk>\d+)/states/$',
        view=WorkflowStateListView.as_view(),
        name='workflow_state_list'
    ),
    url(
        regex=r'^(?P<pk>\d+)/image/$',
        view=WorkflowImageView.as_view(),
        name='workflow_image'
    ),
    url(
        regex=r'^(?P<pk>\d+)/preview/$',
        view=WorkflowPreviewView.as_view(),
        name='workflow_preview'
    ),
    url(
        regex=r'^state/(?P<pk>\d+)/documents/$',
        view=WorkflowStateDocumentListView.as_view(),
        name='workflow_state_document_list'
    ),
]
urlpatterns.extend(urlpatterns_workflows)

api_urls = [
    url(
        regex=r'^workflows/$', view=APIWorkflowListView.as_view(),
        name='workflow-list'
    ),
    url(
        regex=r'^workflows/(?P<pk>[0-9]+)/$', view=APIWorkflowView.as_view(),
        name='workflow-detail'
    ),
    url(
        regex=r'^workflows/(?P<pk>[0-9]+)/document_types/$',
        view=APIWorkflowDocumentTypeList.as_view(),
        name='workflow-document-type-list'
    ),
    url(
        regex=r'^workflows/(?P<pk>[0-9]+)/document_types/(?P<document_type_pk>[0-9]+)/$',
        view=APIWorkflowDocumentTypeView.as_view(),
        name='workflow-document-type-detail'
    ),
    url(
        regex=r'^workflows/(?P<pk>[0-9]+)/states/$',
        view=APIWorkflowStateListView.as_view(), name='workflowstate-list'
    ),
    url(
        regex=r'^workflows/(?P<pk>[0-9]+)/states/(?P<state_pk>[0-9]+)/$',
        view=APIWorkflowStateView.as_view(), name='workflowstate-detail'
    ),
    url(
        regex=r'^workflows/(?P<pk>[0-9]+)/transitions/$',
        view=APIWorkflowTransitionListView.as_view(),
        name='workflowtransition-list'
    ),
    url(
        regex=r'^workflows/(?P<pk>[0-9]+)/transitions/(?P<transition_pk>[0-9]+)/$',
        view=APIWorkflowTransitionView.as_view(),
        name='workflowtransition-detail'
    ),
    url(
        regex=r'^documents/(?P<pk>[0-9]+)/workflows/$',
        view=APIWorkflowInstanceListView.as_view(),
        name='workflowinstance-list'
    ),
    url(
        regex=r'^documents/(?P<pk>[0-9]+)/workflows/(?P<workflow_pk>[0-9]+)/$',
        view=APIWorkflowInstanceView.as_view(),
        name='workflowinstance-detail'
    ),
    url(
        regex=r'^documents/(?P<pk>[0-9]+)/workflows/(?P<workflow_pk>[0-9]+)/log_entries/$',
        view=APIWorkflowInstanceLogEntryListView.as_view(),
        name='workflowinstancelogentry-list'
    ),
    url(
        regex=r'^document_types/(?P<pk>[0-9]+)/workflows/$',
        view=APIDocumentTypeWorkflowListView.as_view(),
        name='documenttype-workflow-list'
    ),
]
