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

from acls.models import AccessControlList
from common.compressed_files import CompressedFile
from common.mixins import MultipleInstanceActionMixin
from common.utils import encapsulate, pretty_size
from common.views import (
    ConfirmView, ParentChildListView, SingleObjectCreateView,
    SingleObjectDeleteView, SingleObjectEditView, SingleObjectListView
)
from common.widgets import two_state_template
from converter.literals import (
    DEFAULT_PAGE_NUMBER, DEFAULT_ROTATION, DEFAULT_ZOOM_LEVEL
)
from converter.models import Transformation
from converter.permissions import permission_transformation_delete
from filetransfers.api import serve_file
from permissions import Permission

from .events import (
    event_document_properties_edit, event_document_type_change
)
from .forms import (
    DocumentDownloadForm, DocumentForm, DocumentPageForm, DocumentPreviewForm,
    DocumentPropertiesForm, DocumentTypeFilenameForm,
    DocumentTypeFilenameForm_create, DocumentTypeSelectForm, PrintForm
)
from .literals import DOCUMENT_IMAGE_TASK_TIMEOUT
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


class DocumentListView(SingleObjectListView):
    extra_context = {
        'hide_links': True,
        'title': _('All documents'),
    }

    object_permission = permission_document_view

    def get_document_queryset(self):
        return Document.objects.all()

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
            AccessControlList.objects.check_access(
                permission_document_view, self.request.user, queryset
            )

        return DeletedDocument.objects.filter(
            pk__in=queryset.values_list('pk', flat=True)
        )


class DeletedDocumentDeleteView(ConfirmView):
    extra_context = {
        'title': _('Delete the selected document?')
    }

    def object_action(self, request, instance):
        source_document = get_object_or_404(
            Document.passthrough, pk=instance.pk
        )

        try:
            Permission.check_permissions(
                request.user, (permission_document_delete,)
            )
        except PermissionDenied:
            AccessControlList.objects.check_access(
                permission_document_delete, request.user, source_document
            )

        instance.delete()
        messages.success(request, _('Document: %(document)s deleted.') % {
            'document': instance}
        )

    def post(self, request, *args, **kwargs):
        document = get_object_or_404(DeletedDocument, pk=self.kwargs['pk'])
        self.object_action(request=request, instance=document)

        return HttpResponseRedirect(self.get_success_url())


class DocumentRestoreView(ConfirmView):
    extra_context = {
        'title': _('Restore the selected document?')
    }

    def object_action(self, request, instance):
        source_document = get_object_or_404(
            Document.passthrough, pk=instance.pk
        )

        try:
            Permission.check_permissions(
                request.user, (permission_document_restore,)
            )
        except PermissionDenied:
            AccessControlList.objects.check_access(
                permission_document_restore, request.user, source_document
            )

        instance.restore()
        messages.success(
            request, _('Document: %(document)s restored.') % {
                'document': instance
            }
        )

    def post(self, request, *args, **kwargs):
        document = get_object_or_404(DeletedDocument, pk=self.kwargs['pk'])
        self.object_action(request=request, instance=document)

        return HttpResponseRedirect(self.get_success_url())


class DocumentManyDeleteView(MultipleInstanceActionMixin, DeletedDocumentDeleteView):
    extra_context = {
        'title': _('Delete the selected documents?')
    }
    model = DeletedDocument


class DocumentManyRestoreView(MultipleInstanceActionMixin, DocumentRestoreView):
    extra_context = {
        'title': _('Restore the selected documents?')
    }
    model = DeletedDocument


class DocumentPageListView(ParentChildListView):
    object_permission = permission_document_view
    parent_queryset = Document.objects.all()

    def get_queryset(self):
        return self.get_object().pages.all()

    def get_context_data(self, **kwargs):
        context = super(DocumentPageListView, self).get_context_data(**kwargs)

        context.update(
            {
                'title': _('Pages for document: %s') % self.get_object(),
            }
        )

        return context


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


class EmptyTrashCanView(ConfirmView):
    extra_context = {
        'title': _('Empty trash?')
    }
    view_permission = permission_empty_trash
    action_cancel_redirect = post_action_redirect = reverse_lazy(
        'documents:document_list_deleted'
    )

    def post(self, request, *args, **kwargs):
        for deleted_document in DeletedDocument.objects.all():
            deleted_document.delete()

        messages.success(request, _('Trash emptied successfully'))

        return HttpResponseRedirect(self.get_success_url())


class RecentDocumentListView(DocumentListView):
    extra_context = {
        'hide_links': True,
        'title': _('Recent documents'),
    }

    def get_document_queryset(self):
        return RecentDocument.objects.get_for_user(self.request.user)


def document_properties(request, document_id):
    document = get_object_or_404(Document, pk=document_id)

    try:
        Permission.check_permissions(request.user, (permission_document_view,))
    except PermissionDenied:
        AccessControlList.objects.check_access(
            permission_document_view, request.user, document
        )

    document.add_as_recent_document_for_user(request.user)

    document_fields = [
        {'label': _('Date added'), 'field': lambda x: x.date_added.date()},
        {
            'label': _('Time added'),
            'field': lambda x: unicode(x.date_added.time()).split('.')[0]
        },
        {'label': _('UUID'), 'field': 'uuid'},
    ]
    if document.latest_version:
        document_fields.extend([
            {
                'label': _('File mimetype'),
                'field': lambda x: x.file_mimetype or _('None')
            },
            {
                'label': _('File encoding'),
                'field': lambda x: x.file_mime_encoding or _('None')
            },
            {
                'label': _('File size'),
                'field': lambda x: pretty_size(x.size) if x.size else '-'
            },
            {'label': _('Exists in storage'), 'field': 'exists'},
            {'label': _('File path in storage'), 'field': 'latest_version.file'},
            {'label': _('Checksum'), 'field': 'checksum'},
            {'label': _('Pages'), 'field': 'page_count'},
        ])

    document_properties_form = DocumentPropertiesForm(
        instance=document, extra_fields=document_fields
    )

    return render_to_response('appearance/generic_form.html', {
        'form': document_properties_form,
        'document': document,
        'object': document,
        'read_only': True,
        'title': _('Properties for document: %s') % document,
    }, context_instance=RequestContext(request))


def document_preview(request, document_id):
    document = get_object_or_404(Document, pk=document_id)

    try:
        Permission.check_permissions(request.user, (permission_document_view,))
    except PermissionDenied:
        AccessControlList.objects.check_access(
            permission_document_view, request.user, document
        )

    document.add_as_recent_document_for_user(request.user)

    preview_form = DocumentPreviewForm(document=document)

    return render_to_response('appearance/generic_form.html', {
        'document': document,
        'form': preview_form,
        'hide_labels': True,
        'object': document,
        'read_only': True,
        'title': _('Preview of document: %s') % document,
    }, context_instance=RequestContext(request))


def document_trash(request, document_id=None, document_id_list=None):
    post_action_redirect = None

    if document_id:
        documents = [get_object_or_404(Document, pk=document_id)]
        post_action_redirect = reverse('documents:document_list_recent')
    elif document_id_list:
        documents = [
            get_object_or_404(Document, pk=document_id) for document_id in document_id_list.split(',')
        ]
    else:
        messages.error(request, _('Must provide at least one document.'))
        return HttpResponseRedirect(
            request.META.get(
                'HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL)
            )
        )

    try:
        Permission.check_permissions(request.user, (permission_document_trash,))
    except PermissionDenied:
        documents = AccessControlList.objects.filter_by_access(
            permission_document_trash, request.user, documents
        )

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))))

    if request.method == 'POST':
        for document in documents:
            try:
                document.delete()
                messages.success(request, _('Document moved to trash successfully.'))
            except Exception as exception:
                messages.error(request, _('Document: %(document)s error moving to trash: %(error)s') % {
                    'document': document, 'error': exception
                })

        return HttpResponseRedirect(next)

    context = {
        'delete_view': True,
        'previous': previous,
        'next': next,
        'title': ungettext(
            'Move the selected document to the trash ?',
            'Move the selected documents to the trash ?',
            len(documents)
        )
    }

    if len(documents) == 1:
        context['object'] = documents[0]

    return render_to_response('appearance/generic_confirm.html', context,
                              context_instance=RequestContext(request))


def document_multiple_trash(request):
    return document_trash(
        request, document_id_list=request.GET.get('id_list', [])
    )


def document_edit(request, document_id):
    document = get_object_or_404(Document, pk=document_id)
    try:
        Permission.check_permissions(
            request.user, (permission_document_properties_edit,)
        )
    except PermissionDenied:
        AccessControlList.objects.check_access(
            permission_document_properties_edit, request.user, document
        )

    if request.method == 'POST':
        form = DocumentForm(request.POST, instance=document)
        if form.is_valid():
            document.label = form.cleaned_data['label']
            document.description = form.cleaned_data['description']
            document.language = form.cleaned_data['language']

            if 'document_type_available_filenames' in form.cleaned_data:
                if form.cleaned_data['document_type_available_filenames']:
                    document.label = form.cleaned_data['document_type_available_filenames'].filename

            document.save()
            event_document_properties_edit.commit(actor=request.user, target=document)
            document.add_as_recent_document_for_user(request.user)

            messages.success(request, _('Document "%s" edited successfully.') % document)

            return HttpResponseRedirect(document.get_absolute_url())
    else:
        form = DocumentForm(instance=document)

    return render_to_response('appearance/generic_form.html', {
        'form': form,
        'object': document,
        'title': _('Edit properties of document: %s') % document,
    }, context_instance=RequestContext(request))


def document_document_type_edit(request, document_id=None, document_id_list=None):
    post_action_redirect = None

    if document_id:
        documents = [get_object_or_404(Document, pk=document_id)]
        post_action_redirect = reverse('documents:document_list_recent')
    elif document_id_list:
        documents = [get_object_or_404(Document, pk=document_id) for document_id in document_id_list.split(',')]
    else:
        messages.error(request, _('Must provide at least one document.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL)))

    try:
        Permission.check_permissions(
            request.user, (permission_document_properties_edit,)
        )
    except PermissionDenied:
        documents = AccessControlList.objects.filter_by_access(
            permission_document_properties_edit, request.user, documents
        )

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))))

    if request.method == 'POST':
        form = DocumentTypeSelectForm(request.POST)
        if form.is_valid():

            for document in documents:
                document.set_document_type(form.cleaned_data['document_type'])
                event_document_type_change.commit(actor=request.user, target=document)
                document.add_as_recent_document_for_user(request.user)

            messages.success(request, _('Document type changed successfully.'))
            return HttpResponseRedirect(next)
    else:
        form = DocumentTypeSelectForm(initial={'document_type': documents[0].document_type})

    context = {
        'form': form,
        'submit_label': _('Submit'),
        'previous': previous,
        'next': next,
        'title': ungettext(
            'Change the type of the selected document.',
            'Change the type of the selected documents.',
            len(documents)
        )
    }

    if len(documents) == 1:
        context['object'] = documents[0]

    return render_to_response('appearance/generic_form.html', context,
                              context_instance=RequestContext(request))


def document_multiple_document_type_edit(request):
    return document_document_type_edit(
        request, document_id_list=request.GET.get('id_list', [])
    )


# TODO: Get rid of this view and convert widget to use API and base64 only images
def get_document_image(request, document_id, size=setting_preview_size.value):
    document = get_object_or_404(Document, pk=document_id)
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
    return HttpResponse(base64.b64decode(data[21:]), content_type='image')


def document_download(request, document_id=None, document_id_list=None, document_version_pk=None):
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))))

    if document_id:
        document_versions = [get_object_or_404(Document, pk=document_id).latest_version]
    elif document_id_list:
        document_versions = [get_object_or_404(Document, pk=document_id).latest_version for document_id in document_id_list.split(',')]
    elif document_version_pk:
        document_versions = [get_object_or_404(DocumentVersion, pk=document_version_pk)]

    try:
        Permission.check_permissions(request.user, (permission_document_download,))
    except PermissionDenied:
        document_versions = AccessControlList.objects.filter_by_access(permission_document_download, request.user, document_versions, related='document')

    subtemplates_list = []
    subtemplates_list.append(
        {
            'name': 'appearance/generic_list_subtemplate.html',
            'context': {
                'title': _('Documents to be downloaded'),
                'object_list': document_versions,
                'hide_link': True,
                'hide_object': True,
                'hide_links': True,
                'scrollable_content': True,
                'scrollable_content_height': '200px',
                'extra_columns': [
                    {'name': _('Document'), 'attribute': 'document'},
                    {'name': _('Date and time'), 'attribute': 'timestamp'},
                    {'name': _('MIME type'), 'attribute': 'mimetype'},
                    {'name': _('Encoding'), 'attribute': 'encoding'},
                ],
            }
        }
    )

    if request.method == 'POST':
        form = DocumentDownloadForm(request.POST, document_versions=document_versions)
        if form.is_valid():
            if form.cleaned_data['compressed'] or len(document_versions) > 1:
                try:
                    compressed_file = CompressedFile()
                    for document_version in document_versions:
                        descriptor = document_version.open()
                        compressed_file.add_file(descriptor, arcname=document_version.document.label)
                        descriptor.close()

                    compressed_file.close()

                    return serve_file(
                        request,
                        compressed_file.as_file(form.cleaned_data['zip_filename']),
                        save_as='"%s"' % form.cleaned_data['zip_filename'],
                        content_type='application/zip'
                    )
                    # TODO: DO a redirection afterwards
                except Exception as exception:
                    if settings.DEBUG:
                        raise
                    else:
                        messages.error(request, exception)
                        return HttpResponseRedirect(request.META['HTTP_REFERER'])
            else:
                try:
                    # Test permissions and trigger exception
                    fd = document_versions[0].open()
                    fd.close()
                    return serve_file(
                        request,
                        document_versions[0].file,
                        save_as='"%s"' % document_versions[0].document.label,
                        content_type=document_versions[0].mimetype if document_versions[0].mimetype else 'application/octet-stream'
                    )
                except Exception as exception:
                    if settings.DEBUG:
                        raise
                    else:
                        messages.error(request, exception)
                        return HttpResponseRedirect(request.META['HTTP_REFERER'])

    else:
        form = DocumentDownloadForm(document_versions=document_versions)

    context = {
        'form': form,
        'subtemplates_list': subtemplates_list,
        'title': _('Download documents'),
        'submit_label': _('Download'),
        'previous': previous,
        'cancel_label': _('Return'),
    }

    if len(document_versions) == 1:
        context['object'] = document_versions[0].document

    return render_to_response(
        'appearance/generic_form.html',
        context,
        context_instance=RequestContext(request)
    )


def document_multiple_download(request):
    return document_download(
        request, document_id_list=request.GET.get('id_list', [])
    )


def document_update_page_count(request, document_id=None, document_id_list=None):
    if document_id:
        documents = [get_object_or_404(Document.objects, pk=document_id)]
    elif document_id_list:
        documents = [get_object_or_404(Document, pk=document_id) for document_id in document_id_list.split(',')]
    else:
        messages.error(request, _('Must provide at least one document.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL)))

    try:
        Permission.check_permissions(request.user, (permission_document_tools,))
    except PermissionDenied:
        documents = AccessControlList.objects.filter_by_access(permission_document_tools, request.user, documents)

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))))

    if request.method == 'POST':
        for document in documents:
            task_update_page_count.apply_async(kwargs={'version_id': document.latest_version.pk})

        messages.success(
            request,
            ungettext(
                _('Document queued for page count reset.'),
                _('Documents queued for page count reset.'),
                len(documents)
            )
        )
        return HttpResponseRedirect(previous)

    context = {
        'previous': previous,
        'title': ungettext(
            'Reset the page count of the selected document?',
            'Reset the page count of the selected documents?',
            len(documents)
        )
    }

    if len(documents) == 1:
        context['object'] = documents[0]

    return render_to_response('appearance/generic_confirm.html', context,
                              context_instance=RequestContext(request))


def document_multiple_update_page_count(request):
    return document_update_page_count(request, document_id_list=request.GET.get('id_list', []))


def document_clear_transformations(request, document_id=None, document_id_list=None):
    if document_id:
        documents = [get_object_or_404(Document.objects, pk=document_id)]
        post_redirect = documents[0].get_absolute_url()
    elif document_id_list:
        documents = [get_object_or_404(Document, pk=document_id) for document_id in document_id_list.split(',')]
        post_redirect = None
    else:
        messages.error(request, _('Must provide at least one document.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL)))

    try:
        Permission.check_permissions(request.user, (permission_transformation_delete,))
    except PermissionDenied:
        documents = AccessControlList.objects.filter_by_access(permission_transformation_delete, request.user, documents)

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', post_redirect or reverse('documents:document_list'))))
    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', post_redirect or reverse('documents:document_list'))))

    if request.method == 'POST':
        for document in documents:
            try:
                for page in document.pages.all():
                    Transformation.objects.get_for_model(page).delete()
            except Exception as exception:
                messages.error(request, _('Error deleting the page transformations for document: %(document)s; %(error)s.') % {
                    'document': document, 'error': exception})
            else:
                messages.success(request, _('All the page transformations for document: %s, have been deleted successfully.') % document)

        return HttpResponseRedirect(next)

    context = {
        'delete_view': True,
        'next': next,
        'previous': previous,
        'title': ungettext(
            'Clear all the page transformations for the selected document?',
            'Clear all the page transformations for the selected documents?',
            len(documents)
        )
    }

    if len(documents) == 1:
        context['object'] = documents[0]

    return render_to_response('appearance/generic_confirm.html', context,
                              context_instance=RequestContext(request))


def document_multiple_clear_transformations(request):
    return document_clear_transformations(request, document_id_list=request.GET.get('id_list', []))


def document_page_view(request, document_page_id):
    document_page = get_object_or_404(DocumentPage, pk=document_page_id)

    try:
        Permission.check_permissions(request.user, (permission_document_view,))
    except PermissionDenied:
        AccessControlList.objects.check_access(permission_document_view, request.user, document_page.document)

    zoom = int(request.GET.get('zoom', DEFAULT_ZOOM_LEVEL))
    rotation = int(request.GET.get('rotation', DEFAULT_ROTATION))
    document_page_form = DocumentPageForm(instance=document_page, zoom=zoom, rotation=rotation)

    base_title = _('Details for: %s') % document_page

    if zoom != DEFAULT_ZOOM_LEVEL:
        zoom_text = '(%d%%)' % zoom
    else:
        zoom_text = ''

    return render_to_response('appearance/generic_form.html', {
        'access_object': document_page.document,
        'form': document_page_form,
        'navigation_object_list': ('page',),
        'page': document_page,
        'rotation': rotation,
        'title': ' '.join([base_title, zoom_text]),
        'read_only': True,
        'zoom': zoom,
    }, context_instance=RequestContext(request))


def document_page_view_reset(request, document_page_id):
    return HttpResponseRedirect(reverse('documents:document_page_view', args=[document_page_id]))


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
        return HttpResponseRedirect('{0}?{1}'.format(reverse(view, args=[document_page.pk]), request.GET.urlencode()))


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
        return HttpResponseRedirect('{0}?{1}'.format(reverse(view, args=[document_page.pk]), request.GET.urlencode()))


def document_page_navigation_first(request, document_page_id):
    document_page = get_object_or_404(DocumentPage, pk=document_page_id)
    document_page = get_object_or_404(document_page.siblings, page_number=1)

    try:
        Permission.check_permissions(request.user, (permission_document_view,))
    except PermissionDenied:
        AccessControlList.objects.check_access(permission_document_view, request.user, document_page.document)

    view = resolve(urlparse.urlparse(request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))).path).view_name

    return HttpResponseRedirect('{0}?{1}'.format(reverse(view, args=[document_page.pk]), request.GET.urlencode()))


def document_page_navigation_last(request, document_page_id):
    document_page = get_object_or_404(DocumentPage, pk=document_page_id)
    document_page = get_object_or_404(document_page.siblings, page_number=document_page.siblings.count())

    try:
        Permission.check_permissions(request.user, (permission_document_view,))
    except PermissionDenied:
        AccessControlList.objects.check_access(permission_document_view, request.user, document_page.document)

    view = resolve(urlparse.urlparse(request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))).path).view_name

    return HttpResponseRedirect('{0}?{1}'.format(reverse(view, args=[document_page.pk]), request.GET.urlencode()))


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
            if form.cleaned_data['page_range']:
                page_range = form.cleaned_data['page_range']

                if page_range:
                    page_range = parse_range(page_range)

                    pages = document.pages.filter(page_number__in=page_range)
                else:
                    pages = document.pages.all()

                return render_to_response('documents/document_print.html', {
                    'appearance_type': 'plain',
                    'object': document,
                    'page_range': page_range,
                    'pages': pages,
                }, context_instance=RequestContext(request))
    else:
        form = PrintForm()

    return render_to_response('appearance/generic_form.html', {
        'form': form,
        'object': document,
        'title': _('Print: %s') % document,
        'next': next,
    }, context_instance=RequestContext(request))


class DocumentTypeListView(SingleObjectListView):
    model = DocumentType
    view_permission = permission_document_type_view

    def get_extra_context(self):
        return {
            'extra_columns': [
                {'name': _('Documents'), 'attribute': encapsulate(lambda document_type: document_type.documents.count())}
            ],
            'hide_link': True,
            'title': _('Document types'),
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
    fields = ('label', 'trash_time_period', 'trash_time_unit', 'delete_time_period', 'delete_time_unit')
    model = DocumentType
    post_action_redirect = reverse_lazy('documents:document_type_list')
    view_permission = permission_document_type_edit

    def get_extra_context(self):
        return {
            'object': self.get_object(),
            'title': _('Edit document type: %s') % self.get_object(),
        }


class DocumentTypeCreateView(SingleObjectCreateView):
    fields = ('label', 'trash_time_period', 'trash_time_unit', 'delete_time_period', 'delete_time_unit')
    model = DocumentType
    post_action_redirect = reverse_lazy('documents:document_type_list')
    view_permission = permission_document_type_create

    def get_extra_context(self):
        return {
            'title': _('Create document type'),
        }


class DocumentTypeFilenameListView(SingleObjectListView):
    model = DocumentType
    view_permission = permission_document_type_view

    def get_document_type(self):
        return get_object_or_404(DocumentType, pk=self.kwargs['pk'])

    def get_extra_context(self):
        return {
            'document_type': self.get_document_type(),
            'extra_columns': (
                {
                    'name': _('Enabled'),
                    'attribute': encapsulate(lambda filename: two_state_template(filename.enabled)),
                },
            ),
            'hide_link': True,
            'navigation_object_list': ('document_type',),
            'title': _('Filenames for document type: %s') % self.get_document_type(),
        }

    def get_queryset(self):
        return self.get_document_type().filenames.all()


class DocumentTypeFilenameEditView(SingleObjectEditView):
    fields = ('enabled', 'filename',)
    model = DocumentTypeFilename
    view_permission = permission_document_type_edit

    def get_post_action_redirect(self):
        return reverse(
            'documents:document_type_filename_list',
            args=(self.get_object().document_type.pk,)
        )

    def get_extra_context(self):
        document_type_filename = self.get_object()

        return {
            'document_type': document_type_filename.document_type,
            'filename': document_type_filename,
            'navigation_object_list': ('document_type', 'filename',),
            'title': _('Edit filename "%(filename)s" from document type "%(document_type)s"') % {
                'document_type': document_type_filename.document_type, 'filename': document_type_filename
            },
        }


def document_type_filename_delete(request, document_type_filename_id):
    Permission.check_permissions(request.user, (permission_document_type_edit,))
    document_type_filename = get_object_or_404(DocumentTypeFilename, pk=document_type_filename_id)

    post_action_redirect = reverse('documents:document_type_filename_list', args=[document_type_filename.document_type_id])

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))))

    if request.method == 'POST':
        try:
            document_type_filename.delete()
            messages.success(request, _('Document type filename: %s deleted successfully.') % document_type_filename)
        except Exception as exception:
            messages.error(request, _('Document type filename: %(document_type_filename)s delete error: %(error)s') % {
                'document_type_filename': document_type_filename, 'error': exception})

        return HttpResponseRedirect(next)

    context = {
        'delete_view': True,
        'document_type': document_type_filename.document_type,
        'filename': document_type_filename,
        'previous': previous,
        'navigation_object_list': ('document_type', 'filename',),
        'next': next,
        'title': _('Delete the filename: %(filename)s, from document type "%(document_type)s"?') % {
            'document_type': document_type_filename.document_type, 'filename': document_type_filename
        },
    }

    return render_to_response('appearance/generic_confirm.html', context,
                              context_instance=RequestContext(request))


def document_type_filename_create(request, document_type_id):
    Permission.check_permissions(request.user, (permission_document_type_edit,))

    document_type = get_object_or_404(DocumentType, pk=document_type_id)

    if request.method == 'POST':
        form = DocumentTypeFilenameForm_create(request.POST)
        if form.is_valid():
            try:
                document_type_filename = DocumentTypeFilename(
                    document_type=document_type,
                    filename=form.cleaned_data['filename'],
                    enabled=True
                )
                document_type_filename.save()
                messages.success(request, _('Document type filename created successfully'))
                return HttpResponseRedirect(reverse('documents:document_type_filename_list', args=[document_type_id]))
            except Exception as exception:
                messages.error(request, _('Error creating document type filename; %(error)s') % {
                    'error': exception})
    else:
        form = DocumentTypeFilenameForm_create()

    return render_to_response('appearance/generic_form.html', {
        'document_type': document_type,
        'form': form,
        'navigation_object_list': ('document_type',),
        'title': _('Create filename for document type: %s') % document_type,
    }, context_instance=RequestContext(request))


def document_clear_image_cache(request):
    Permission.check_permissions(request.user, (permission_document_tools,))

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))))

    if request.method == 'POST':
        task_clear_image_cache.apply_async()
        messages.success(request, _('Document cache clearing queued successfully.'))

        return HttpResponseRedirect(previous)

    return render_to_response('appearance/generic_confirm.html', {
        'previous': previous,
        'title': _('Clear the document cache?'),
    }, context_instance=RequestContext(request))


class DocumentVersionListView(SingleObjectListView):
    def dispatch(self, request, *args, **kwargs):
        try:
            Permission.check_permissions(request.user, (permission_document_view,))
        except PermissionDenied:
            AccessControlList.objects.check_access(permission_document_view, request.user, self.get_document())

        self.get_document().add_as_recent_document_for_user(request.user)

        return super(DocumentVersionListView, self).dispatch(request, *args, **kwargs)

    def get_document(self):
        return get_object_or_404(Document, pk=self.kwargs['pk'])

    def get_extra_context(self):
        return {
            'extra_columns': (
                {'name': _('Time and date'), 'attribute': 'timestamp'},
                {'name': _('MIME type'), 'attribute': 'mimetype'},
                {'name': _('Encoding'), 'attribute': 'encoding'},
                {'name': _('Comment'), 'attribute': 'comment'},
            ), 'hide_object': True, 'object': self.get_document(),
            'title': _('Versions of document: %s') % self.get_document(),
        }

    def get_queryset(self):
        return self.get_document().versions.order_by('-timestamp')


def document_version_revert(request, document_version_pk):
    document_version = get_object_or_404(DocumentVersion, pk=document_version_pk)

    try:
        Permission.check_permissions(request.user, (permission_document_version_revert,))
    except PermissionDenied:
        AccessControlList.objects.check_access(permission_document_version_revert, request.user, document_version.document)

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))))

    if request.method == 'POST':
        try:
            document_version.revert(user=request.user)
            messages.success(request, _('Document version reverted successfully'))
        except Exception as exception:
            messages.error(request, _('Error reverting document version; %s') % exception)

        return HttpResponseRedirect(previous)

    return render_to_response('appearance/generic_confirm.html', {
        'previous': previous,
        'object': document_version.document,
        'title': _('Revert to this version?'),
        'message': _('All later version after this one will be deleted too.'),
    }, context_instance=RequestContext(request))
