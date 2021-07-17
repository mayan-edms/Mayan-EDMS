from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_control, patch_cache_control

from mayan.apps.acls.models import AccessControlList
from mayan.apps.documents.models.document_models import Document
from mayan.apps.documents.models.document_type_models import DocumentType
from mayan.apps.documents.permissions import permission_document_type_view
from mayan.apps.documents.serializers.document_type_serializers import DocumentTypeSerializer
from mayan.apps.rest_api.api_view_mixins import ExternalObjectAPIViewMixin
from mayan.apps.rest_api import generics

from .literals import WORKFLOW_IMAGE_TASK_TIMEOUT
from .models import Workflow
from .permissions import (
    permission_workflow_instance_transition,
    permission_workflow_template_create, permission_workflow_template_delete,
    permission_workflow_template_edit, permission_workflow_template_view
)
from .serializers import (
    WorkflowInstanceSerializer, WorkflowInstanceLogEntrySerializer,
    WorkflowTemplateDocumentTypeAddSerializer,
    WorkflowTemplateDocumentTypeRemoveSerializer, WorkflowTemplateSerializer,
    WorkflowTemplateStateSerializer, WorkflowTemplateTransitionSerializer,
    WorkflowTransitionFieldSerializer
)

from .settings import setting_workflow_image_cache_time
from .tasks import task_generate_workflow_image


class APIWorkflowTemplateDocumentTypeListView(
    ExternalObjectAPIViewMixin, generics.ListAPIView
):
    """
    get: Returns a list of all the document types attached to a workflow template.
    """
    external_object_class = Workflow
    external_object_pk_url_kwarg = 'workflow_template_id'
    mayan_external_object_permissions = {
        'GET': (permission_workflow_template_view,)
    }
    mayan_object_permissions = {
        'GET': (permission_document_type_view,),
    }
    serializer_class = DocumentTypeSerializer

    def get_queryset(self):
        """
        This view returns a list of document types that belong to a workflow template.
        """
        return self.external_object.document_types.all()


class APIWorkflowTemplateDocumentTypeAddView(generics.ObjectActionAPIView):
    """
    post: Add a document type to a workflow template.
    """
    lookup_url_kwarg = 'workflow_template_id'
    mayan_object_permissions = {
        'POST': (permission_workflow_template_edit,)
    }
    serializer_class = WorkflowTemplateDocumentTypeAddSerializer
    queryset = Workflow.objects.all()

    def object_action(self, request, serializer):
        document_type = serializer.validated_data['document_type_id']
        self.object._event_actor = self.request.user
        self.object.document_types_add(
            queryset=DocumentType.objects.filter(pk=document_type.id)
        )


class APIWorkflowTemplateDocumentTypeRemoveView(generics.ObjectActionAPIView):
    """
    post: Add a document type from a workflow template.
    """
    lookup_url_kwarg = 'workflow_template_id'
    mayan_object_permissions = {
        'POST': (permission_workflow_template_edit,)
    }
    serializer_class = WorkflowTemplateDocumentTypeRemoveSerializer
    queryset = Workflow.objects.all()

    def object_action(self, request, serializer):
        document_type = serializer.validated_data['document_type_id']
        self.object._event_actor = self.request.user
        self.object.document_types_remove(
            queryset=DocumentType.objects.filter(pk=document_type.id)
        )


class APIWorkflowTemplateImageView(generics.RetrieveAPIView):
    """
    get: Returns an image representation of the selected workflow template.
    """
    lookup_url_kwarg = 'workflow_template_id'
    mayan_object_permissions = {
        'GET': (permission_workflow_template_view,),
    }
    queryset = Workflow.objects.all()

    def get_serializer(self, *args, **kwargs):
        return None

    def get_serializer_class(self):
        return None

    @cache_control(private=True)
    def retrieve(self, request, *args, **kwargs):
        task = task_generate_workflow_image.apply_async(
            kwargs=dict(
                document_state_id=self.get_object().pk,
            )
        )

        kwargs = {'timeout': WORKFLOW_IMAGE_TASK_TIMEOUT}
        if settings.DEBUG:
            # In debug mode, task are run synchronously, causing this method
            # to be called inside another task. Disable the check of nested
            # tasks when using debug mode.
            kwargs['disable_sync_subtasks'] = False

        cache_filename = task.get(**kwargs)
        cache_file = self.get_object().cache_partition.get_file(filename=cache_filename)
        with cache_file.open() as file_object:
            response = HttpResponse(content=file_object.read(), content_type='image')
            if '_hash' in request.GET:
                patch_cache_control(
                    response,
                    max_age=setting_workflow_image_cache_time.value
                )
            return response


class APIWorkflowTemplateListView(generics.ListCreateAPIView):
    """
    get: Returns a list of all the workflow templates.
    post: Create a new workflow template.
    """
    mayan_object_permissions = {'GET': (permission_workflow_template_view,)}
    mayan_view_permissions = {'POST': (permission_workflow_template_create,)}
    ordering_fields = ('id', 'internal_name', 'label')
    queryset = Workflow.objects.all()
    serializer_class = WorkflowTemplateSerializer

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user,
        }


class APIWorkflowTemplateDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    delete: Delete the selected workflow template.
    get: Return the details of the selected workflow template.
    patch: Edit the selected workflow template.
    put: Edit the selected workflow template.
    """
    lookup_url_kwarg = 'workflow_template_id'
    mayan_object_permissions = {
        'DELETE': (permission_workflow_template_delete,),
        'GET': (permission_workflow_template_view,),
        'PATCH': (permission_workflow_template_edit,),
        'PUT': (permission_workflow_template_edit,)
    }
    queryset = Workflow.objects.all()
    serializer_class = WorkflowTemplateSerializer

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user,
        }


# Workflow state views


class APIWorkflowTemplateStateListView(generics.ListCreateAPIView):
    """
    get: Returns a list of all the workflow template states.
    post: Create a new workflow template state.
    """
    ordering_fields = ('completion', 'id', 'initial', 'label')
    serializer_class = WorkflowTemplateStateSerializer

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user,
            'workflow': self.get_workflow_template()
        }

    def get_queryset(self):
        return self.get_workflow_template().states.all()

    def get_workflow_template(self):
        if self.request.method == 'GET':
            permission_required = permission_workflow_template_view
        else:
            permission_required = permission_workflow_template_edit

        queryset = AccessControlList.objects.restrict_queryset(
            permission=permission_required, queryset=Workflow.objects.all(),
            user=self.request.user
        )

        return get_object_or_404(
            klass=queryset, pk=self.kwargs['workflow_template_id']
        )


class APIWorkflowTemplateStateView(
    ExternalObjectAPIViewMixin, generics.RetrieveUpdateDestroyAPIView
):
    """
    delete: Delete the selected workflow template state.
    get: Return the details of the selected workflow template state.
    patch: Edit the selected workflow template state.
    put: Edit the selected workflow template state.
    """
    external_object_class = Workflow
    external_object_pk_url_kwarg = 'workflow_template_id'
    mayan_external_object_permissions = {
        'DELETE': (permission_workflow_template_edit,),
        'GET': (permission_workflow_template_view,),
        'PATCH': (permission_workflow_template_edit,),
        'PUT': (permission_workflow_template_edit,),
    }
    lookup_url_kwarg = 'workflow_template_state_id'
    serializer_class = WorkflowTemplateStateSerializer

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user,
        }

    def get_queryset(self):
        return self.external_object.states.all()


# Workflow transition views


class APIWorkflowTemplateTransitionListView(
    ExternalObjectAPIViewMixin, generics.ListCreateAPIView
):
    """
    get: Returns a list of all the workflow template transitions.
    post: Create a new workflow template transition.
    """
    external_object_class = Workflow
    external_object_pk_url_kwarg = 'workflow_template_id'
    mayan_external_object_permissions = {
        'GET': (permission_workflow_template_view,),
        'POST': (permission_workflow_template_edit,),
    }
    ordering_fields = ('destination_state', 'id', 'label', 'origin_state')
    serializer_class = WorkflowTemplateTransitionSerializer

    def get_instance_extra_data(self):
        # This method is only called during POST, therefore filter only by
        # edit permission.
        return {
            '_event_actor': self.request.user,
            'workflow': self.external_object,
        }

    def get_queryset(self):
        return self.external_object.transitions.all()


class APIWorkflowTemplateTransitionView(
    ExternalObjectAPIViewMixin, generics.RetrieveUpdateDestroyAPIView
):
    """
    delete: Delete the selected workflow template transition.
    get: Return the details of the selected workflow template transition.
    patch: Edit the selected workflow template transition.
    put: Edit the selected workflow template transition.
    """
    external_object_class = Workflow
    external_object_pk_url_kwarg = 'workflow_template_id'
    mayan_external_object_permissions = {
        'DELETE': (permission_workflow_template_edit,),
        'GET': (permission_workflow_template_view,),
        'PATCH': (permission_workflow_template_edit,),
        'PUT': (permission_workflow_template_edit,),
    }
    lookup_url_kwarg = 'workflow_template_transition_id'
    serializer_class = WorkflowTemplateTransitionSerializer

    def get_instance_extra_data(self):
        # This method is only called during POST, therefore filter only by
        # edit permission.
        return {
            '_event_actor': self.request.user,
            'workflow': self.external_object,
        }

    def get_queryset(self):
        return self.external_object.transitions.all()


# Workflow template transition fields


class APIWorkflowTemplateTransitionFieldListView(generics.ListCreateAPIView):
    """
    get: Returns a list of all the workflow template transition fields.
    post: Create a new workflow template transition field.
    """
    ordering_fields = ('id', 'label', 'name', 'required', 'widget_kwargs')
    serializer_class = WorkflowTransitionFieldSerializer

    def get_instance_extra_data(self):
        # This method is only called during POST, therefore filter only by
        # edit permission.
        return {
            '_event_actor': self.request.user,
            'transition': self.get_workflow_template_transition(),
        }

    def get_queryset(self):
        return self.get_workflow_template_transition().fields.all()

    def get_workflow_template(self):
        if self.request.method == 'GET':
            permission_required = permission_workflow_template_view
        else:
            permission_required = permission_workflow_template_edit

        queryset = AccessControlList.objects.restrict_queryset(
            permission=permission_required, queryset=Workflow.objects.all(),
            user=self.request.user
        )

        return get_object_or_404(
            klass=queryset, pk=self.kwargs['workflow_template_id']
        )

    def get_workflow_template_transition(self):
        return get_object_or_404(
            klass=self.get_workflow_template().transitions,
            pk=self.kwargs['workflow_template_transition_id']
        )


class APIWorkflowTemplateTransitionFieldDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    delete: Delete the selected workflow template transition field.
    get: Return the details of the selected workflow template transition field.
    patch: Edit the selected workflow template transition field.
    put: Edit the selected workflow template transition field.
    """
    lookup_url_kwarg = 'workflow_template_transition_field_id'
    serializer_class = WorkflowTransitionFieldSerializer

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user,
        }

    def get_queryset(self):
        return self.get_workflow_template_transition().fields.all()

    def get_workflow_template(self):
        if self.request.method == 'GET':
            permission_required = permission_workflow_template_view
        else:
            permission_required = permission_workflow_template_edit

        queryset = AccessControlList.objects.restrict_queryset(
            permission=permission_required, queryset=Workflow.objects.all(),
            user=self.request.user
        )

        return get_object_or_404(
            klass=queryset, pk=self.kwargs['workflow_template_id']
        )

    def get_workflow_template_transition(self):
        return get_object_or_404(
            klass=self.get_workflow_template().transitions,
            pk=self.kwargs['workflow_template_transition_id']
        )


# Document workflow views

class APIWorkflowInstanceListView(
    ExternalObjectAPIViewMixin, generics.ListAPIView
):
    """
    get: Returns a list of all the document workflow instances.
    """
    external_object_queryset = Document.valid
    external_object_pk_url_kwarg = 'document_id'
    mayan_external_object_permissions = {
        'GET': (permission_workflow_template_view,),
    }
    mayan_object_permissions = {
        'GET': (permission_workflow_template_view,),
    }
    serializer_class = WorkflowInstanceSerializer

    def get_queryset(self):
        return self.external_object.workflows.all()


class APIWorkflowInstanceDetailView(
    ExternalObjectAPIViewMixin, generics.RetrieveAPIView
):
    """
    get: Return the details of the selected document workflow instances.
    """
    external_object_queryset = Document.valid
    external_object_pk_url_kwarg = 'document_id'
    lookup_url_kwarg = 'workflow_instance_id'
    mayan_external_object_permissions = {
        'GET': (permission_workflow_template_view,),
    }
    mayan_object_permissions = {
        'GET': (permission_workflow_template_view,),
    }
    serializer_class = WorkflowInstanceSerializer

    def get_queryset(self):
        return self.external_object.workflows.all()


class APIWorkflowInstanceLogEntryDetailView(
    ExternalObjectAPIViewMixin, generics.RetrieveAPIView
):
    """
    get: Return the details of the selected document instances log entry.
    """
    external_object_pk_url_kwarg = 'document_id'
    external_object_queryset = Document.valid
    mayan_external_object_permissions = {
        'GET': (permission_workflow_template_view,),
    }
    serializer_class = WorkflowInstanceLogEntrySerializer
    lookup_url_kwarg = 'workflow_instance_log_entry_id'

    def get_queryset(self):
        return self.get_workflow_instance().log_entries.all()

    def get_workflow_instance(self):
        workflow = get_object_or_404(
            klass=self.external_object.workflows,
            pk=self.kwargs['workflow_instance_id']
        )

        return workflow


class APIWorkflowInstanceLogEntryListView(
    ExternalObjectAPIViewMixin, generics.ListCreateAPIView
):
    """
    get: Returns a list of all the document workflow instances log entries.
    post: Transition a document workflow by creating a new document workflow instance log entry.
    """
    external_object_pk_url_kwarg = 'document_id'
    external_object_queryset = Document.valid
    mayan_external_object_permissions = {
        'GET': (permission_workflow_template_view,),
        'POST': (permission_workflow_instance_transition,),
    }
    mayan_object_permissions = {
        'GET': (permission_workflow_template_view,),
    }
    ordering_fields = (
        'comment', 'id', 'transition', 'transition__destination_state',
        'transition__origin_state'
    )
    serializer_class = WorkflowInstanceLogEntrySerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.kwargs:
            context.update(
                {
                    'workflow_instance': self.get_workflow_instance(),
                }
            )

        return context

    def get_queryset(self):
        return self.get_workflow_instance().log_entries.all()

    def get_workflow_instance(self):
        workflow = get_object_or_404(
            klass=self.external_object.workflows,
            pk=self.kwargs['workflow_instance_id']
        )

        return workflow


class APIWorkflowInstanceLogEntryTransitionListView(
    ExternalObjectAPIViewMixin, generics.ListAPIView
):
    """
    get: Returns a list of all the possible transition choices for the workflow instance.
    """
    external_object_pk_url_kwarg = 'document_id'
    external_object_queryset = Document.valid
    mayan_external_object_permissions = {
        'GET': (permission_workflow_template_view,),
    }
    mayan_object_permissions = {
        'GET': (permission_workflow_template_view,),
    }
    ordering_fields = ('destination_state', 'id', 'origin_state')
    serializer_class = WorkflowTemplateTransitionSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.kwargs:
            context.update(
                {
                    'workflow_instance': self.get_workflow_instance(),
                }
            )

        return context

    def get_queryset(self):
        return self.get_workflow_instance().get_transition_choices(
            _user=self.request.user
        )

    def get_workflow_instance(self):
        workflow = get_object_or_404(
            klass=self.external_object.workflows,
            pk=self.kwargs['workflow_instance_id']
        )

        return workflow
