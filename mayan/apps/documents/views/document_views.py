import logging

from django.conf import settings
from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _, ungettext

from mayan.apps.acls.models import AccessControlList
from mayan.apps.common.classes import ModelQueryFields
from mayan.apps.converter.layers import layer_saved_transformations
from mayan.apps.converter.permissions import (
    permission_transformation_delete, permission_transformation_edit
)
from mayan.apps.views.generics import (
    FormView, MultipleObjectConfirmActionView, MultipleObjectFormActionView,
    SingleObjectDetailView, SingleObjectEditView, SingleObjectListView
)

from ..events import event_document_viewed
from ..forms import (
    DocumentForm, DocumentFilePageNumberForm, DocumentPropertiesForm,
    DocumentTypeFilteredSelectForm
)
from ..icons import (
    icon_document_list, icon_document_list_recent_access,
    icon_recent_added_document_list
)
from ..models import Document, RecentDocument
from ..permissions import (
    permission_document_properties_edit, permission_document_tools,
    permission_document_version_print, permission_document_view
)
from ..settings import setting_recent_added_count

from .document_version_views import DocumentVersionPreviewView

__all__ = (
    'DocumentListView', 'DocumentTypeChangeView', 'DocumentPropertiesEditView',
    'DocumentPreviewView', 'DocumentTransformationsClearView',
    'DocumentTransformationsCloneView', 'DocumentPrint',
    'RecentAccessDocumentListView', 'RecentAddedDocumentListView'
)
logger = logging.getLogger(name=__name__)


class DocumentListView(SingleObjectListView):
    object_permission = permission_document_view

    def get_context_data(self, **kwargs):
        try:
            return super().get_context_data(**kwargs)
        except Exception as exception:
            messages.error(
                message=_(
                    'Error retrieving document list: %(exception)s.'
                ) % {
                    'exception': exception
                }, request=self.request
            )
            self.object_list = Document.objects.none()
            return super().get_context_data(**kwargs)

    def get_document_queryset(self):
        return Document.objects.all()

    def get_extra_context(self):
        return {
            'hide_links': True,
            'hide_object': True,
            'list_as_items': True,
            'no_results_icon': icon_document_list,
            'no_results_text': _(
                'This could mean that no documents have been uploaded or '
                'that your user account has not been granted the view '
                'permission for any document or document type.'
            ),
            'no_results_title': _('No documents available'),
            'title': _('All documents'),
        }

    def get_source_queryset(self):
        queryset = ModelQueryFields.get(model=Document).get_queryset()
        return self.get_document_queryset().filter(pk__in=queryset)


class DocumentTypeChangeView(MultipleObjectFormActionView):
    form_class = DocumentTypeFilteredSelectForm
    model = Document
    object_permission = permission_document_properties_edit
    pk_url_kwarg = 'document_id'
    success_message = _(
        'Document type change request performed on %(count)d document'
    )
    success_message_plural = _(
        'Document type change request performed on %(count)d documents'
    )

    def get_extra_context(self):
        queryset = self.object_list

        result = {
            'submit_label': _('Change'),
            'title': ungettext(
                singular='Change the type of the selected document',
                plural='Change the type of the selected documents',
                number=queryset.count()
            )
        }

        if queryset.count() == 1:
            result.update(
                {
                    'object': queryset.first(),
                    'title': _(
                        'Change the type of the document: %s'
                    ) % queryset.first()
                }
            )

        return result

    def get_form_extra_kwargs(self):
        result = {
            'user': self.request.user
        }

        return result

    def object_action(self, form, instance):
        instance.document_type_change(
            document_type=form.cleaned_data['document_type'],
            _user=self.request.user
        )

        messages.success(
            message=_(
                'Document type for "%s" changed successfully.'
            ) % instance, request=self.request
        )


class DocumentPreviewView(DocumentVersionPreviewView):
    model = Document
    object_permission = permission_document_view
    pk_url_kwarg = 'document_id'

    def dispatch(self, request, *args, **kwargs):
        result = super(
            DocumentVersionPreviewView, self
        ).dispatch(request=request, *args, **kwargs)
        self.object.add_as_recent_document_for_user(user=request.user)
        event_document_viewed.commit(
            actor=request.user, target=self.object
        )

        return result

    def get_extra_context(self):
        return {
            'hide_labels': True,
            'object': self.object,
            'title': _('Preview of document: %s') % self.object,
        }


class DocumentPropertiesEditView(SingleObjectEditView):
    form_class = DocumentForm
    model = Document
    object_permission = permission_document_properties_edit
    pk_url_kwarg = 'document_id'

    def dispatch(self, request, *args, **kwargs):
        result = super().dispatch(request, *args, **kwargs)
        self.object.add_as_recent_document_for_user(user=request.user)
        return result

    def get_extra_context(self):
        return {
            'object': self.object,
            'title': _('Edit properties of document: %s') % self.object,
        }

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }

    def get_post_action_redirect(self):
        return reverse(
            viewname='documents:document_properties', kwargs={
                'document_id': self.object.pk
            }
        )


class DocumentPropertiesView(SingleObjectDetailView):
    form_class = DocumentPropertiesForm
    model = Document
    object_permission = permission_document_view
    pk_url_kwarg = 'document_id'

    def dispatch(self, request, *args, **kwargs):
        result = super().dispatch(request, *args, **kwargs)
        self.object.add_as_recent_document_for_user(request.user)
        return result

    def get_extra_context(self):
        return {
            'document': self.object,
            'object': self.object,
            'title': _('Properties of document: %s') % self.object,
        }


class DocumentTransformationsClearView(MultipleObjectConfirmActionView):
    model = Document
    object_permission = permission_transformation_delete
    pk_url_kwarg = 'document_id'
    success_message = _(
        'Transformation clear request processed for %(count)d document'
    )
    success_message_plural = _(
        'Transformation clear request processed for %(count)d documents'
    )

    def get_extra_context(self):
        queryset = self.object_list

        result = {
            'title': ungettext(
                singular='Clear all the page transformations for the selected document?',
                plural='Clear all the page transformations for the selected document?',
                number=queryset.count()
            )
        }

        if queryset.count() == 1:
            result.update(
                {
                    'object': queryset.first(),
                    'title': _(
                        'Clear all the page transformations for the '
                        'document: %s?'
                    ) % queryset.first()
                }
            )

        return result

    def object_action(self, form, instance):
        try:
            for page in instance.pages.all():
                layer_saved_transformations.get_transformations_for(obj=page).delete()
        except Exception as exception:
            messages.error(
                message=_(
                    'Error deleting the page transformations for '
                    'document: %(document)s; %(error)s.'
                ) % {
                    'document': instance, 'error': exception
                }, request=self.request
            )


class DocumentTransformationsCloneView(FormView):
    form_class = DocumentFilePageNumberForm

    def form_valid(self, form):
        instance = self.get_object()

        try:
            target_pages = instance.pages.exclude(
                pk=form.cleaned_data['page'].pk
            )

            with transaction.atomic():
                for page in target_pages:
                    layer_saved_transformations.get_transformations_for(obj=page).delete()

                layer_saved_transformations.copy_transformations(
                    source=form.cleaned_data['page'], targets=target_pages
                )
        except Exception as exception:
            if settings.DEBUG:
                raise
            else:
                messages.error(
                    message=_(
                        'Error cloning the page transformations for '
                        'document: %(document)s; %(error)s.'
                    ) % {
                        'document': instance, 'error': exception
                    }, request=self.request
                )
        else:
            messages.success(
                message=_('Transformations cloned successfully.'),
                request=self.request
            )

        return super().form_valid(form=form)

    def get_form_extra_kwargs(self):
        return {
            'document': self.get_object()
        }

    def get_extra_context(self):
        instance = self.get_object()

        context = {
            'object': instance,
            'submit_label': _('Submit'),
            'title': _(
                'Clone page transformations for document: %s'
            ) % instance,
        }

        return context

    def get_object(self):
        instance = get_object_or_404(
            klass=Document, pk=self.kwargs['document_id']
        )

        AccessControlList.objects.check_access(
            obj=instance, permissions=(permission_transformation_edit,),
            user=self.request.user
        )

        instance.add_as_recent_document_for_user(self.request.user)

        return instance


class RecentAccessDocumentListView(DocumentListView):
    def get_document_queryset(self):
        return RecentDocument.objects.get_for_user(user=self.request.user)

    def get_extra_context(self):
        context = super().get_extra_context()
        context.update(
            {
                'no_results_icon': icon_document_list_recent_access,
                'no_results_text': _(
                    'This view will list the latest documents viewed or '
                    'manipulated in any way by this user account.'
                ),
                'no_results_title': _(
                    'There are no recently accessed document'
                ),
                'title': _('Recently accessed'),
            }
        )
        return context


class RecentAddedDocumentListView(DocumentListView):
    def get_document_queryset(self):
        queryset = ModelQueryFields.get(model=Document).get_queryset()

        return queryset.filter(
            pk__in=queryset.order_by('-date_added')[
                :setting_recent_added_count.value
            ].values('pk')
        ).order_by('-date_added')

    def get_extra_context(self):
        context = super().get_extra_context()
        context.update(
            {
                'no_results_icon': icon_recent_added_document_list,
                'no_results_text': _(
                    'This view will list the latest documents uploaded '
                    'in the system.'
                ),
                'no_results_title': _(
                    'There are no recently added document'
                ),
                'title': _('Recently added'),
            }
        )
        return context
