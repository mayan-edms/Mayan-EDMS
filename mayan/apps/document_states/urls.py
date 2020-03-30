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
    WorkflowTemplateEditView, WorkflowTemplateLaunchView,
    WorkflowTemplateListView, WorkflowTemplatePreviewView,
    WorkflowTemplateDocumentTypesView
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
        regex=r'^documents/(?P<document_id>\d+)/workflows/$',
        name='workflow_instance_list',
        view=WorkflowInstanceListView.as_view()
    ),
    url(
        regex=r'^documents/workflows/(?P<workflow_instance_id>\d+)/$',
        name='workflow_instance_detail',
        view=WorkflowInstanceDetailView.as_view()
    ),
    url(
        regex=r'^documents/workflows/(?P<workflow_instance_id>\d+)/transitions/select/$',
        name='workflow_instance_transition_selection',
        view=WorkflowInstanceTransitionSelectView.as_view()
    ),
    url(
        regex=r'^documents/workflows/(?P<workflow_instance_id>\d+)/transitions/(?P<workflow_transition_id>\d+)/execute/$',
        name='workflow_instance_transition_execute',
        view=WorkflowInstanceTransitionExecuteView.as_view()
    )
]

urlpatterns_workflow_runtime_proxies = [
    url(
        regex=r'workflow_runtime_proxies/$',
        name='workflow_runtime_proxy_list',
        view=WorkflowRuntimeProxyListView.as_view()
    ),
    url(
        regex=r'^workflow_runtime_proxies/(?P<workflow_runtime_proxy_id>\d+)/documents/$',
        name='workflow_runtime_proxy_document_list',
        view=WorkflowRuntimeProxyDocumentListView.as_view()
    ),
    url(
        regex=r'^workflow_runtime_proxies/(?P<workflow_runtime_proxy_id>\d+)/states/$',
        name='workflow_runtime_proxy_state_list',
        view=WorkflowRuntimeProxyStateListView.as_view()
    ),
    url(
        regex=r'^workflow_runtime_proxies/states/(?P<workflow_runtime_proxy_state_id>\d+)/documents/$',
        name='workflow_runtime_proxy_state_document_list',
        view=WorkflowRuntimeProxyStateDocumentListView.as_view()
    )
]

urlpatterns_workflow_states = [
    url(
        regex=r'^workflow_templates/(?P<workflow_template_id>\d+)/states/$',
        name='workflow_template_state_list',
        view=WorkflowTemplateStateListView.as_view()
    ),
    url(
        regex=r'^workflow_templates/(?P<workflow_template_id>\d+)/states/create/$',
        name='workflow_template_state_create',
        view=WorkflowTemplateStateCreateView.as_view()
    ),
    url(
        regex=r'^workflow_templates/states/(?P<workflow_template_state_id>\d+)/delete/$',
        name='workflow_template_state_delete',
        view=WorkflowTemplateStateDeleteView.as_view()
    ),
    url(
        regex=r'^workflow_templates/states/(?P<workflow_template_state_id>\d+)/edit/$',
        name='workflow_template_state_edit',
        view=WorkflowTemplateStateEditView.as_view()
    )
]

urlpatterns_workflow_state_actions = [
    url(
        regex=r'^workflow_templates/states/(?P<workflow_template_state_id>\d+)/actions/$',
        name='workflow_template_state_action_list',
        view=WorkflowTemplateStateActionListView.as_view()
    ),
    url(
        regex=r'^workflow_templates/states/(?P<workflow_template_state_id>\d+)/actions/selection/$',
        name='workflow_template_state_action_selection',
        view=WorkflowTemplateStateActionSelectionView.as_view()
    ),
    url(
        regex=r'^workflow_templates/states/(?P<workflow_template_state_id>\d+)/actions/(?P<class_path>[a-zA-Z0-9_.]+)/create/$',
        name='workflow_template_state_action_create',
        view=WorkflowTemplateStateActionCreateView.as_view()
    ),
    url(
        regex=r'^workflow_templates/states/actions/(?P<workflow_template_state_action_id>\d+)/delete/$',
        name='workflow_template_state_action_delete',
        view=WorkflowTemplateStateActionDeleteView.as_view()
    ),
    url(
        regex=r'^workflow_templates/states/actions/(?P<workflow_template_state_action_id>\d+)/edit/$',
        name='workflow_template_state_action_edit',
        view=WorkflowTemplateStateActionEditView.as_view()
    )
]

urlpatterns_workflow_templates = [
    url(
        regex=r'^document_types/(?P<document_type_id>\d+)/workflow_templates/$',
        name='document_type_workflow_templates',
        view=DocumentTypeWorkflowTemplatesView.as_view()
    ),
    url(
        regex=r'^workflow_templates/$', name='workflow_template_list',
        view=WorkflowTemplateListView.as_view()
    ),
    url(
        regex=r'^workflow_templates/create/$',
        name='workflow_template_create',
        view=WorkflowTemplateCreateView.as_view()
    ),
    url(
        regex=r'^workflow_templates/(?P<workflow_template_id>\d+)/delete/$',
        name='workflow_template_delete',
        view=WorkflowTemplateDeleteView.as_view()
    ),
    url(
        regex=r'^workflow_templates/(?P<workflow_template_id>\d+)/document_types/$',
        name='workflow_template_document_types',
        view=WorkflowTemplateDocumentTypesView.as_view()
    ),
    url(
        regex=r'^workflow_templates/(?P<workflow_template_id>\d+)/edit/$',
        name='workflow_template_edit',
        view=WorkflowTemplateEditView.as_view()
    ),
    url(
        regex=r'^workflow_templates/(?P<workflow_template_id>\d+)/launch/$',
        name='workflow_template_launch',
        view=WorkflowTemplateLaunchView.as_view()
    ),
    url(
        regex=r'^workflow_templates/(?P<workflow_template_id>\d+)/preview/$',
        name='workflow_template_preview',
        view=WorkflowTemplatePreviewView.as_view()
    )
]
urlpatterns_workflow_transitions = [
    url(
        regex=r'^workflow_templates/(?P<workflow_template_id>\d+)/transitions/$',
        name='workflow_template_transition_list',
        view=WorkflowTemplateTransitionListView.as_view()
    ),
    url(
        regex=r'^workflow_templates/(?P<workflow_template_id>\d+)/transitions/create/$',
        name='workflow_template_transition_create',
        view=WorkflowTemplateTransitionCreateView.as_view()
    ),
    url(
        regex=r'^workflow_templates/transitions/(?P<workflow_template_transition_id>\d+)/delete/$',
        name='workflow_template_transition_delete',
        view=WorkflowTemplateTransitionDeleteView.as_view()
    ),
    url(
        regex=r'^workflow_templates/transitions/(?P<workflow_template_transition_id>\d+)/edit/$',
        name='workflow_template_transition_edit',
        view=WorkflowTemplateTransitionEditView.as_view()
    ),
    url(
        regex=r'^workflow_templates/transitions/(?P<workflow_template_transition_id>\d+)/events/$',
        name='workflow_template_transition_events',
        view=WorkflowTemplateTransitionTriggerEventListView.as_view()
    )
]

urlpatterns_workflow_transition_fields = [
    url(
        regex=r'^workflow_templates/transitions/(?P<workflow_template_transition_id>\d+)/fields/create/$',
        name='workflow_template_transition_field_create',
        view=WorkflowTemplateTransitionFieldCreateView.as_view()
    ),
    url(
        regex=r'^workflow_templates/transitions/(?P<workflow_template_transition_id>\d+)/fields/$',
        name='workflow_template_transition_field_list',
        view=WorkflowTemplateTransitionFieldListView.as_view()
    ),
    url(
        regex=r'^workflow_templates/transitions/fields/(?P<workflow_template_transition_field_id>\d+)/delete/$',
        name='workflow_template_transition_field_delete',
        view=WorkflowTemplateTransitionFieldDeleteView.as_view()
    ),
    url(
        regex=r'^workflow_templates/transitions/fields/(?P<workflow_template_transition_field_id>\d+)/edit/$',
        name='workflow_template_transition_field_edit',
        view=WorkflowTemplateTransitionFieldEditView.as_view()
    )
]

urlpatterns_tools = [
    url(
        regex=r'^tools/workflows/launch/$', name='tool_launch_workflows',
        view=ToolLaunchWorkflows.as_view()
    )
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
        regex=r'^workflows/$', name='workflow-list',
        view=APIWorkflowRuntimeProxyListView.as_view()
    ),
    url(
        regex=r'^workflows/(?P<pk>[0-9]+)/$', name='workflow-detail',
        view=APIWorkflowView.as_view()
    ),
    url(
        regex=r'^workflows/(?P<pk>[0-9]+)/document_types/$',
        name='workflow-document-type-list',
        view=APIWorkflowDocumentTypeList.as_view()
    ),
    url(
        regex=r'^workflows/(?P<pk>[0-9]+)/document_types/(?P<document_type_pk>[0-9]+)/$',
        name='workflow-document-type-detail',
        view=APIWorkflowDocumentTypeView.as_view()
    ),
    url(
        regex=r'^workflows/(?P<pk>\d+)/image/$',
        name='workflow-image', view=APIWorkflowImageView.as_view()
    ),
    url(
        regex=r'^workflows/(?P<pk>[0-9]+)/states/$',
        name='workflowstate-list', view=APIWorkflowStateListView.as_view()
    ),
    url(
        regex=r'^workflows/(?P<pk>[0-9]+)/states/(?P<state_pk>[0-9]+)/$',
        name='workflowstate-detail', view=APIWorkflowStateView.as_view()
    ),
    url(
        regex=r'^workflows/(?P<pk>[0-9]+)/transitions/$',
        name='workflowtransition-list',
        view=APIWorkflowTransitionListView.as_view()
    ),
    url(
        regex=r'^workflows/(?P<pk>[0-9]+)/transitions/(?P<transition_pk>[0-9]+)/$',
        name='workflowtransition-detail',
        view=APIWorkflowTransitionView.as_view()
    ),
    url(
        regex=r'^documents/(?P<pk>[0-9]+)/workflows/$',
        name='workflowinstance-list',
        view=APIWorkflowInstanceListView.as_view()
    ),
    url(
        regex=r'^documents/(?P<pk>[0-9]+)/workflows/(?P<workflow_pk>[0-9]+)/$',
        name='workflowinstance-detail',
        view=APIWorkflowInstanceView.as_view()
    ),
    url(
        regex=r'^documents/(?P<pk>[0-9]+)/workflows/(?P<workflow_pk>[0-9]+)/log_entries/$',
        name='workflowinstancelogentry-list',
        view=APIWorkflowInstanceLogEntryListView.as_view()
    ),
    url(
        regex=r'^document_types/(?P<pk>[0-9]+)/workflows/$',
        name='documenttype-workflow-list',
        view=APIDocumentTypeWorkflowRuntimeProxyListView.as_view()
    )
]
