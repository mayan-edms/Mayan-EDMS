from __future__ import absolute_import, unicode_literals

import base64
import logging
import urlparse

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import resolve, reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.http import urlencode
from django.utils.translation import ugettext_lazy as _, ungettext
from django.views.generic import RedirectView

from acls.models import AccessControlList
from common.compressed_files import CompressedFile
from common.generics import (
    ConfirmView, SimpleView, SingleObjectCreateView, SingleObjectDeleteView,
    SingleObjectDetailView, SingleObjectEditView, SingleObjectListView
)
from common.mixins import MultipleInstanceActionMixin
from converter.literals import (
    DEFAULT_PAGE_NUMBER, DEFAULT_ROTATION, DEFAULT_ZOOM_LEVEL
)
from converter.models import Transformation
from converter.permissions import permission_transformation_delete
from filetransfers.api import serve_file
from permissions import Permission

from .events import event_document_download, event_document_view
from .forms import (
    DocumentDownloadForm, DocumentForm, DocumentPageForm, DocumentPreviewForm,
    DocumentPropertiesForm, DocumentTypeSelectForm,
    DocumentTypeFilenameForm_create, PrintForm
)
from .literals import DOCUMENT_IMAGE_TASK_TIMEOUT, PAGE_RANGE_RANGE
from .models import (
    DeletedDocument, Document, DocumentType, DocumentPage,
    DocumentTypeFilename, DocumentVersion, RecentDocument
)
from .permissions import (
    permission_document_delete, permission_document_download,
    permission_document_print, permission_document_properties_edit,
    permission_document_restore, permission_document_tools,
    permission_document_trash, permission_document_type_create,
    permission_document_type_delete, permission_document_type_edit,
    permission_document_type_view, permission_document_version_revert,
    permission_document_view, permission_empty_trash
)
from .settings import (
    setting_preview_size, setting_rotation_step, setting_zoom_percent_step,
    setting_zoom_max_level, setting_zoom_min_level
)
from .tasks import (
    task_clear_image_cache, task_get_document_page_image,
    task_update_page_count
)
from .utils import parse_range

logger = logging.getLogger(__name__)


class ClearImageCacheView(ConfirmView):
    extra_context = {
        'title': _('Clear the document image cache?')
    }
    view_permission = permission_document_tools

    def view_action(self):
        task_clear_image_cache.apply_async()
        messages.success(
            self.request, _('Document cache clearing queued successfully.')
        )


class DocumentListView(SingleObjectListView):
    extra_context = {
        'hide_links': True,
        'title': _('All documents'),
    }

    object_permission = permission_document_view

    def get_document_queryset(self):
        return Document.objects.defer('description', 'uuid', 'date_added', 'language', 'in_trash', 'deleted_date_time').all()

    def get_queryset(self):
        self.queryset = self.get_document_queryset().filter(is_stub=False)
        return super(DocumentListView, self).get_queryset()


class DeletedDocumentListView(DocumentListView):
    object_permission = None

    extra_context = {
        'hide_link': True,
        'title': _('Documents in trash'),
    }

    def get_document_queryset(self):
        queryset = Document.trash.all()

        try:
            Permission.check_permissions(
                self.request.user, (permission_document_view,)
            )
        except PermissionDenied:
            queryset = AccessControlList.objects.filter_by_access(
                permission_document_view, self.request.user, queryset
            )

        return DeletedDocument.objects.filter(
            pk__in=queryset.values_list('pk', flat=True)
        )


class DeletedDocumentDeleteView(ConfirmView):
    extra_context = {
        'title': _('Delete the selected document?')
    }

    def object_action(self, instance):
        source_document = get_object_or_404(
            Document.passthrough, pk=instance.pk
        )

        try:
            Permission.check_permissions(
                self.request.user, (permission_document_delete,)
            )
        except PermissionDenied:
            AccessControlList.objects.check_access(
                permission_document_delete, self.request.user, source_document
            )

        instance.delete()

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


class DocumentRestoreView(ConfirmView):
    extra_context = {
        'title': _('Restore the selected document?')
    }

    def object_action(self, instance):
        source_document = get_object_or_404(
            Document.passthrough, pk=instance.pk
        )

        try:
            Permission.check_permissions(
                self.request.user, (permission_document_restore,)
            )
        except PermissionDenied:
            AccessControlList.objects.check_access(
                permission_document_restore, self.request.user, source_document
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


class DocumentPageListView(SingleObjectListView):
    def dispatch(self, request, *args, **kwargs):
        try:
            Permission.check_permissions(
                self.request.user, (permission_document_view,)
            )
        except PermissionDenied:
            AccessControlList.objects.check_access(
                permission_document_view, self.request.user,
                self.get_document()
            )

        return super(
            DocumentPageListView, self
        ).dispatch(request, *args, **kwargs)

    def get_document(self):
        return get_object_or_404(Document, pk=self.kwargs['pk'])

    def get_queryset(self):
        return self.get_document().pages.all()

    def get_extra_context(self):
        return {
            'object': self.get_document(),
            'title': _('Pages for document: %s') % self.get_document(),
        }


class DocumentPageView(SimpleView):
    template_name = 'appearance/generic_form.html'

    def dispatch(self, request, *args, **kwargs):
        try:
            Permission.check_permissions(
                request.user, (permission_document_view,)
            )
        except PermissionDenied:
            AccessControlList.objects.check_access(
                permission_document_view, request.user,
                self.get_object().document
            )
        return super(
            DocumentPageView, self
        ).dispatch(request, *args, **kwargs)

    def get_extra_context(self):
        zoom = int(self.request.GET.get('zoom', DEFAULT_ZOOM_LEVEL))
        rotation = int(self.request.GET.get('rotation', DEFAULT_ROTATION))
        document_page_form = DocumentPageForm(
            instance=self.get_object(), zoom=zoom, rotation=rotation
        )

        base_title = _('Image of: %s') % self.get_object()

        if zoom != DEFAULT_ZOOM_LEVEL:
            zoom_text = '(%d%%)' % zoom
        else:
            zoom_text = ''

        return {
            'form': document_page_form,
            'hide_labels': True,
            'navigation_object_list': ('page',),
            'page': self.get_object(),
            'rotation': rotation,
            'title': ' '.join([base_title, zoom_text]),
            'read_only': True,
            'zoom': zoom,
        }

    def get_object(self):
        return get_object_or_404(DocumentPage, pk=self.kwargs['pk'])


class DocumentPageViewResetView(RedirectView):
    pattern_name = 'documents:document_page_view'


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


class DocumentTrashView(ConfirmView):
    def get_extra_context(self):
        return {
            'object': self.get_object(),
            'title': _('Move "%s" to the trash?') % self.get_object()
        }

    def get_object(self):
        return get_object_or_404(Document, pk=self.kwargs['pk'])

    def get_post_action_redirect(self):
        return reverse('documents:document_list_recent')

    def object_action(self, instance):
        try:
            Permission.check_permissions(
                self.request.user, (permission_document_trash,)
            )
        except PermissionDenied:
            AccessControlList.objects.check_access(
                permission_document_trash, self.request.user, instance
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


class DocumentTypeDocumentListView(DocumentListView):
    def get_document_type(self):
        return get_object_or_404(DocumentType, pk=self.kwargs['pk'])

    def get_document_queryset(self):
        return self.get_document_type().documents.all()

    def get_extra_context(self):
        return {
            'hide_links': True,
            'object': self.get_document_type(),
            'title': _('Documents of type: %s') % self.get_document_type()
        }


class DocumentTypeListView(SingleObjectListView):
    model = DocumentType
    view_permission = permission_document_type_view

    def get_extra_context(self):
        return {
            'hide_link': True,
            'title': _('Document types'),
        }


class DocumentTypeCreateView(SingleObjectCreateView):
    fields = (
        'label', 'trash_time_period', 'trash_time_unit', 'delete_time_period',
        'delete_time_unit'
    )
    model = DocumentType
    post_action_redirect = reverse_lazy('documents:document_type_list')
    view_permission = permission_document_type_create

    def get_extra_context(self):
        return {
            'title': _('Create document type'),
        }


class DocumentTypeDeleteView(SingleObjectDeleteView):
    model = DocumentType
    post_action_redirect = reverse_lazy('documents:document_type_list')
    view_permission = permission_document_type_delete

    def get_extra_context(self):
        return {
            'message': _('All documents of this type will be deleted too.'),
            'object': self.get_object(),
            'title': _('Delete the document type: %s?') % self.get_object(),
        }


class DocumentTypeEditView(SingleObjectEditView):
    fields = (
        'label', 'trash_time_period', 'trash_time_unit', 'delete_time_period',
        'delete_time_unit'
    )
    model = DocumentType
    post_action_redirect = reverse_lazy('documents:document_type_list')
    view_permission = permission_document_type_edit

    def get_extra_context(self):
        return {
            'object': self.get_object(),
            'title': _('Edit document type: %s') % self.get_object(),
        }


class DocumentTypeFilenameCreateView(SingleObjectCreateView):
    form_class = DocumentTypeFilenameForm_create

    def dispatch(self, request, *args, **kwargs):
        try:
            Permission.check_permissions(
                request.user, (permission_document_type_edit,)
            )
        except PermissionDenied:
            AccessControlList.objects.check_access(
                permission_document_type_edit, request.user,
                self.get_document_type()
            )

        return super(DocumentTypeFilenameCreateView, self).dispatch(
            request, *args, **kwargs
        )

    def get_document_type(self):
        return get_object_or_404(DocumentType, pk=self.kwargs['pk'])

    def get_extra_context(self):
        return {
            'document_type': self.get_document_type(),
            'navigation_object_list': ('document_type',),
            'title': _(
                'Create quick label for document type: %s'
            ) % self.get_document_type(),
        }

    def get_instance_extra_data(self):
        return {'document_type': self.get_document_type()}


class DocumentTypeFilenameEditView(SingleObjectEditView):
    fields = ('enabled', 'filename',)
    model = DocumentTypeFilename
    view_permission = permission_document_type_edit

    def get_extra_context(self):
        document_type_filename = self.get_object()

        return {
            'document_type': document_type_filename.document_type,
            'filename': document_type_filename,
            'navigation_object_list': ('document_type', 'filename',),
            'title': _(
                'Edit quick label "%(filename)s" from document type '
                '"%(document_type)s"'
            ) % {
                'document_type': document_type_filename.document_type,
                'filename': document_type_filename
            },
        }

    def get_post_action_redirect(self):
        return reverse(
            'documents:document_type_filename_list',
            args=(self.get_object().document_type.pk,)
        )


class DocumentTypeFilenameDeleteView(SingleObjectDeleteView):
    model = DocumentTypeFilename
    view_permission = permission_document_type_edit

    def get_extra_context(self):
        return {
            'document_type': self.get_object().document_type,
            'filename': self.get_object(),
            'navigation_object_list': ('document_type', 'filename',),
            'title': _(
                'Delete the quick label: %(label)s, from document type '
                '"%(document_type)s"?'
            ) % {
                'document_type': self.get_object().document_type,
                'label': self.get_object()
            },
        }

    def get_post_action_redirect(self):
        return reverse(
            'documents:document_type_filename_list',
            args=(self.get_object().document_type.pk,)
        )


class DocumentTypeFilenameListView(SingleObjectListView):
    model = DocumentType
    view_permission = permission_document_type_view

    def get_document_type(self):
        return get_object_or_404(DocumentType, pk=self.kwargs['pk'])

    def get_extra_context(self):
        return {
            'document_type': self.get_document_type(),
            'hide_link': True,
            'navigation_object_list': ('document_type',),
            'title': _(
                'Quick labels for document type: %s'
            ) % self.get_document_type(),
        }

    def get_queryset(self):
        return self.get_document_type().filenames.all()


class DocumentVersionListView(SingleObjectListView):
    def dispatch(self, request, *args, **kwargs):
        try:
            Permission.check_permissions(
                request.user, (permission_document_view,)
            )
        except PermissionDenied:
            AccessControlList.objects.check_access(
                permission_document_view, request.user, self.get_document()
            )

        self.get_document().add_as_recent_document_for_user(request.user)

        return super(
            DocumentVersionListView, self
        ).dispatch(request, *args, **kwargs)

    def get_document(self):
        return get_object_or_404(Document, pk=self.kwargs['pk'])

    def get_extra_context(self):
        return {
            'hide_object': True, 'object': self.get_document(),
            'title': _('Versions of document: %s') % self.get_document(),
        }

    def get_queryset(self):
        return self.get_document().versions.order_by('-timestamp')


class DocumentVersionRevertView(ConfirmView):
    object_permission = permission_document_version_revert
    object_permission_related = 'document'

    def get_extra_context(self):
        return {
            'message': _(
                'All later version after this one will be deleted too.'
            ),
            'object': self.get_object().document,
            'title': _('Revert to this version?'),
        }

    def get_object(self):
        return get_object_or_404(DocumentVersion, pk=self.kwargs['pk'])

    def view_action(self):
        try:
            self.get_object().revert(_user=self.request.user)
            messages.success(
                self.request, _('Document version reverted successfully')
            )
        except Exception as exception:
            messages.error(
                self.request,
                _('Error reverting document version; %s') % exception
            )


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
            deleted_document.delete()

        messages.success(self.request, _('Trash emptied successfully'))


class RecentDocumentListView(DocumentListView):
    extra_context = {
        'hide_links': True,
        'title': _('Recent documents'),
    }

    def get_document_queryset(self):
        return RecentDocument.objects.get_for_user(self.request.user)


def document_document_type_edit(request, document_id=None, document_id_list=None):
    post_action_redirect = None

    if document_id:
        queryset = Document.objects.filter(pk=document_id)
        post_action_redirect = reverse('documents:document_list_recent')
    elif document_id_list:
        queryset = Document.objects.filter(pk__in=document_id_list)

    try:
        Permission.check_permissions(
            request.user, (permission_document_properties_edit,)
        )
    except PermissionDenied:
        queryset = AccessControlList.objects.filter_by_access(
            permission_document_properties_edit, request.user, queryset
        )

    if not queryset:
        if document_id:
            raise PermissionDenied
        else:
            messages.error(request, _('Must provide at least one document.'))
            return HttpResponseRedirect(
                request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))
            )

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))))

    if request.method == 'POST':
        form = DocumentTypeSelectForm(request.POST, user=request.user)
        if form.is_valid():

            for instance in queryset:
                instance.set_document_type(
                    form.cleaned_data['document_type'], _user=request.user
                )

                messages.success(
                    request, _(
                        'Document type for "%s" changed successfully.'
                    ) % instance
                )
            return HttpResponseRedirect(next)
    else:
        form = DocumentTypeSelectForm(
            initial={'document_type': queryset.first().document_type},
            user=request.user
        )

    context = {
        'form': form,
        'submit_label': _('Submit'),
        'previous': previous,
        'next': next,
        'title': ungettext(
            'Change the type of the selected document.',
            'Change the type of the selected documents.',
            queryset.count()
        )
    }

    if queryset.count() == 1:
        context['object'] = queryset.first()

    return render_to_response(
        'appearance/generic_form.html', context,
        context_instance=RequestContext(request)
    )


def document_multiple_document_type_edit(request):
    return document_document_type_edit(
        request, document_id_list=request.GET.get(
            'id_list', request.POST.get('id_list', '')
        ).split(',')
    )


# TODO: Get rid of this view and convert widget to use API and base64 only images
def get_document_image(request, document_id, size=setting_preview_size.value):
    document = get_object_or_404(Document.passthrough, pk=document_id)
    try:
        Permission.check_permissions(request.user, (permission_document_view,))
    except PermissionDenied:
        AccessControlList.objects.check_access(
            permission_document_view, request.user, document
        )

    page = int(request.GET.get('page', DEFAULT_PAGE_NUMBER))

    zoom = int(request.GET.get('zoom', DEFAULT_ZOOM_LEVEL))

    version = int(request.GET.get('version', document.latest_version.pk))

    if zoom < setting_zoom_min_level.value:
        zoom = setting_zoom_min_level.value

    if zoom > setting_zoom_max_level.value:
        zoom = setting_zoom_max_level.value

    rotation = int(request.GET.get('rotation', DEFAULT_ROTATION)) % 360

    document_page = document.pages.get(page_number=page)

    task = task_get_document_page_image.apply_async(kwargs=dict(document_page_id=document_page.pk, size=size, zoom=zoom, rotation=rotation, as_base64=True, version=version))
    data = task.get(timeout=DOCUMENT_IMAGE_TASK_TIMEOUT)
    return HttpResponse(base64.b64decode(data.partition('base64,')[2]), content_type='image')


def document_download(request, document_id=None, document_id_list=None, document_version_pk=None):
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))))

    if document_id:
        documents = Document.objects.filter(pk=document_id)
    elif document_id_list:
        documents = Document.objects.filter(pk__in=document_id_list)
    elif document_version_pk:
        documents = Document.objects.filter(
            pk=get_object_or_404(
                DocumentVersion, pk=document_version_pk
            ).document.pk
        )

    try:
        Permission.check_permissions(
            request.user, (permission_document_download,)
        )
    except PermissionDenied:
        documents = AccessControlList.objects.filter_by_access(
            permission_document_download, request.user, documents
        )

    if not documents:
        messages.error(
            request, _('Must provide at least one document or version.')
        )
        return HttpResponseRedirect(
            request.META.get(
                'HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL)
            )
        )

    if document_version_pk:
        queryset = DocumentVersion.objects.filter(pk=document_version_pk)
    else:
        queryset = DocumentVersion.objects.filter(
            pk__in=[document.latest_version.pk for document in documents]
        )

    subtemplates_list = []
    subtemplates_list.append(
        {
            'name': 'appearance/generic_list_subtemplate.html',
            'context': {
                'title': _('Documents to be downloaded'),
                'object_list': queryset,
                'hide_link': True,
                'hide_object': True,
                'hide_links': True,
                'scrollable_content': True,
                'scrollable_content_height': '200px',
                'extra_columns': (
                    {'name': _('Document'), 'attribute': 'document'},
                    {'name': _('Date and time'), 'attribute': 'timestamp'},
                    {'name': _('MIME type'), 'attribute': 'mimetype'},
                    {'name': _('Encoding'), 'attribute': 'encoding'},
                ),
            }
        }
    )

    if request.method == 'POST':
        form = DocumentDownloadForm(request.POST, queryset=queryset)
        if form.is_valid():
            if form.cleaned_data['compressed'] or queryset.count() > 1:
                try:
                    compressed_file = CompressedFile()
                    for document_version in queryset:
                        descriptor = document_version.open()
                        compressed_file.add_file(
                            descriptor,
                            arcname=document_version.document.label
                        )
                        descriptor.close()
                        event_document_download.commit(
                            actor=request.user,
                            target=document_version.document
                        )

                    compressed_file.close()

                    return serve_file(
                        request,
                        compressed_file.as_file(
                            form.cleaned_data['zip_filename']
                        ),
                        save_as='"%s"' % form.cleaned_data['zip_filename'],
                        content_type='application/zip'
                    )
                except Exception as exception:
                    if settings.DEBUG:
                        raise
                    else:
                        messages.error(request, exception)
                        return HttpResponseRedirect(
                            request.META['HTTP_REFERER']
                        )
            else:
                try:
                    # Test permissions and trigger exception
                    fd = queryset.first().open()
                    fd.close()
                    event_document_download.commit(
                        actor=request.user, target=queryset.first().document
                    )
                    return serve_file(
                        request,
                        queryset.first().file,
                        save_as='"%s"' % queryset.first().document.label,
                        content_type=queryset.first().mimetype if queryset.first().mimetype else 'application/octet-stream'
                    )
                except Exception as exception:
                    if settings.DEBUG:
                        raise
                    else:
                        messages.error(request, exception)
                        return HttpResponseRedirect(
                            request.META['HTTP_REFERER']
                        )

    else:
        form = DocumentDownloadForm(queryset=queryset)

    context = {
        'form': form,
        'previous': previous,
        'submit_label': _('Download'),
        'subtemplates_list': subtemplates_list,
        'title': _('Download documents'),
    }

    if queryset.count() == 1:
        context['object'] = queryset.first().document

    return render_to_response(
        'appearance/generic_form.html',
        context,
        context_instance=RequestContext(request)
    )


def document_multiple_download(request):
    return document_download(
        request, document_id_list=request.GET.get(
            'id_list', request.POST.get('id_list', '')
        ).split(',')
    )


def document_update_page_count(request, document_id=None, document_id_list=None):
    if document_id:
        documents = Document.objects.filter(pk=document_id)
    elif document_id_list:
        documents = Document.objects.filter(pk__in=document_id_list)

    if not documents:
        messages.error(request, _('At least one document must be selected.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL)))

    try:
        Permission.check_permissions(
            request.user, (permission_document_tools,)
        )
    except PermissionDenied:
        documents = AccessControlList.objects.filter_by_access(
            permission_document_tools, request.user, documents
        )

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))))

    if request.method == 'POST':
        for document in documents:
            task_update_page_count.apply_async(
                kwargs={'version_id': document.latest_version.pk}
            )

        messages.success(
            request,
            ungettext(
                _('Document queued for page count recalculation.'),
                _('Documents queued for page count recalculation.'),
                documents.count()
            )
        )
        return HttpResponseRedirect(previous)

    context = {
        'previous': previous,
        'title': ungettext(
            'Recalculate the page count of the selected document?',
            'Recalculate the page count of the selected documents?',
            documents.count()
        )
    }

    if documents.count() == 1:
        context['object'] = documents.first()

    return render_to_response(
        'appearance/generic_confirm.html', context,
        context_instance=RequestContext(request)
    )


def document_multiple_update_page_count(request):
    return document_update_page_count(
        request, document_id_list=request.GET.get(
            'id_list', request.POST.get('id_list', '')
        ).split(',')
    )


def document_clear_transformations(request, document_id=None, document_id_list=None):
    if document_id:
        documents = Document.objects.filter(pk=document_id)
        post_redirect = documents[0].get_absolute_url()
    elif document_id_list:
        documents = Document.objects.filter(pk__in=document_id_list)
        post_redirect = None

    if not documents:
        messages.error(request, _('Must provide at least one document.'))
        return HttpResponseRedirect(
            request.META.get(
                'HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL)
            )
        )

    try:
        Permission.check_permissions(
            request.user, (permission_transformation_delete,)
        )
    except PermissionDenied:
        documents = AccessControlList.objects.filter_by_access(
            permission_transformation_delete, request.user, documents
        )

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', post_redirect or reverse('documents:document_list'))))
    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', post_redirect or reverse('documents:document_list'))))

    if request.method == 'POST':
        for document in documents:
            try:
                for page in document.pages.all():
                    Transformation.objects.get_for_model(page).delete()
            except Exception as exception:
                messages.error(
                    request, _(
                        'Error deleting the page transformations for '
                        'document: %(document)s; %(error)s.'
                    ) % {
                        'document': document, 'error': exception
                    }
                )
            else:
                messages.success(
                    request, _(
                        'All the page transformations for document: %s, '
                        'have been deleted successfully.'
                    ) % document
                )

        return HttpResponseRedirect(next)

    context = {
        'delete_view': True,
        'next': next,
        'previous': previous,
        'title': ungettext(
            'Clear all the page transformations for the selected document?',
            'Clear all the page transformations for the selected documents?',
            documents.count()
        )
    }

    if documents.count() == 1:
        context['object'] = documents.first()

    return render_to_response(
        'appearance/generic_confirm.html', context,
        context_instance=RequestContext(request)
    )


def document_multiple_clear_transformations(request):
    return document_clear_transformations(
        request, document_id_list=request.GET.get(
            'id_list', request.POST.get('id_list', '')
        ).split(',')
    )


def document_page_navigation_next(request, document_page_id):
    document_page = get_object_or_404(DocumentPage, pk=document_page_id)

    try:
        Permission.check_permissions(request.user, (permission_document_view,))
    except PermissionDenied:
        AccessControlList.objects.check_access(permission_document_view, request.user, document_page.document)

    view = resolve(urlparse.urlparse(request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))).path).view_name

    if document_page.page_number >= document_page.siblings.count():
        messages.warning(request, _('There are no more pages in this document'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL)))
    else:
        document_page = get_object_or_404(document_page.siblings, page_number=document_page.page_number + 1)
        return HttpResponseRedirect('{0}?{1}'.format(reverse(view, args=(document_page.pk,)), request.GET.urlencode()))


def document_page_navigation_previous(request, document_page_id):
    document_page = get_object_or_404(DocumentPage, pk=document_page_id)

    try:
        Permission.check_permissions(request.user, (permission_document_view,))
    except PermissionDenied:
        AccessControlList.objects.check_access(permission_document_view, request.user, document_page.document)

    view = resolve(urlparse.urlparse(request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))).path).view_name

    if document_page.page_number <= 1:
        messages.warning(request, _('You are already at the first page of this document'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL)))
    else:
        document_page = get_object_or_404(document_page.siblings, page_number=document_page.page_number - 1)
        return HttpResponseRedirect('{0}?{1}'.format(reverse(view, args=(document_page.pk,)), request.GET.urlencode()))


def document_page_navigation_first(request, document_page_id):
    document_page = get_object_or_404(DocumentPage, pk=document_page_id)
    document_page = get_object_or_404(document_page.siblings, page_number=1)

    try:
        Permission.check_permissions(request.user, (permission_document_view,))
    except PermissionDenied:
        AccessControlList.objects.check_access(permission_document_view, request.user, document_page.document)

    view = resolve(urlparse.urlparse(request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))).path).view_name

    return HttpResponseRedirect('{0}?{1}'.format(reverse(view, args=(document_page.pk,)), request.GET.urlencode()))


def document_page_navigation_last(request, document_page_id):
    document_page = get_object_or_404(DocumentPage, pk=document_page_id)
    document_page = get_object_or_404(document_page.siblings, page_number=document_page.siblings.count())

    try:
        Permission.check_permissions(request.user, (permission_document_view,))
    except PermissionDenied:
        AccessControlList.objects.check_access(permission_document_view, request.user, document_page.document)

    view = resolve(urlparse.urlparse(request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))).path).view_name

    return HttpResponseRedirect('{0}?{1}'.format(reverse(view, args=(document_page.pk,)), request.GET.urlencode()))


def transform_page(request, document_page_id, zoom_function=None, rotation_function=None):
    document_page = get_object_or_404(DocumentPage, pk=document_page_id)

    try:
        Permission.check_permissions(request.user, (permission_document_view,))
    except PermissionDenied:
        AccessControlList.objects.check_access(permission_document_view, request.user, document_page.document)

    view = resolve(urlparse.urlparse(request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))).path).view_name

    # Get the query string from the referer url
    query = urlparse.urlparse(request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))).query
    # Parse the query string and get the zoom value
    # parse_qs return a dictionary whose values are lists
    zoom = int(urlparse.parse_qs(query).get('zoom', ['100'])[0])
    rotation = int(urlparse.parse_qs(query).get('rotation', ['0'])[0])

    if zoom_function:
        zoom = zoom_function(zoom)

    if rotation_function:
        rotation = rotation_function(rotation)

    return HttpResponseRedirect(
        '?'.join([
            reverse(view, args=(document_page.pk,)),
            urlencode({'zoom': zoom, 'rotation': rotation})
        ])
    )


def document_page_zoom_in(request, document_page_id):
    return transform_page(
        request,
        document_page_id,
        zoom_function=lambda x: setting_zoom_max_level.value if x + setting_zoom_percent_step.value > setting_zoom_max_level.value else x + setting_zoom_percent_step.value
    )


def document_page_zoom_out(request, document_page_id):
    return transform_page(
        request,
        document_page_id,
        zoom_function=lambda x: setting_zoom_min_level.value if x - setting_zoom_percent_step.value < setting_zoom_min_level.value else x - setting_zoom_percent_step.value
    )


def document_page_rotate_right(request, document_page_id):
    return transform_page(
        request,
        document_page_id,
        rotation_function=lambda x: (x + setting_rotation_step.value) % 360
    )


def document_page_rotate_left(request, document_page_id):
    return transform_page(
        request,
        document_page_id,
        rotation_function=lambda x: (x - setting_rotation_step.value) % 360
    )


def document_print(request, document_id):
    document = get_object_or_404(Document, pk=document_id)

    try:
        Permission.check_permissions(request.user, (permission_document_print,))
    except PermissionDenied:
        AccessControlList.objects.check_access(permission_document_print, request.user, document)

    document.add_as_recent_document_for_user(request.user)

    post_redirect = None
    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', post_redirect or document.get_absolute_url())))

    if request.method == 'POST':
        form = PrintForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['page_group'] == PAGE_RANGE_RANGE:
                page_range = form.cleaned_data['page_range']

                if page_range:
                    page_range = parse_range(page_range)
                    pages = document.pages.filter(page_number__in=page_range)
                else:
                    pages = document.pages.all()
            else:
                pages = document.pages.all()

            return render_to_response('documents/document_print.html', {
                'appearance_type': 'plain',
                'object': document,
                'pages': pages,
                'title': _('Print: %s') % document,
            }, context_instance=RequestContext(request))
    else:
        form = PrintForm()

    return render_to_response('appearance/generic_form.html', {
        'form': form,
        'object': document,
        'next': next,
        'title': _('Print: %s') % document,
        'submit_label': _('Submit'),
    }, context_instance=RequestContext(request))
