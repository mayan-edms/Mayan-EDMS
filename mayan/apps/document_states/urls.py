from __future__ import unicode_literals

from django.conf.urls import url

from .api_views import (
    APIDocumentTypeWorkflowRuntimeProxyListView, APIWorkflowDocumentTypeList,
    APIWorkflowDocumentTypeView, APIWorkflowImageView,
    APIWorkflowInstanceListView, APIWorkflowInstanceView,
    APIWorkflowInstanceLogEntryListView, APIWorkflowRuntimeProxyListView,
    APIWorkflowStateListView, APIWorkflowStateView,
    APIWorkflowTransitionListView, APIWorkflowTransitionView, APIWorkflowView
)
from .views.workflow_instance_views import (
    WorkflowInstanceDetailView, WorkflowInstanceListView,
    WorkflowInstanceTransitionSelectView,
    WorkflowInstanceTransitionExecuteView
)
from .views.workflow_proxy_views import (
    WorkflowRuntimeProxyDocumentListView,
    WorkflowRuntimeProxyListView, WorkflowRuntimeProxyStateDocumentListView,
    WorkflowRuntimeProxyStateListView
)
from .views.workflow_template_views import (
    DocumentTypeWorkflowTemplatesView, ToolLaunchWorkflows,
    WorkflowTemplateCreateView, WorkflowTemplateDeleteView,
    WorkflowTemplateEditView, WorkflowTemplateListView,
    WorkflowTemplatePreviewView, WorkflowTemplateDocumentTypesView
)
from .views.workflow_template_state_views import (
    WorkflowTemplateStateActionCreateView,
    WorkflowTemplateStateActionDeleteView, WorkflowTemplateStateActionEditView,
    WorkflowTemplateStateActionListView,
    WorkflowTemplateStateActionSelectionView, WorkflowTemplateStateCreateView,
    WorkflowTemplateStateDeleteView, WorkflowTemplateStateEditView,
    WorkflowTemplateStateListView
)
from .views.workflow_template_transition_views import (
    WorkflowTemplateTransitionCreateView, WorkflowTemplateTransitionDeleteView,
    WorkflowTemplateTransitionEditView, WorkflowTemplateTransitionListView,
    WorkflowTemplateTransitionTriggerEventListView,
    WorkflowTemplateTransitionFieldCreateView,
    WorkflowTemplateTransitionFieldDeleteView,
    WorkflowTemplateTransitionFieldEditView,
    WorkflowTemplateTransitionFieldListView
)

urlpatterns_workflow_instances = [
    url(
        regex=r'^documents/(?P<pk>\d+)/workflows/$',
        view=WorkflowInstanceListView.as_view(),
        name='workflow_instance_list'
    ),
    url(
        regex=r'^documents/workflows/(?P<pk>\d+)/$',
        view=WorkflowInstanceDetailView.as_view(),
        name='workflow_instance_detail'
    ),
    url(
        regex=r'^documents/workflows/(?P<pk>\d+)/transitions/select/$',
        view=WorkflowInstanceTransitionSelectView.as_view(),
        name='workflow_instance_transition_selection'
    ),
    url(
        regex=r'^documents/workflows/(?P<workflow_instance_pk>\d+)/transitions/(?P<workflow_transition_pk>\d+)/execute/$',
        view=WorkflowInstanceTransitionExecuteView.as_view(),
        name='workflow_instance_transition_execute'
    ),
]

urlpatterns_workflow_runtime_proxies = [
    url(
        regex=r'workflow_runtime_proxies/$',
        view=WorkflowRuntimeProxyListView.as_view(),
        name='workflow_runtime_proxy_list'
    ),
    url(
        regex=r'^workflow_runtime_proxies/(?P<pk>\d+)/documents/$',
        view=WorkflowRuntimeProxyDocumentListView.as_view(),
        name='workflow_runtime_proxy_document_list'
    ),
    url(
        regex=r'^workflow_runtime_proxies/(?P<pk>\d+)/states/$',
        view=WorkflowRuntimeProxyStateListView.as_view(),
        name='workflow_runtime_proxy_state_list'
    ),
    url(
        regex=r'^workflow_runtime_proxies/states/(?P<pk>\d+)/documents/$',
        view=WorkflowRuntimeProxyStateDocumentListView.as_view(),
        name='workflow_runtime_proxy_state_document_list'
    ),
]

urlpatterns_workflow_states = [
    url(
        regex=r'^workflow_templates/(?P<pk>\d+)/states/$',
        view=WorkflowTemplateStateListView.as_view(),
        name='workflow_template_state_list'
    ),
    url(
        regex=r'^workflow_templates/(?P<pk>\d+)/states/create/$',
        view=WorkflowTemplateStateCreateView.as_view(),
        name='workflow_template_state_create'
    ),
    url(
        regex=r'^workflow_templates/states/(?P<pk>\d+)/delete/$',
        view=WorkflowTemplateStateDeleteView.as_view(),
        name='workflow_template_state_delete'
    ),
    url(
        regex=r'^workflow_templates/states/(?P<pk>\d+)/edit/$',
        view=WorkflowTemplateStateEditView.as_view(),
        name='workflow_template_state_edit'
    ),
]

urlpatterns_workflow_state_actions = [
    url(
        regex=r'^workflow_templates/states/(?P<pk>\d+)/actions/$',
        view=WorkflowTemplateStateActionListView.as_view(),
        name='workflow_template_state_action_list'
    ),
    url(
        regex=r'^workflow_templates/states/(?P<pk>\d+)/actions/selection/$',
        view=WorkflowTemplateStateActionSelectionView.as_view(),
        name='workflow_template_state_action_selection'
    ),
    url(
        regex=r'^workflow_templates/states/(?P<pk>\d+)/actions/(?P<class_path>[a-zA-Z0-9_.]+)/create/$',
        view=WorkflowTemplateStateActionCreateView.as_view(),
        name='workflow_template_state_action_create'
    ),
    url(
        regex=r'^workflow_templates/states/actions/(?P<pk>\d+)/delete/$',
        view=WorkflowTemplateStateActionDeleteView.as_view(),
        name='workflow_template_state_action_delete'
    ),
    url(
        regex=r'^workflow_templates/states/actions/(?P<pk>\d+)/edit/$',
        view=WorkflowTemplateStateActionEditView.as_view(),
        name='workflow_template_state_action_edit'
    ),
]

urlpatterns_workflow_templates = [
    url(
        regex=r'^workflow_templates/$', view=WorkflowTemplateListView.as_view(),
        name='workflow_template_list'
    ),
    url(
        regex=r'^workflow_templates/create/$', view=WorkflowTemplateCreateView.as_view(),
        name='workflow_template_create'
    ),
    url(
        regex=r'^workflow_templates/(?P<pk>\d+)/delete/$',
        view=WorkflowTemplateDeleteView.as_view(), name='workflow_template_delete'
    ),
    url(
        regex=r'^workflow_templates/(?P<pk>\d+)/document_types/$',
        view=WorkflowTemplateDocumentTypesView.as_view(),
        name='workflow_template_document_types'
    ),
    url(
        regex=r'^workflow_templates/(?P<pk>\d+)/edit/$',
        view=WorkflowTemplateEditView.as_view(), name='workflow_template_edit'
    ),
    url(
        regex=r'^workflow_templates/(?P<pk>\d+)/preview/$',
        view=WorkflowTemplatePreviewView.as_view(),
        name='workflow_template_preview'
    ),
    url(
        regex=r'^document_types/(?P<pk>\d+)/workflow_templates/$',
        view=DocumentTypeWorkflowTemplatesView.as_view(),
        name='document_type_workflow_templates'
    ),
]
urlpatterns_workflow_transitions = [
    url(
        regex=r'^workflow_templates/(?P<pk>\d+)/transitions/$',
        view=WorkflowTemplateTransitionListView.as_view(),
        name='workflow_template_transition_list'
    ),
    url(
        regex=r'^workflow_templates/(?P<pk>\d+)/transitions/create/$',
        view=WorkflowTemplateTransitionCreateView.as_view(),
        name='workflow_template_transition_create'
    ),
    url(
        regex=r'^workflow_templates/(?P<pk>\d+)/transitions/events/$',
        view=WorkflowTemplateTransitionTriggerEventListView.as_view(),
        name='workflow_template_transition_events'
    ),
    url(
        regex=r'^workflow_templates/transitions/(?P<pk>\d+)/delete/$',
        view=WorkflowTemplateTransitionDeleteView.as_view(),
        name='workflow_template_transition_delete'
    ),
    url(
        regex=r'^workflow_templates/transitions/(?P<pk>\d+)/edit/$',
        view=WorkflowTemplateTransitionEditView.as_view(),
        name='workflow_template_transition_edit'
    ),
]

urlpatterns_workflow_transition_fields = [
    url(
        regex=r'^workflow_templates/transitions/(?P<pk>\d+)/fields/create/$',
        view=WorkflowTemplateTransitionFieldCreateView.as_view(),
        name='workflow_template_transition_field_create'
    ),
    url(
        regex=r'^workflow_templates/transitions/(?P<pk>\d+)/fields/$',
        view=WorkflowTemplateTransitionFieldListView.as_view(),
        name='workflow_template_transition_field_list'
    ),
    url(
        regex=r'^workflow_templates/transitions/fields/(?P<pk>\d+)/delete/$',
        view=WorkflowTemplateTransitionFieldDeleteView.as_view(),
        name='workflow_template_transition_field_delete'
    ),
    url(
        regex=r'^workflow_templates/transitions/fields/(?P<pk>\d+)/edit/$',
        view=WorkflowTemplateTransitionFieldEditView.as_view(),
        name='workflow_template_transition_field_edit'
    ),
]

urlpatterns_tools = [
    url(
        regex=r'^tools/workflows/launch/$',
        view=ToolLaunchWorkflows.as_view(),
        name='tool_launch_workflows'
    ),
]

urlpatterns = []
urlpatterns.extend(urlpatterns_tools)
urlpatterns.extend(urlpatterns_workflow_instances)
urlpatterns.extend(urlpatterns_workflow_runtime_proxies)
urlpatterns.extend(urlpatterns_workflow_states)
urlpatterns.extend(urlpatterns_workflow_state_actions)
urlpatterns.extend(urlpatterns_workflow_templates)
urlpatterns.extend(urlpatterns_workflow_transitions)
urlpatterns.extend(urlpatterns_workflow_transition_fields)

api_urls = [
    url(
        regex=r'^workflows/$', view=APIWorkflowRuntimeProxyListView.as_view(),
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
        regex=r'^workflows/(?P<pk>\d+)/image/$',
        name='workflow-image', view=APIWorkflowImageView.as_view()
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
        view=APIDocumentTypeWorkflowRuntimeProxyListView.as_view(),
        name='documenttype-workflow-list'
    ),
]
