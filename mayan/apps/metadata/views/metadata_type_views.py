from django.template import RequestContext
from django.urls import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _

from mayan.apps.documents.models import DocumentType
from mayan.apps.documents.permissions import (
    permission_document_type_edit
)
from mayan.apps.views.generics import (
    MultipleObjectDeleteView, RelationshipView, SingleObjectCreateView,
    SingleObjectEditView, SingleObjectListView
)

from ..forms import (
    DocumentTypeMetadataTypeRelationshipFormSet, MetadataTypeForm
)
from ..icons import icon_metadata
from ..links import link_metadata_type_create
from ..models import MetadataType
from ..permissions import (
    permission_metadata_type_create, permission_metadata_type_delete,
    permission_metadata_type_edit, permission_metadata_type_view
)


class MetadataTypeCreateView(SingleObjectCreateView):
    extra_context = {'title': _('Create metadata type')}
    form_class = MetadataTypeForm
    model = MetadataType
    post_action_redirect = reverse_lazy(
        viewname='metadata:metadata_type_list'
    )
    view_permission = permission_metadata_type_create

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user,
        }


class MetadataTypeDeleteView(MultipleObjectDeleteView):
    error_message = _(
        'Error deleting metadata type "%(instance)s"; %(exception)s'
    )
    model = MetadataType
    object_permission = permission_metadata_type_delete
    pk_url_kwarg = 'metadata_type_id'
    post_action_redirect = reverse_lazy(
        viewname='metadata:metadata_type_list'
    )
    success_message_single = _(
        'Metadata type "%(object)s" deleted successfully.'
    )
    success_message_singular = _(
        '%(count)d metadata type deleted successfully.'
    )
    success_message_plural = _(
        '%(count)d metadata types deleted successfully.'
    )
    title_single = _('Delete metadata type: %(object)s.')
    title_singular = _('Delete the %(count)d selected metadata type.')
    title_plural = _('Delete the %(count)d selected metadata types.')


class MetadataTypeEditView(SingleObjectEditView):
    form_class = MetadataTypeForm
    model = MetadataType
    object_permission = permission_metadata_type_edit
    pk_url_kwarg = 'metadata_type_id'
    post_action_redirect = reverse_lazy(
        viewname='metadata:metadata_type_list'
    )

    def get_extra_context(self):
        return {
            'object': self.object,
            'title': _('Edit metadata type: %s') % self.object,
        }

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user,
        }


class MetadataTypeListView(SingleObjectListView):
    model = MetadataType
    object_permission = permission_metadata_type_view

    def get_extra_context(self):
        return {
            'hide_link': True,
            'hide_object': True,
            'no_results_icon': icon_metadata,
            'no_results_main_link': link_metadata_type_create.resolve(
                context=RequestContext(request=self.request)
            ),
            'no_results_text': _(
                'Metadata types are users defined properties that can be '
                'assigned values. Once created they must be associated to '
                'document types, either as optional or required, for each. '
                'Setting a metadata type as required for a document type '
                'will block the upload of documents of that type until a '
                'metadata value is provided.'
            ),
            'no_results_title': _('There are no metadata types'),
            'title': _('Metadata types'),
        }


class DocumentTypeMetadataTypeRelationshipView(RelationshipView):
    form_class = DocumentTypeMetadataTypeRelationshipFormSet
    model = DocumentType
    model_permission = permission_document_type_edit
    pk_url_kwarg = 'document_type_id'
    relationship_related_field = 'metadata'
    relationship_related_query_field = 'metadata_type'
    sub_model = MetadataType
    sub_model_permission = permission_metadata_type_edit

    def get_extra_context(self):
        return {
            'form_display_mode_table': True,
            'no_results_icon': icon_metadata,
            'no_results_main_link': link_metadata_type_create.resolve(
                context=RequestContext(request=self.request)
            ),
            'no_results_text': _(
                'Create metadata type relationships to be able to associate '
                'them to this document type.'
            ),
            'no_results_title': _(
                'There are no metadata type relationships available'
            ),
            'object': self.get_object(),
            'title': _(
                'Metadata type relationships for document type: %s'
            ) % self.get_object()
        }

    def get_form_extra_kwargs(self):
        return {
            '_event_actor': self.request.user,
        }

    def get_initial(self):
        obj = self.get_object()
        initial = []

        for element in self.get_sub_model_queryset():
            initial.append(
                {
                    'object': obj,
                    'relationship_related_field': self.relationship_related_field,
                    'relationship_related_query_field': self.relationship_related_query_field,
                    'sub_object': element,
                }
            )
        return initial

    def get_post_action_redirect(self):
        return reverse(viewname='documents:document_type_list')


class MetadataTypesDocumentTypeRelationshipView(
    DocumentTypeMetadataTypeRelationshipView
):
    model = MetadataType
    model_permission = permission_metadata_type_edit
    pk_url_kwarg = 'metadata_type_id'
    relationship_related_field = 'document_types'
    relationship_related_query_field = 'document_type'
    sub_model = DocumentType
    sub_model_permission = permission_document_type_edit

    def get_extra_context(self):
        return {
            'form_display_mode_table': True,
            'object': self.get_object(),
            'title': _(
                'Document type relationships for metadata type: %s'
            ) % self.get_object()
        }

    def get_initial(self):
        obj = self.get_object()
        initial = []

        for element in self.get_sub_model_queryset():
            initial.append(
                {
                    'object': obj,
                    'relationship_related_field': self.relationship_related_field,
                    'relationship_related_query_field': self.relationship_related_query_field,
                    'sub_object': element,
                }
            )
        return initial

    def get_post_action_redirect(self):
        return reverse(viewname='metadata:metadata_type_list')
