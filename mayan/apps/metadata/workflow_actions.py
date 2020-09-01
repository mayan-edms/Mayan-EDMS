import logging

from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.models import AccessControlList
from mayan.apps.document_states.classes import WorkflowAction
from mayan.apps.document_states.exceptions import WorkflowStateActionError
from mayan.apps.metadata.models import DocumentMetadata, MetadataType
from mayan.apps.metadata.permissions import (
    permission_document_metadata_add, permission_document_metadata_remove,
    permission_document_metadata_edit
)

logger = logging.getLogger(name=__name__)


class DocumentMetadataAddAction(WorkflowAction):
    fields = {
        'metadata_types': {
            'label': _('Metadata types'),
            'class': 'django.forms.ModelMultipleChoiceField', 'kwargs': {
                'help_text': _('Metadata types to add to the document.'),
                'queryset': MetadataType.objects.none(), 'required': False
            }
        },
    }
    label = _('Add metadata')
    widgets = {
        'metadata_types': {
            'class': 'django.forms.widgets.SelectMultiple', 'kwargs': {
                'attrs': {'class': 'select2'},
            }
        }
    }

    permission = permission_document_metadata_add

    def execute(self, context):
        for metadata_type in self.get_metadata_types():
            try:
                context['document'].metadata.create(metadata_type=metadata_type)
            except IntegrityError as exception:
                """This document already has the metadata type added"""
                raise WorkflowStateActionError(
                    _(
                        'Unable to add metadata type "%(metadata_type)s '
                        'from document: %(document)s. Exception: '
                        '%(exception)s'
                    ) % {
                        'document': context['document'],
                        'exception': exception,
                        'metadata_type': metadata_type,
                    }
                ) from exception

    def get_form_schema(self, **kwargs):
        result = super().get_form_schema(**kwargs)

        document_types_queryset = kwargs['workflow_state'].workflow.document_types

        metadata_type_queryset = MetadataType.objects.get_for_document_types(
            queryset=document_types_queryset
        )

        queryset = AccessControlList.objects.restrict_queryset(
            permission=self.permission, queryset=metadata_type_queryset,
            user=kwargs['request'].user
        )

        result['fields']['metadata_types']['kwargs']['queryset'] = queryset

        return result

    def get_metadata_types(self):
        return MetadataType.objects.filter(
            pk__in=self.form_data.get('metadata_types', ())
        )


class DocumentMetadataEditAction(WorkflowAction):
    fields = {
        'metadata_type': {
            'label': _('Metadata type'),
            'class': 'django.forms.ModelChoiceField', 'kwargs': {
                'help_text': _('Metadata types to edit.'),
                'queryset': MetadataType.objects.none(), 'required': True
            }
        },
        'value': {
            'label': _('Value'),
            'class': 'django.forms.CharField', 'kwargs': {
                'help_text': _(
                    'Value to assign to the metadata. '
                    'Can be a literal value or template code.'
                ),
                'required': True
            }
        },
    }
    field_order = ('metadata_type', 'value')
    label = _('Edit metadata')
    widgets = {
        'metadata_types': {
            'class': 'django.forms.widgets.Select', 'kwargs': {
                'attrs': {'class': 'select2'},
            }
        },
        'value': {
            'class': 'django.forms.widgets.Textarea', 'kwargs': {
                'attrs': {'rows': '10'},
            }
        }
    }

    def execute(self, context):
        try:
            metadata_type = self.get_metadata_type()
            document_metadata = context['document'].metadata.get(
                metadata_type=metadata_type
            )
        except DocumentMetadata.DoesNotExist as exception:
            """Non fatal, we just ignore the action to edit the metadata value"""
            raise WorkflowStateActionError(
                _(
                    'Unable to edit metadata type "%(metadata_type)s '
                    'from document: %(document)s. Document does not have '
                    'the metadata type to be edit. Exception: '
                    '%(exception)s'
                ) % {
                    'document': context['document'],
                    'exception': exception,
                    'metadata_type': metadata_type,
                }
            ) from exception
        else:
            document_metadata.value = self.render_field(
                field_name='value', context=context
            )
            document_metadata.save()

    def get_form_schema(self, **kwargs):
        result = super().get_form_schema(**kwargs)

        document_types_queryset = kwargs['workflow_state'].workflow.document_types

        metadata_type_queryset = MetadataType.objects.get_for_document_types(
            queryset=document_types_queryset
        )

        queryset = AccessControlList.objects.restrict_queryset(
            permission=permission_document_metadata_edit,
            queryset=metadata_type_queryset,
            user=kwargs['request'].user
        )

        result['fields']['metadata_type']['kwargs']['queryset'] = queryset

        return result

    def get_metadata_type(self):
        return MetadataType.objects.get(pk=self.form_data['metadata_type'])


class DocumentMetadataRemoveAction(DocumentMetadataAddAction):
    fields = {
        'metadata_types': {
            'label': _('Metadata types'),
            'class': 'django.forms.ModelMultipleChoiceField', 'kwargs': {
                'help_text': _('Metadata types to remove from the document.'),
                'queryset': MetadataType.objects.none(), 'required': False
            }
        },
    }
    label = _('Remove metadata')

    permission = permission_document_metadata_remove

    def execute(self, context):
        for metadata_type in self.get_metadata_types():
            try:
                context['document'].metadata.get(
                    metadata_type=metadata_type
                ).delete()
            except DocumentMetadata.DoesNotExist:
                """This document does not have the metadata type added"""
            except ValidationError as exception:
                raise WorkflowStateActionError(
                    _(
                        'Unable to remove metadata type "%(metadata_type)s '
                        'from document: %(document)s. Exception: '
                        '%(exception)s'
                    ) % {
                        'document': context['document'],
                        'exception': exception,
                        'metadata_type': metadata_type,
                    }
                ) from exception
