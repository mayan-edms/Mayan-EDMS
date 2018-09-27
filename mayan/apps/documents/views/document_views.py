from __future__ import absolute_import, unicode_literals

import logging

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.http import urlencode
from django.utils.translation import ugettext_lazy as _, ungettext

from acls.models import AccessControlList
from common.compressed_files import ZipArchive
from common.exceptions import ActionError
from common.generics import (
    ConfirmView, FormView, MultipleObjectConfirmActionView,
    MultipleObjectFormActionView, SingleObjectDetailView,
    SingleObjectDownloadView, SingleObjectEditView, SingleObjectListView
)
from common.mixins import MultipleInstanceActionMixin
from common.utils import encapsulate
from converter.models import Transformation
from converter.permissions import (
    permission_transformation_delete, permission_transformation_edit
)

from ..events import event_document_download, event_document_view
from ..forms import (
    DocumentDownloadForm, DocumentForm, DocumentPageNumberForm,
    DocumentPreviewForm, DocumentPrintForm, DocumentPropertiesForm,
    DocumentTypeSelectForm,
)
from ..icons import (
    icon_document_list, icon_document_list_deleted,
    icon_document_list_favorites, icon_document_list_recent_access,
    icon_document_list_recent_added, icon_duplicated_document_list
)
from ..literals import PAGE_RANGE_RANGE, DEFAULT_ZIP_FILENAME
from ..models import (
    DeletedDocument, Document, DuplicatedDocument, FavoriteDocument,
    RecentDocument
)
from ..permissions import (
    permission_document_delete, permission_document_download,
    permission_document_print, permission_document_properties_edit,
    permission_document_restore, permission_document_tools,
    permission_document_trash, permission_document_view,
    permission_empty_trash
)
from ..settings import (
    setting_favorite_count, setting_print_width, setting_print_height,
    setting_recent_added_count
)
from ..tasks import task_delete_document, task_update_page_count
from ..utils import parse_range

logger = logging.getLogger(__name__)


class DocumentListView(SingleObjectListView):
    object_permission = permission_document_view
    queryset_slice = None

    def get_context_data(self, **kwargs):
        try:
            return super(DocumentListView, self).get_context_data(**kwargs)
        except Exception as exception:
            messages.error(
                self.request, _(
                    'Error retrieving document list: %(exception)s.'
                ) % {
                    'exception': exception
                }
            )
            self.object_list = Document.objects.none()
            return super(DocumentListView, self).get_context_data(**kwargs)

    def get_document_queryset(self):
        return Document.objects.defer(
            'description', 'uuid', 'date_added', 'language', 'in_trash',
            'deleted_date_time'
        ).all()

    def get_extra_context(self):
        return {
            'hide_links': True,
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

    def get_object_list(self):
        queryset = self.get_document_queryset().filter(is_stub=False)
        if self.queryset_slice:
            return queryset.__getitem__(slice(*self.queryset_slice))
        else:
            return queryset


class DeletedDocumentDeleteView(ConfirmView):
    extra_context = {
        'title': _('Delete the selected document?')
    }

    def object_action(self, instance):
        source_document = get_object_or_404(
            Document.passthrough, pk=instance.pk
        )

        AccessControlList.objects.check_access(
            permissions=permission_document_delete, user=self.request.user,
            obj=source_document
        )

        task_delete_document.apply_async(
            kwargs={'deleted_document_id': instance.pk}
        )

    def view_action(self):
        instance = get_object_or_404(DeletedDocument, pk=self.kwargs['pk'])
        self.object_action(instance=instance)
        messages.success(
            self.request, _('Document: %(document)s deleted.') % {
                'document': instance
            }
        )


class DeletedDocumentDeleteManyView(MultipleInstanceActionMixin, DeletedDocumentDeleteView):
    extra_context = {
        'title': _('Delete the selected documents?')
    }
    model = DeletedDocument
    success_message = '%(count)d document deleted.'
    success_message_plural = '%(count)d documents deleted.'


class DeletedDocumentListView(DocumentListView):
    object_permission = None

    def get_document_queryset(self):
        return AccessControlList.objects.filter_by_access(
            permission_document_view, self.request.user,
            queryset=DeletedDocument.trash.all()
        )

    def get_extra_context(self):
        context = super(DeletedDocumentListView, self).get_extra_context()
        context.update(
            {
                'hide_link': True,
                'no_results_icon': icon_document_list_deleted,
                'no_results_text': _(
                    'To avoid loss of data, documents are not deleted '
                    'instantly. First, they are placed in the trash can. '
                    'From here they can be then finally deleted or restored.'
                ),
                'no_results_title': _(
                    'There are no documents in the trash can'
                ),
                'title': _('Documents in trash'),
            }
        )
        return context


class DocumentDocumentTypeEditView(MultipleObjectFormActionView):
    form_class = DocumentTypeSelectForm
    model = Document
    object_permission = permission_document_properties_edit
    success_message = _(
        'Document type change request performed on %(count)d document'
    )
    success_message_plural = _(
        'Document type change request performed on %(count)d documents'
    )

    def get_extra_context(self):
        queryset = self.get_queryset()

        result = {
            'submit_label': _('Change'),
            'title': ungettext(
                'Change the type of the selected document',
                'Change the type of the selected documents',
                queryset.count()
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
        instance.set_document_type(
            form.cleaned_data['document_type'], _user=self.request.user
        )

        messages.success(
            self.request, _(
                'Document type for "%s" changed successfully.'
            ) % instance
        )


class DocumentDuplicatesListView(DocumentListView):
    def dispatch(self, request, *args, **kwargs):
        AccessControlList.objects.check_access(
            permissions=permission_document_view, user=self.request.user,
            obj=self.get_document()
        )

        return super(
            DocumentDuplicatesListView, self
        ).dispatch(request, *args, **kwargs)

    def get_document(self):
        return get_object_or_404(Document, pk=self.kwargs['pk'])

    def get_extra_context(self):
        context = super(DocumentDuplicatesListView, self).get_extra_context()
        context.update(
            {
                'no_results_icon': icon_duplicated_document_list,
                'no_results_text': _(
                    'Only exact copies of this document will be shown in the '
                    'this list.'
                ),
                'no_results_title': _(
                    'There are no duplicates for this document'
                ),
                'object': self.get_document(),
                'title': _('Duplicates for document: %s') % self.get_document(),
            }
        )
        return context

    def get_object_list(self):
        try:
            return DuplicatedDocument.objects.get(
                document=self.get_document()
            ).documents.all()
        except DuplicatedDocument.DoesNotExist:
            return Document.objects.none()


class DocumentEditView(SingleObjectEditView):
    form_class = DocumentForm
    model = Document
    object_permission = permission_document_properties_edit

    def dispatch(self, request, *args, **kwargs):
        result = super(
            DocumentEditView, self
        ).dispatch(request, *args, **kwargs)
        self.get_object().add_as_recent_document_for_user(request.user)
        return result

    def get_extra_context(self):
        return {
            'object': self.get_object(),
            'title': _('Edit properties of document: %s') % self.get_object(),
        }

    def get_save_extra_data(self):
        return {
            '_user': self.request.user
        }

    def get_post_action_redirect(self):
        return reverse(
            'documents:document_properties', args=(self.get_object().pk,)
        )


class DocumentPreviewView(SingleObjectDetailView):
    form_class = DocumentPreviewForm
    model = Document
    object_permission = permission_document_view

    def dispatch(self, request, *args, **kwargs):
        result = super(
            DocumentPreviewView, self
        ).dispatch(request, *args, **kwargs)
        self.get_object().add_as_recent_document_for_user(request.user)
        event_document_view.commit(
            actor=request.user, target=self.get_object()
        )

        return result

    def get_extra_context(self):
        return {
            'hide_labels': True,
            'object': self.get_object(),
            'title': _('Preview of document: %s') % self.get_object(),
        }


class DocumentRestoreView(ConfirmView):
    extra_context = {
        'title': _('Restore the selected document?')
    }

    def object_action(self, instance):
        source_document = get_object_or_404(
            Document.passthrough, pk=instance.pk
        )

        AccessControlList.objects.check_access(
            permissions=permission_document_restore, user=self.request.user,
            obj=source_document
        )

        instance.restore()

    def view_action(self):
        instance = get_object_or_404(DeletedDocument, pk=self.kwargs['pk'])

        self.object_action(instance=instance)

        messages.success(
            self.request, _('Document: %(document)s restored.') % {
                'document': instance
            }
        )


class DocumentRestoreManyView(MultipleInstanceActionMixin, DocumentRestoreView):
    extra_context = {
        'title': _('Restore the selected documents?')
    }
    model = DeletedDocument
    success_message = '%(count)d document restored.'
    success_message_plural = '%(count)d documents restored.'


class DocumentTrashView(ConfirmView):
    def get_extra_context(self):
        return {
            'object': self.get_object(),
            'title': _('Move "%s" to the trash?') % self.get_object()
        }

    def get_object(self):
        return get_object_or_404(Document, pk=self.kwargs['pk'])

    def get_post_action_redirect(self):
        return reverse('documents:document_list_recent_access')

    def object_action(self, instance):
        AccessControlList.objects.check_access(
            permissions=permission_document_trash, user=self.request.user,
            obj=instance
        )

        instance.delete()

    def view_action(self):
        instance = self.get_object()

        self.object_action(instance=instance)

        messages.success(
            self.request, _('Document: %(document)s moved to trash successfully.') % {
                'document': instance
            }
        )


class DocumentTrashManyView(MultipleInstanceActionMixin, DocumentTrashView):
    model = Document
    success_message = '%(count)d document moved to the trash.'
    success_message_plural = '%(count)d documents moved to the trash.'

    def get_extra_context(self):
        return {
            'title': _('Move the selected documents to the trash?')
        }


class DocumentView(SingleObjectDetailView):
    form_class = DocumentPropertiesForm
    model = Document
    object_permission = permission_document_view

    def dispatch(self, request, *args, **kwargs):
        result = super(DocumentView, self).dispatch(request, *args, **kwargs)
        self.get_object().add_as_recent_document_for_user(request.user)
        return result

    def get_extra_context(self):
        return {
            'document': self.get_object(),
            'object': self.get_object(),
            'title': _('Properties for document: %s') % self.get_object(),
        }


class EmptyTrashCanView(ConfirmView):
    extra_context = {
        'title': _('Empty trash?')
    }
    view_permission = permission_empty_trash
    action_cancel_redirect = post_action_redirect = reverse_lazy(
        'documents:document_list_deleted'
    )

    def view_action(self):
        for deleted_document in DeletedDocument.objects.all():
            task_delete_document.apply_async(
                kwargs={'deleted_document_id': deleted_document.pk}
            )

        messages.success(self.request, _('Trash emptied successfully'))


class DocumentDownloadFormView(FormView):
    form_class = DocumentDownloadForm
    model = Document
    multiple_download_view = 'documents:document_multiple_download'
    querystring_form_fields = ('compressed', 'zip_filename')
    single_download_view = 'documents:document_download'

    def form_valid(self, form):
        querystring_dictionary = {}

        for field in self.querystring_form_fields:
            data = form.cleaned_data[field]
            if data:
                querystring_dictionary[field] = data

        querystring_dictionary.update(
            {
                'id_list': ','.join(
                    map(str, self.queryset.values_list('pk', flat=True))
                )
            }
        )

        querystring = urlencode(querystring_dictionary, doseq=True)

        if self.queryset.count() > 1:
            url = reverse(self.multiple_download_view)
        else:
            url = reverse(
                self.single_download_view, args=(self.queryset.first().pk,)
            )

        return HttpResponseRedirect('{}?{}'.format(url, querystring))

    def get_document_queryset(self):
        id_list = self.request.GET.get(
            'id_list', self.request.POST.get('id_list', '')
        )

        if not id_list:
            id_list = self.kwargs['pk']

        return self.model.objects.filter(
            pk__in=id_list.split(',')
        ).filter(is_stub=False)

    def get_extra_context(self):
        subtemplates_list = [
            {
                'name': 'appearance/generic_list_items_subtemplate.html',
                'context': {
                    'object_list': self.queryset,
                    'hide_link': True,
                    'hide_links': True,
                    'hide_multi_item_actions': True,
                }
            }
        ]

        context = {
            'submit_label': _('Download'),
            'subtemplates_list': subtemplates_list,
            'title': _('Download documents'),
        }

        if self.queryset.count() == 1:
            context['object'] = self.queryset.first()

        return context

    def get_form_kwargs(self):
        kwargs = super(DocumentDownloadFormView, self).get_form_kwargs()
        self.queryset = self.get_queryset()
        kwargs.update({'queryset': self.queryset})
        return kwargs

    def get_queryset(self):
        return AccessControlList.objects.filter_by_access(
            permission_document_download, self.request.user,
            queryset=self.get_document_queryset()
        )


class DocumentDownloadView(SingleObjectDownloadView):
    model = Document
    # Set to None to disable the .get_object call
    object_permission = None

    @staticmethod
    def commit_event(item, request):
        if isinstance(item, Document):
            event_document_download.commit(
                actor=request.user,
                target=item
            )
        else:
            # TODO: Improve by adding a document version download event
            event_document_download.commit(
                actor=request.user,
                target=item.document
            )

    @staticmethod
    def get_item_file(item):
        return item.open()

    def get_document_queryset(self):
        id_list = self.request.GET.get(
            'id_list', self.request.POST.get('id_list', '')
        )

        if not id_list:
            id_list = self.kwargs['pk']

        queryset = self.model.objects.filter(pk__in=id_list.split(','))

        return AccessControlList.objects.filter_by_access(
            permission_document_download, self.request.user, queryset
        )

    def get_file(self):
        queryset = self.get_document_queryset()
        zip_filename = self.request.GET.get(
            'zip_filename', DEFAULT_ZIP_FILENAME
        )

        if self.request.GET.get('compressed') == 'True' or queryset.count() > 1:
            compressed_file = ZipArchive()
            compressed_file.create()
            for item in queryset:
                with DocumentDownloadView.get_item_file(item=item) as file_object:
                    compressed_file.add_file(
                        file_object=file_object,
                        filename=self.get_item_label(item=item)
                    )
                    DocumentDownloadView.commit_event(
                        item=item, request=self.request
                    )

            compressed_file.close()

            return DocumentDownloadView.VirtualFile(
                compressed_file.as_file(zip_filename), name=zip_filename
            )
        else:
            item = queryset.first()
            if item:
                DocumentDownloadView.commit_event(
                    item=item, request=self.request
                )
            else:
                raise PermissionDenied

            return DocumentDownloadView.VirtualFile(
                DocumentDownloadView.get_item_file(item=item),
                name=self.get_item_label(item=item)
            )

    def get_item_label(self, item):
        return item.label


class DocumentUpdatePageCountView(MultipleObjectConfirmActionView):
    model = Document
    object_permission = permission_document_tools
    success_message = _(
        '%(count)d document queued for page count recalculation'
    )
    success_message_plural = _(
        '%(count)d documents queued for page count recalculation'
    )

    def get_extra_context(self):
        queryset = self.get_queryset()

        result = {
            'title': ungettext(
                'Recalculate the page count of the selected document?',
                'Recalculate the page count of the selected documents?',
                queryset.count()
            )
        }

        if queryset.count() == 1:
            result.update(
                {
                    'object': queryset.first(),
                    'title': _(
                        'Recalculate the page count of the document: %s?'
                    ) % queryset.first()
                }
            )

        return result

    def object_action(self, form, instance):
        latest_version = instance.latest_version
        if latest_version:
            task_update_page_count.apply_async(
                kwargs={'version_id': latest_version.pk}
            )
        else:
            messages.error(
                self.request, _(
                    'Document "%(document)s" is empty. Upload at least one '
                    'document version before attempting to detect the '
                    'page count.'
                ) % {
                    'document': instance,
                }
            )


class DocumentTransformationsClearView(MultipleObjectConfirmActionView):
    model = Document
    object_permission = permission_transformation_delete
    success_message = _(
        'Transformation clear request processed for %(count)d document'
    )
    success_message_plural = _(
        'Transformation clear request processed for %(count)d documents'
    )

    def get_extra_context(self):
        queryset = self.get_queryset()

        result = {
            'title': ungettext(
                'Clear all the page transformations for the selected document?',
                'Clear all the page transformations for the selected document?',
                queryset.count()
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
                Transformation.objects.get_for_model(page).delete()
        except Exception as exception:
            messages.error(
                self.request, _(
                    'Error deleting the page transformations for '
                    'document: %(document)s; %(error)s.'
                ) % {
                    'document': instance, 'error': exception
                }
            )


class DocumentTransformationsCloneView(FormView):
    form_class = DocumentPageNumberForm

    def form_valid(self, form):
        instance = self.get_object()

        try:
            target_pages = instance.pages.exclude(
                pk=form.cleaned_data['page'].pk
            )

            for page in target_pages:
                Transformation.objects.get_for_model(page).delete()

            Transformation.objects.copy(
                source=form.cleaned_data['page'], targets=target_pages
            )
        except Exception as exception:
            messages.error(
                self.request, _(
                    'Error deleting the page transformations for '
                    'document: %(document)s; %(error)s.'
                ) % {
                    'document': instance, 'error': exception
                }
            )
        else:
            messages.success(
                self.request, _('Transformations cloned successfully.')
            )

        return super(DocumentTransformationsCloneView, self).form_valid(form=form)

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
        instance = get_object_or_404(Document, pk=self.kwargs['pk'])

        AccessControlList.objects.check_access(
            permissions=permission_transformation_edit,
            user=self.request.user, obj=instance
        )

        instance.add_as_recent_document_for_user(self.request.user)

        return instance


class DocumentPrint(FormView):
    form_class = DocumentPrintForm

    def dispatch(self, request, *args, **kwargs):
        instance = self.get_object()
        AccessControlList.objects.check_access(
            permissions=permission_document_print, user=self.request.user,
            obj=instance
        )

        instance.add_as_recent_document_for_user(self.request.user)

        self.page_group = self.request.GET.get('page_group')
        self.page_range = self.request.GET.get('page_range')
        return super(DocumentPrint, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if not self.page_group and not self.page_range:
            return super(DocumentPrint, self).get(request, *args, **kwargs)
        else:
            instance = self.get_object()

            if self.page_group == PAGE_RANGE_RANGE:
                if self.page_range:
                    page_range = parse_range(self.page_range)
                    pages = instance.pages.filter(page_number__in=page_range)
                else:
                    pages = instance.pages.all()
            else:
                pages = instance.pages.all()

            context = self.get_context_data()

            context.update(
                {
                    'appearance_type': 'plain',
                    'pages': pages,
                    'width': setting_print_width.value,
                    'height': setting_print_height.value,
                }
            )

            return self.render_to_response(context=context)

    def get_extra_context(self):
        instance = self.get_object()

        context = {
            'form_action': reverse(
                'documents:document_print', args=(instance.pk,)
            ),
            'object': instance,
            'submit_label': _('Submit'),
            'submit_method': 'GET',
            'submit_target': '_blank',
            'title': _('Print: %s') % instance,
        }

        return context

    def get_object(self):
        return get_object_or_404(Document, pk=self.kwargs['pk'])

    def get_template_names(self):
        if self.page_group or self.page_range:
            return ('documents/document_print.html',)
        else:
            return (self.template_name,)


class DuplicatedDocumentListView(DocumentListView):
    def get_document_queryset(self):
        return DuplicatedDocument.objects.get_duplicated_documents()

    def get_extra_context(self):
        context = super(DuplicatedDocumentListView, self).get_extra_context()
        context.update(
            {
                'extra_columns': (
                    {
                        'name': _('Duplicates'),
                        'attribute': encapsulate(
                            lambda document: DuplicatedDocument.objects.get(
                                document=document
                            ).documents.count()
                        )
                    },
                ),
                'no_results_icon': icon_duplicated_document_list,
                'no_results_text': _(
                    'Duplicates are documents that are composed of the exact '
                    'same file, down to the last byte. Files that have the '
                    'same text or OCR but are not identical or were saved '
                    'using a different file format will not appear as '
                    'duplicates.'
                ),
                'no_results_title': _(
                    'There are no duplicated documents'
                ),
                'title': _('Duplicated documents')
            }
        )
        return context


class FavoriteDocumentListView(DocumentListView):
    def get_document_queryset(self):
        return FavoriteDocument.objects.get_for_user(user=self.request.user)

    def get_extra_context(self):
        context = super(FavoriteDocumentListView, self).get_extra_context()
        context.update(
            {
                'no_results_icon': icon_document_list_favorites,
                'no_results_text': _(
                    'Favorited documents will be listed in this view. '
                    'Up to %(count)d documents can be favorited per user. '
                ) % {'count': setting_favorite_count.value},
                'no_results_title': _('There are no favorited documents.'),
                'title': _('Favorites'),
            }
        )
        return context


class FavoriteAddView(MultipleObjectConfirmActionView):
    model = Document
    object_permission = permission_document_view
    success_message = _(
        '%(count)d document added to favorites.'
    )
    success_message_plural = _(
        '%(count)d documents added to favorites.'
    )

    def get_extra_context(self):
        queryset = self.get_queryset()

        return {
            'submit_label': _('Add'),
            'submit_icon_class': icon_document_list_favorites,
            'title': ungettext(
                singular='Add the selected document to favorites',
                plural='Add the selected documents to favorites',
                number=queryset.count()
            )
        }

    def object_action(self, form, instance):
        FavoriteDocument.objects.add_for_user(
            user=self.request.user, document=instance
        )


class FavoriteRemoveView(MultipleObjectConfirmActionView):
    error_message = _('Document "%(instance)s" is not in favorites.')
    model = Document
    object_permission = permission_document_view
    success_message = _(
        '%(count)d document removed from favorites.'
    )
    success_message_plural = _(
        '%(count)d documents removed from favorites.'
    )

    def get_extra_context(self):
        queryset = self.get_queryset()

        return {
            'submit_label': _('Remove'),
            'submit_icon_class': icon_document_list_favorites,
            'title': ungettext(
                singular='Remove the selected document from favorites',
                plural='Remove the selected documents from favorites',
                number=queryset.count()
            )
        }

    def object_action(self, form, instance):
        try:
            FavoriteDocument.objects.remove_for_user(
                user=self.request.user, document=instance
            )
        except FavoriteDocument.DoesNotExist:
            raise ActionError


class RecentAccessDocumentListView(DocumentListView):
    def get_document_queryset(self):
        return RecentDocument.objects.get_for_user(user=self.request.user)

    def get_extra_context(self):
        context = super(RecentAccessDocumentListView, self).get_extra_context()
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
    queryset_slice = (0, setting_recent_added_count.value)

    def get_document_queryset(self):
        return Document.objects.order_by('-date_added')

    def get_extra_context(self):
        context = super(RecentAddedDocumentListView, self).get_extra_context()
        context.update(
            {
                'no_results_icon': icon_document_list_recent_added,
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
