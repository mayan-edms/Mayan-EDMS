from furl import furl

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _, ungettext

from mayan.apps.acls.models import AccessControlList
from mayan.apps.documents.models import Document, DocumentType
from mayan.apps.documents.permissions import (
    permission_document_type_edit
)
from mayan.apps.views.generics import (
    FormView, MultipleObjectFormActionView, SingleObjectCreateView,
    SingleObjectDeleteView, SingleObjectEditView, SingleObjectListView
)
from mayan.apps.views.mixins import ExternalObjectMixin
from mayan.apps.views.utils import convert_to_id_list

from .api import save_metadata_list
from .forms import (
    DocumentMetadataAddForm, DocumentMetadataFormSet,
    DocumentMetadataRemoveFormSet,
    DocumentTypeMetadataTypeRelationshipFormSet, MetadataTypeForm
)
from .icons import (
    icon_document_metadata_add, icon_document_metadata_edit,
    icon_document_metadata_remove, icon_metadata
)
from .links import (
    link_metadata_add, link_metadata_multiple_add,
    link_setup_metadata_type_create
)
from .mixins import DocumentMetadataSameTypeMixin
from .models import DocumentMetadata, MetadataType
from .permissions import (
    permission_document_metadata_add, permission_document_metadata_edit,
    permission_document_metadata_remove, permission_document_metadata_view,
    permission_metadata_type_create, permission_metadata_type_delete,
    permission_metadata_type_edit, permission_metadata_type_view
)


class DocumentMetadataAddView(
    DocumentMetadataSameTypeMixin, MultipleObjectFormActionView
):
    form_class = DocumentMetadataAddForm
    model = Document
    object_permission = permission_document_metadata_add
    pk_url_kwarg = 'document_id'
    success_message = _('Metadata add request performed on %(count)d document')
    success_message_plural = _(
        'Metadata add request performed on %(count)d documents'
    )

    def get_extra_context(self):
        queryset = self.object_list

        result = {
            'submit_icon_class': icon_document_metadata_add,
            'submit_label': _('Add'),
            'title': ungettext(
                singular='Add metadata types to document',
                plural='Add metadata types to documents',
                number=queryset.count()
            )
        }

        if queryset.count() == 1:
            result.update(
                {
                    'object': queryset.first(),
                    'title': _(
                        'Add metadata types to document: %s'
                    ) % queryset.first()
                }
            )

        return result

    def get_form_extra_kwargs(self):
        queryset = self.object_list

        result = {}

        if queryset.count():
            result.update(
                {
                    'document_type': queryset.first().document_type,
                }
            )

        if queryset.count() == 1:
            result.update(
                {
                    'queryset': MetadataType.objects.get_for_document_type(
                        document_type=queryset.first().document_type
                    ).exclude(
                        pk__in=MetadataType.objects.get_for_document(
                            document=queryset.first()
                        )
                    )
                }
            )

        return result

    def get_post_object_action_url(self):
        if self.action_count == 1:
            return reverse(
                viewname='metadata:metadata_edit', kwargs={
                    'document_id': self.action_id_list[0]
                }
            )

        elif self.action_count > 1:
            url = furl(
                path=reverse(
                    viewname='metadata:metadata_multiple_edit'
                ), args={
                    'id_list': convert_to_id_list(items=self.action_id_list)
                }
            )

            return url.tostr()

    def object_action(self, form, instance):
        queryset = AccessControlList.objects.restrict_queryset(
            queryset=form.cleaned_data['metadata_type'],
            permission=permission_document_metadata_add,
            user=self.request.user
        )

        for metadata_type in queryset:
            try:
                created = False
                try:
                    DocumentMetadata.objects.get(
                        document=instance,
                        metadata_type=metadata_type,
                    )
                except DocumentMetadata.DoesNotExist:
                    document_metadata = DocumentMetadata(
                        document=instance,
                        metadata_type=metadata_type,
                    )
                    document_metadata.save(_user=self.request.user)
                    created = True
            except Exception as exception:
                messages.error(
                    message=_(
                        'Error adding metadata type '
                        '"%(metadata_type)s" to document: '
                        '%(document)s; %(exception)s'
                    ) % {
                        'metadata_type': metadata_type,
                        'document': instance,
                        'exception': ', '.join(
                            getattr(exception, 'messages', exception)
                        )
                    }, request=self.request
                )
            else:
                if created:
                    messages.success(
                        message=_(
                            'Metadata type: %(metadata_type)s '
                            'successfully added to document %(document)s.'
                        ) % {
                            'metadata_type': metadata_type,
                            'document': instance
                        }, request=self.request
                    )
                else:
                    messages.warning(
                        message=_(
                            'Metadata type: %(metadata_type)s already '
                            'present in document %(document)s.'
                        ) % {
                            'metadata_type': metadata_type,
                            'document': instance
                        }, request=self.request
                    )


class DocumentMetadataEditView(
    DocumentMetadataSameTypeMixin, MultipleObjectFormActionView
):
    form_class = DocumentMetadataFormSet
    model = Document
    object_permission = permission_document_metadata_edit
    pk_url_kwarg = 'document_id'
    success_message = _(
        'Metadata edit request performed on %(count)d document'
    )
    success_message_plural = _(
        'Metadata edit request performed on %(count)d documents'
    )

    def get_extra_context(self):
        queryset = self.object_list

        id_list = ','.join(
            map(
                force_text, queryset.values_list('pk', flat=True)
            )
        )

        if queryset.count() == 1:
            no_results_main_link = link_metadata_add.resolve(
                context=RequestContext(
                    request=self.request, dict_={'object': queryset.first()}
                )
            )
        else:
            no_results_main_link = link_metadata_multiple_add.resolve(
                context=RequestContext(request=self.request)
            )
            no_results_main_link.url = '{}?id_list={}'.format(
                no_results_main_link.url, id_list
            )

        result = {
            'form_display_mode_table': True,
            'no_results_icon': icon_metadata,
            'no_results_main_link': no_results_main_link,
            'no_results_text': _(
                'Add metadata types available for this document\'s type '
                'and assign them corresponding values.'
            ),
            'no_results_title': _('There is no metadata to edit'),
            'submit_icon_class': icon_document_metadata_edit,
            'submit_label': _('Edit'),
            'title': ungettext(
                'Edit document metadata',
                'Edit documents metadata',
                queryset.count()
            )
        }

        if queryset.count() == 1:
            result.update(
                {
                    'object': queryset.first(),
                    'title': _(
                        'Edit metadata for document: %s'
                    ) % queryset.first()
                }
            )

        return result

    def get_initial(self):
        queryset = self.object_list

        metadata_dict = {}
        initial = []

        for document in queryset:
            document_metadata_queryset = AccessControlList.objects.restrict_queryset(
                queryset=document.metadata.all(),
                permission=permission_document_metadata_edit,
                user=self.request.user
            )
            for document_metadata in document_metadata_queryset:
                metadata_dict.setdefault(
                    document_metadata.metadata_type, set()
                )

                if document_metadata.value:
                    metadata_dict[
                        document_metadata.metadata_type
                    ].add(document_metadata.value)

        for key, value in metadata_dict.items():
            initial.append({
                'document_type': document.document_type,
                'metadata_type': key,
                'value': ', '.join(value) if value else '',
            })

        return initial

    def get_post_object_action_url(self):
        if self.action_count == 1:
            return reverse(
                viewname='metadata:metadata_view', kwargs={
                    'document_id': self.action_id_list[0]
                }
            )
        elif self.action_count > 1:
            url = furl(
                path=reverse(
                    viewname='metadata:metadata_multiple_edit'
                ), args={
                    'id_list': convert_to_id_list(items=self.action_id_list)
                }
            )
            return url.tostr()

    def object_action(self, form, instance):
        document_metadata_queryset = AccessControlList.objects.restrict_queryset(
            queryset=instance.metadata.all(),
            permission=permission_document_metadata_edit,
            user=self.request.user
        )

        errors = []
        for form in form.forms:
            if form.cleaned_data['update']:
                if document_metadata_queryset.filter(metadata_type=form.cleaned_data['id']).exists():
                    try:
                        save_metadata_list(
                            metadata_list=[form.cleaned_data], document=instance,
                            _user=self.request.user
                        )
                    except Exception as exception:
                        errors.append(exception)

        for error in errors:
            if settings.DEBUG:
                raise
            else:
                if isinstance(error, ValidationError):
                    exception_message = ', '.join(error.messages)
                else:
                    exception_message = force_text(s=error)

                messages.error(
                    message=_(
                        'Error editing metadata for document: '
                        '%(document)s; %(exception)s.'
                    ) % {
                        'document': instance,
                        'exception': exception_message
                    }, request=self.request
                )
        else:
            messages.success(
                message=_(
                    'Metadata for document %s edited successfully.'
                ) % instance, request=self.request
            )


class DocumentMetadataListView(ExternalObjectMixin, SingleObjectListView):
    external_object_class = Document
    external_object_permission = permission_document_metadata_view
    external_object_pk_url_kwarg = 'document_id'
    object_permission = permission_document_metadata_view

    def get_extra_context(self):
        return {
            'hide_link': True,
            'hide_object': True,
            'object': self.external_object,
            'no_results_icon': icon_metadata,
            'no_results_main_link': link_metadata_add.resolve(
                context=RequestContext(
                    request=self.request, dict_={
                        'object': self.external_object
                    }
                )
            ),
            'no_results_text': _(
                'Add metadata types this document\'s type '
                'to be able to add them to individual documents. '
                'Once added to individual document, you can then edit their '
                'values.'
            ),
            'no_results_title': _('This document doesn\'t have any metadata'),
            'title': _('Metadata for document: %s') % self.external_object,
        }

    def get_source_queryset(self):
        return self.external_object.metadata.all()


class DocumentMetadataRemoveView(
    DocumentMetadataSameTypeMixin, MultipleObjectFormActionView
):
    form_class = DocumentMetadataRemoveFormSet
    model = Document
    object_permission = permission_document_metadata_remove
    pk_url_kwarg = 'document_id'
    success_message = _(
        'Metadata remove request performed on %(count)d document'
    )
    success_message_plural = _(
        'Metadata remove request performed on %(count)d documents'
    )

    def get_extra_context(self):
        queryset = self.object_list

        result = {
            'form_display_mode_table': True,
            'submit_icon_class': icon_document_metadata_remove,
            'submit_label': _('Remove'),
            'title': ungettext(
                singular='Remove metadata types from the document',
                plural='Remove metadata types from the documents',
                number=queryset.count()
            )
        }

        if queryset.count() == 1:
            result.update(
                {
                    'object': queryset.first(),
                    'title': _(
                        'Remove metadata types from the document: %s'
                    ) % queryset.first()
                }
            )

        return result

    def get_initial(self):
        queryset = self.object_list

        metadata = {}
        for document in queryset:
            document_metadata_queryset = AccessControlList.objects.restrict_queryset(
                queryset=document.metadata.all(),
                permission=permission_document_metadata_remove,
                user=self.request.user
            )

            for document_metadata in document_metadata_queryset:
                # Metadata value cannot be None here, fallback to an empty
                # string
                value = document_metadata.value or ''
                if document_metadata.metadata_type in metadata:
                    if value not in metadata[document_metadata.metadata_type]:
                        metadata[document_metadata.metadata_type].append(value)
                else:
                    metadata[document_metadata.metadata_type] = [value] if value else ''

        initial = []
        for key, value in metadata.items():
            initial.append(
                {
                    'document_type': queryset.first().document_type,
                    'metadata_type': key,
                    'value': ', '.join(value)
                }
            )
        return initial

    def get_post_object_action_url(self):
        if self.action_count == 1:
            return reverse(
                viewname='metadata:metadata_view', kwargs={
                    'document_id': self.action_id_list[0]
                }
            )

    def object_action(self, form, instance):
        for form in form.forms:
            if form.cleaned_data['update']:
                queryset = AccessControlList.objects.restrict_queryset(
                    queryset=MetadataType.objects.all(),
                    permission=permission_document_metadata_remove,
                    user=self.request.user
                )
                metadata_type = get_object_or_404(
                    klass=queryset, pk=form.cleaned_data['id']
                )
                try:
                    document_metadata = DocumentMetadata.objects.get(
                        document=instance, metadata_type=metadata_type
                    )
                    document_metadata.delete(_user=self.request.user)
                    messages.success(
                        message=_(
                            'Successfully remove metadata type "%(metadata_type)s" from document: %(document)s.'
                        ) % {
                            'metadata_type': metadata_type,
                            'document': instance
                        }, request=self.request
                    )
                except ValidationError as exception:
                    messages.error(
                        message=_(
                            'Error removing metadata type "%(metadata_type)s" from document: %(document)s; %(exception)s'
                        ) % {
                            'metadata_type': metadata_type,
                            'document': instance,
                            'exception': ', '.join(exception.messages)
                        }, request=self.request
                    )


# Setup views
class MetadataTypeCreateView(SingleObjectCreateView):
    extra_context = {'title': _('Create metadata type')}
    form_class = MetadataTypeForm
    model = MetadataType
    post_action_redirect = reverse_lazy(
        viewname='metadata:setup_metadata_type_list'
    )
    view_permission = permission_metadata_type_create

    def get_save_extra_data(self):
        return {
            '_user': self.request.user,
        }


class MetadataTypeDeleteView(SingleObjectDeleteView):
    model = MetadataType
    object_permission = permission_metadata_type_delete
    pk_url_kwarg = 'metadata_type_id'
    post_action_redirect = reverse_lazy(
        viewname='metadata:setup_metadata_type_list'
    )

    def get_extra_context(self):
        return {
            'delete_view': True,
            'object': self.object,
            'title': _('Delete the metadata type: %s?') % self.object,
        }


class MetadataTypeEditView(SingleObjectEditView):
    form_class = MetadataTypeForm
    model = MetadataType
    object_permission = permission_metadata_type_edit
    pk_url_kwarg = 'metadata_type_id'
    post_action_redirect = reverse_lazy(
        viewname='metadata:setup_metadata_type_list'
    )

    def get_extra_context(self):
        return {
            'object': self.object,
            'title': _('Edit metadata type: %s') % self.object,
        }

    def get_save_extra_data(self):
        return {
            '_user': self.request.user,
        }


class MetadataTypeListView(SingleObjectListView):
    model = MetadataType
    object_permission = permission_metadata_type_view

    def get_extra_context(self):
        return {
            'hide_link': True,
            'hide_object': True,
            'no_results_icon': icon_metadata,
            'no_results_main_link': link_setup_metadata_type_create.resolve(
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


class SetupDocumentTypeMetadataTypes(FormView):
    form_class = DocumentTypeMetadataTypeRelationshipFormSet
    main_model = 'document_type'
    model = DocumentType
    model_permission = permission_document_type_edit
    pk_url_kwarg = 'document_type_id'
    submodel = MetadataType
    submodel_permission = permission_metadata_type_edit

    def form_valid(self, form):
        try:
            for instance in form:
                instance.save()
        except Exception as exception:
            messages.error(
                message=_(
                    'Error updating relationship; %s'
                ) % exception, request=self.request
            )
        else:
            messages.success(
                message=_('Relationships updated successfully'),
                request=self.request
            )

        return super(
            SetupDocumentTypeMetadataTypes, self
        ).form_valid(form=form)

    def get_extra_context(self):
        return {
            'form_display_mode_table': True,
            'no_results_icon': icon_metadata,
            'no_results_main_link': link_setup_metadata_type_create.resolve(
                context=RequestContext(request=self.request)
            ),
            'no_results_text': _(
                'Create metadata types to be able to associate them '
                'to this document type.'
            ),
            'no_results_title': _('There are no metadata types available'),
            'object': self.get_object(),
            'title': _(
                'Metadata types for document type: %s'
            ) % self.get_object()
        }

    def get_form_extra_kwargs(self):
        return {
            '_user': self.request.user,
        }

    def get_initial(self):
        obj = self.get_object()
        initial = []

        for element in self.get_queryset():
            initial.append({
                'document_type': obj,
                'main_model': self.main_model,
                'metadata_type': element,
            })
        return initial

    def get_object(self):
        obj = get_object_or_404(
            klass=self.model, pk=self.kwargs[self.pk_url_kwarg]
        )

        AccessControlList.objects.check_access(
            obj=obj, permissions=(self.model_permission,),
            user=self.request.user
        )
        return obj

    def get_post_action_redirect(self):
        return reverse(viewname='documents:document_type_list')

    def get_queryset(self):
        queryset = self.submodel.objects.all()
        return AccessControlList.objects.restrict_queryset(
            permission=self.submodel_permission,
            user=self.request.user, queryset=queryset
        )


class SetupMetadataTypesDocumentTypes(SetupDocumentTypeMetadataTypes):
    main_model = 'metadata_type'
    model = MetadataType
    model_permission = permission_metadata_type_edit
    pk_url_kwarg = 'metadata_type_id'
    submodel = DocumentType
    submodel_permission = permission_document_type_edit

    def get_extra_context(self):
        return {
            'form_display_mode_table': True,
            'object': self.get_object(),
            'title': _(
                'Document types for metadata type: %s'
            ) % self.get_object()
        }

    def get_initial(self):
        obj = self.get_object()
        initial = []

        for element in self.get_queryset():
            initial.append({
                'document_type': element,
                'main_model': self.main_model,
                'metadata_type': obj,
            })
        return initial

    def get_post_action_redirect(self):
        return reverse(viewname='metadata:setup_metadata_type_list')
