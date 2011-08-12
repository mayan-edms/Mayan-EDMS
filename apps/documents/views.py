import urlparse
import copy

from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.views.generic.list_detail import object_list
from django.core.urlresolvers import reverse
from django.utils.http import urlencode

import sendfile
from common.utils import pretty_size, parse_range, urlquote, \
    return_diff, encapsulate
from common.widgets import two_state_template
from common.literals import PAGE_SIZE_DIMENSIONS, \
    PAGE_ORIENTATION_PORTRAIT, PAGE_ORIENTATION_LANDSCAPE
from common.conf.settings import DEFAULT_PAPER_SIZE
from converter.literals import DEFAULT_ZOOM_LEVEL, DEFAULT_ROTATION, \
    DEFAULT_PAGE_NUMBER
from filetransfers.api import serve_file
from grouping.utils import get_document_group_subtemplate
from metadata.forms import MetadataFormSet, MetadataSelectionForm
from navigation.utils import resolve_to_name
from permissions.api import check_permissions
from document_indexing.api import update_indexes, delete_indexes
from history.api import create_history

from documents.conf.settings import PREVIEW_SIZE
from documents.conf.settings import STORAGE_BACKEND
from documents.conf.settings import ZOOM_PERCENT_STEP
from documents.conf.settings import ZOOM_MAX_LEVEL
from documents.conf.settings import ZOOM_MIN_LEVEL
from documents.conf.settings import ROTATION_STEP
from documents.conf.settings import PRINT_SIZE
from documents.conf.settings import RECENT_COUNT

from documents.literals import PERMISSION_DOCUMENT_CREATE, \
    PERMISSION_DOCUMENT_PROPERTIES_EDIT, \
    PERMISSION_DOCUMENT_VIEW, \
    PERMISSION_DOCUMENT_DELETE, PERMISSION_DOCUMENT_DOWNLOAD, \
    PERMISSION_DOCUMENT_TRANSFORM, \
    PERMISSION_DOCUMENT_EDIT
from documents.literals import HISTORY_DOCUMENT_CREATED, \
    HISTORY_DOCUMENT_EDITED, HISTORY_DOCUMENT_DELETED

from documents.forms import DocumentTypeSelectForm, \
        DocumentForm_edit, DocumentPropertiesForm, \
        DocumentPreviewForm, \
        DocumentPageForm, DocumentPageTransformationForm, \
        DocumentContentForm, DocumentPageForm_edit, \
        DocumentPageForm_text, PrintForm, DocumentTypeForm, \
        DocumentTypeFilenameForm, DocumentTypeFilenameForm_create
from documents.wizards import DocumentCreateWizard
from documents.models import Document, DocumentType, DocumentPage, \
    DocumentPageTransformation, RecentDocument, DocumentTypeFilename

# Document type permissions
from documents.literals import PERMISSION_DOCUMENT_TYPE_EDIT, \
    PERMISSION_DOCUMENT_TYPE_DELETE, PERMISSION_DOCUMENT_TYPE_CREATE


def document_list(request, object_list=None, title=None, extra_context=None):
    check_permissions(request.user, [PERMISSION_DOCUMENT_VIEW])

    context = {
        'object_list': object_list if not (object_list is None) else Document.objects.only('file_filename', 'file_extension').all(),
        'title': title if title else _(u'documents'),
        'multi_select_as_buttons': True,
        'hide_links': True,
    }
    if extra_context:
        context.update(extra_context)

    return render_to_response('generic_list.html', context,
        context_instance=RequestContext(request))


def document_create(request):
    check_permissions(request.user, [PERMISSION_DOCUMENT_CREATE])

    wizard = DocumentCreateWizard(form_list=[DocumentTypeSelectForm, MetadataSelectionForm, MetadataFormSet])

    return wizard(request)


def document_create_siblings(request, document_id):
    check_permissions(request.user, [PERMISSION_DOCUMENT_CREATE])

    document = get_object_or_404(Document, pk=document_id)
    query_dict = {}
    for pk, metadata in enumerate(document.documentmetadata_set.all()):
        query_dict['metadata%s_id' % pk] = metadata.metadata_type_id
        query_dict['metadata%s_value' % pk] = metadata.value

    if document.document_type_id:
        query_dict['document_type_id'] = document.document_type_id

    url = reverse('upload_interactive')
    return HttpResponseRedirect('%s?%s' % (url, urlencode(query_dict)))


def document_view(request, document_id, advanced=False):
    check_permissions(request.user, [PERMISSION_DOCUMENT_VIEW])
    #document = get_object_or_404(Document.objects.select_related(), pk=document_id)
    # Triggers a 404 error on documents uploaded via local upload
    # TODO: investigate
    document = get_object_or_404(Document, pk=document_id)

    RecentDocument.objects.add_document_for_user(request.user, document)

    subtemplates_list = []

    if advanced:
        document_properties_form = DocumentPropertiesForm(instance=document, extra_fields=[
            {'label': _(u'Filename'), 'field': 'file_filename'},
            {'label': _(u'File extension'), 'field': 'file_extension'},
            {'label': _(u'File mimetype'), 'field': 'file_mimetype'},
            {'label': _(u'File mime encoding'), 'field': 'file_mime_encoding'},
            {'label': _(u'File size'), 'field':lambda x: pretty_size(x.file.storage.size(x.file.path)) if x.exists() else '-'},
            {'label': _(u'Exists in storage'), 'field': 'exists'},
            {'label': _(u'File path in storage'), 'field': 'file'},
            {'label': _(u'Date added'), 'field':lambda x: x.date_added.date()},
            {'label': _(u'Time added'), 'field':lambda x: unicode(x.date_added.time()).split('.')[0]},
            {'label': _(u'Checksum'), 'field': 'checksum'},
            {'label': _(u'UUID'), 'field': 'uuid'},
            {'label': _(u'Pages'), 'field': lambda x: x.documentpage_set.count()},
        ])

        subtemplates_list.append(
            {
                'name': 'generic_form_subtemplate.html',
                'context': {
                    'form': document_properties_form,
                    'object': document,
                    'title': _(u'document properties for: %s') % document,
                }
            },
        )
    else:
        preview_form = DocumentPreviewForm(document=document)
        subtemplates_list.append(
            {
                'name': 'generic_form_subtemplate.html',
                'context': {
                    'form': preview_form,
                    'object': document,
                }
            },
        )

        content_form = DocumentContentForm(document=document)

        subtemplates_list.append(
            {
                'name': 'generic_form_subtemplate.html',
                'context': {
                    'title': _(u'document data'),
                    'form': content_form,
                    'object': document,
                },
            }
        )

        document_group_subtemplate = get_document_group_subtemplate(request, document)

        if document_group_subtemplate:
            subtemplates_list.append(document_group_subtemplate)

    return render_to_response('generic_detail.html', {
        'object': document,
        'document': document,
        'subtemplates_list': subtemplates_list,
        'disable_auto_focus': True,
    }, context_instance=RequestContext(request))


def document_delete(request, document_id=None, document_id_list=None):
    check_permissions(request.user, [PERMISSION_DOCUMENT_DELETE])
    post_action_redirect = None

    if document_id:
        documents = [get_object_or_404(Document, pk=document_id)]
        post_action_redirect = reverse('document_list')
    elif document_id_list:
        documents = [get_object_or_404(Document, pk=document_id) for document_id in document_id_list.split(',')]
    else:
        messages.error(request, _(u'Must provide at least one document.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', '/')))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', '/')))

    if request.method == 'POST':
        for document in documents:
            try:
                warnings = delete_indexes(document)
                if request.user.is_staff or request.user.is_superuser:
                    for warning in warnings:
                        messages.warning(request, warning)

                document.delete()
                #create_history(HISTORY_DOCUMENT_DELETED, data={'user': request.user, 'document': document})
                messages.success(request, _(u'Document: %s deleted successfully.') % document)
            except Exception, e:
                messages.error(request, _(u'Document: %(document)s delete error: %(error)s') % {
                    'document': document, 'error': e
                })

        return HttpResponseRedirect(next)

    context = {
        'object_name': _(u'document'),
        'delete_view': True,
        'previous': previous,
        'next': next,
        'form_icon': u'page_delete.png',
    }
    if len(documents) == 1:
        context['object'] = documents[0]
        context['title'] = _(u'Are you sure you wish to delete the document: %s?') % ', '.join([unicode(d) for d in documents])
    elif len(documents) > 1:
        context['title'] = _(u'Are you sure you wish to delete the documents: %s?') % ', '.join([unicode(d) for d in documents])

    return render_to_response('generic_confirm.html', context,
        context_instance=RequestContext(request))


def document_multiple_delete(request):
    return document_delete(
        request, document_id_list=request.GET.get('id_list', [])
    )


def document_edit(request, document_id):
    check_permissions(request.user, [PERMISSION_DOCUMENT_PROPERTIES_EDIT])

    document = get_object_or_404(Document, pk=document_id)

    if request.method == 'POST':
        old_document = copy.copy(document)
        form = DocumentForm_edit(request.POST, instance=document)
        if form.is_valid():
            warnings = delete_indexes(document)
            if request.user.is_staff or request.user.is_superuser:
                for warning in warnings:
                    messages.warning(request, warning)

            document.file_filename = form.cleaned_data['new_filename']
            document.description = form.cleaned_data['description']

            if 'document_type_available_filenames' in form.cleaned_data:
                if form.cleaned_data['document_type_available_filenames']:
                    document.file_filename = form.cleaned_data['document_type_available_filenames'].filename

            document.save()
            create_history(HISTORY_DOCUMENT_EDITED, document, {'user': request.user, 'diff': return_diff(old_document, document, ['file_filename', 'description'])})
            RecentDocument.objects.add_document_for_user(request.user, document)

            messages.success(request, _(u'Document "%s" edited successfully.') % document)

            warnings = update_indexes(document)
            if request.user.is_staff or request.user.is_superuser:
                for warning in warnings:
                    messages.warning(request, warning)

            return HttpResponseRedirect(document.get_absolute_url())
    else:
        form = DocumentForm_edit(instance=document, initial={
            'new_filename': document.file_filename})

    return render_to_response('generic_form.html', {
        'form': form,
        'object': document,
    }, context_instance=RequestContext(request))


def get_document_image(request, document_id, size=PREVIEW_SIZE):
    check_permissions(request.user, [PERMISSION_DOCUMENT_VIEW])

    document = get_object_or_404(Document, pk=document_id)

    page = int(request.GET.get('page', DEFAULT_PAGE_NUMBER))

    zoom = int(request.GET.get('zoom', DEFAULT_ZOOM_LEVEL))

    if zoom < ZOOM_MIN_LEVEL:
        zoom = ZOOM_MIN_LEVEL

    if zoom > ZOOM_MAX_LEVEL:
        zoom = ZOOM_MAX_LEVEL

    rotation = int(request.GET.get('rotation', DEFAULT_ROTATION)) % 360

    return sendfile.sendfile(request, document.get_image(size=size, page=page, zoom=zoom, rotation=rotation))


def document_download(request, document_id):
    check_permissions(request.user, [PERMISSION_DOCUMENT_DOWNLOAD])

    document = get_object_or_404(Document, pk=document_id)
    try:
        #Test permissions and trigger exception
        document.open()
        return serve_file(
            request,
            document.file,
            save_as=u'"%s"' % document.get_fullname(),
            content_type=document.file_mimetype if document.file_mimetype else 'application/octet-stream'
        )
    except Exception, e:
        messages.error(request, e)
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


def document_page_transformation_list(request, document_page_id):
    check_permissions(request.user, [PERMISSION_DOCUMENT_TRANSFORM])

    document_page = get_object_or_404(DocumentPage, pk=document_page_id)

    return object_list(
        request,
        queryset=document_page.documentpagetransformation_set.all(),
        template_name='generic_list.html',
        extra_context={
            'page': document_page,
            'navigation_object_name': 'page',
            'title': _(u'transformations for: %s') % document_page,
            'web_theme_hide_menus': True,
            'list_object_variable_name': 'transformation',
            'extra_columns': [
                {'name': _(u'order'), 'attribute': 'order'},
                {'name': _(u'transformation'), 'attribute': encapsulate(lambda x: x.get_transformation_display())},
                {'name': _(u'arguments'), 'attribute': 'arguments'}
                ],
            'hide_link': True,
            'hide_object': True,
        },
    )


def document_page_transformation_create(request, document_page_id):
    check_permissions(request.user, [PERMISSION_DOCUMENT_TRANSFORM])

    document_page = get_object_or_404(DocumentPage, pk=document_page_id)

    if request.method == 'POST':
        form = DocumentPageTransformationForm(request.POST, initial={'document_page': document_page})
        if form.is_valid():
            document_page.document.invalidate_cached_image(document_page.page_number)
            form.save()
            messages.success(request, _(u'Document page transformation created successfully.'))
            return HttpResponseRedirect(reverse('document_page_transformation_list', args=[document_page_id]))
    else:
        form = DocumentPageTransformationForm(initial={'document_page': document_page})

    return render_to_response('generic_form.html', {
        'form': form,
        'page': document_page,
        'navigation_object_name': 'page',
        'title': _(u'Create new transformation for page: %(page)s of document: %(document)s') % {
            'page': document_page.page_number, 'document': document_page.document},
        'web_theme_hide_menus': True,
    }, context_instance=RequestContext(request))


def document_page_transformation_edit(request, document_page_transformation_id):
    check_permissions(request.user, [PERMISSION_DOCUMENT_TRANSFORM])

    document_page_transformation = get_object_or_404(DocumentPageTransformation, pk=document_page_transformation_id)

    if request.method == 'POST':
        form = DocumentPageTransformationForm(request.POST, instance=document_page_transformation)
        if form.is_valid():
            document_page_transformation.document_page.document.invalidate_cached_image(document_page_transformation.document_page.page_number)
            form.save()
            messages.success(request, _(u'Document page transformation edited successfully.'))
            return HttpResponseRedirect(reverse('document_page_transformation_list', args=[document_page_transformation.document_page_id]))
    else:
        form = DocumentPageTransformationForm(instance=document_page_transformation)

    return render_to_response('generic_form.html', {
        'form': form,
        'transformation': document_page_transformation,
        'page': document_page_transformation.document_page,
        'navigation_object_list': [
            {'object': 'page'},
            {'object': 'transformation', 'name': _(u'transformation')}
        ],
        'title': _(u'Edit transformation "%(transformation)s" for: %(document_page)s') % {
            'transformation': document_page_transformation.get_transformation_display(),
            'document_page': document_page_transformation.document_page},
        'web_theme_hide_menus': True,
    }, context_instance=RequestContext(request))


def document_page_transformation_delete(request, document_page_transformation_id):
    check_permissions(request.user, [PERMISSION_DOCUMENT_TRANSFORM])

    document_page_transformation = get_object_or_404(DocumentPageTransformation, pk=document_page_transformation_id)

    redirect_view = reverse('document_page_transformation_list', args=[document_page_transformation.document_page_id])
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', redirect_view)))

    if request.method == 'POST':
        document_page_transformation.document_page.document.invalidate_cached_image(document_page_transformation.document_page.page_number)
        document_page_transformation.delete()
        messages.success(request, _(u'Document page transformation deleted successfully.'))
        return HttpResponseRedirect(redirect_view)

    return render_to_response('generic_confirm.html', {
        'delete_view': True,
        'page': document_page_transformation.document_page,
        'transformation': document_page_transformation,
        'navigation_object_list': [
            {'object': 'page'},
            {'object': 'transformation', 'name': _(u'transformation')}
        ],
        'title': _(u'Are you sure you wish to delete transformation "%(transformation)s" for: %(document_page)s') % {
            'transformation': document_page_transformation.get_transformation_display(),
            'document_page': document_page_transformation.document_page},
        'web_theme_hide_menus': True,
        'previous': previous,
        'form_icon': u'pencil_delete.png',
    }, context_instance=RequestContext(request))


def document_find_duplicates(request, document_id):
    check_permissions(request.user, [PERMISSION_DOCUMENT_VIEW])

    document = get_object_or_404(Document, pk=document_id)
    extra_context = {
        'title': _(u'duplicates of: %s') % document,
        'object': document,
    }
    return _find_duplicate_list(request, [document], include_source=True, confirmation=False, extra_context=extra_context)


def _find_duplicate_list(request, source_document_list=Document.objects.all(), include_source=False, confirmation=True, extra_context=None):
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', None)))

    if confirmation and request.method != 'POST':
        return render_to_response('generic_confirm.html', {
            'previous': previous,
            'title': _(u'Are you sure you wish to find all duplicates?'),
            'message': _(u'On large databases this operation may take some time to execute.'),
            'form_icon': u'page_refresh.png',
        }, context_instance=RequestContext(request))
    else:
        duplicated = []
        for document in source_document_list:
            if document.pk not in duplicated:
                results = Document.objects.filter(checksum=document.checksum).exclude(id__in=duplicated).exclude(pk=document.pk).values_list('pk', flat=True)
                duplicated.extend(results)

                if include_source and results:
                    duplicated.append(document.pk)

        context = {
            'object_list': Document.objects.filter(pk__in=duplicated),
            'title': _(u'duplicated documents'),
            'hide_links': True,
            'multi_select_as_buttons': True,
        }

        if extra_context:
            context.update(extra_context)

        return render_to_response('generic_list.html', context,
            context_instance=RequestContext(request))


def document_find_all_duplicates(request):
    check_permissions(request.user, [PERMISSION_DOCUMENT_VIEW])

    return _find_duplicate_list(request, include_source=True)


def document_clear_transformations(request, document_id=None, document_id_list=None):
    check_permissions(request.user, [PERMISSION_DOCUMENT_TRANSFORM])

    if document_id:
        documents = [get_object_or_404(Document.objects, pk=document_id)]
        post_redirect = reverse('document_view_simple', args=[documents[0].pk])
    elif document_id_list:
        documents = [get_object_or_404(Document, pk=document_id) for document_id in document_id_list.split(',')]
        post_redirect = None
    else:
        messages.error(request, _(u'Must provide at least one document.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', u'/'))

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', post_redirect or reverse('document_list'))))
    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', post_redirect or reverse('document_list'))))

    if request.method == 'POST':
        for document in documents:
            try:
                for document_page in document.documentpage_set.all():
                    document_page.document.invalidate_cached_image(document_page.page_number)
                    for transformation in document_page.documentpagetransformation_set.all():
                        transformation.delete()
                messages.success(request, _(u'All the page transformations for document: %s, have been deleted successfully.') % document)
            except Exception, e:
                messages.error(request, _(u'Error deleting the page transformations for document: %(document)s; %(error)s.') % {
                    'document': document, 'error': e})

        return HttpResponseRedirect(next)

    context = {
        'object_name': _(u'document transformation'),
        'delete_view': True,
        'previous': previous,
        'next': next,
        'form_icon': u'page_paintbrush.png',
    }

    if len(documents) == 1:
        context['object'] = documents[0]
        context['title'] = _(u'Are you sure you wish to clear all the page transformations for document: %s?') % ', '.join([unicode(d) for d in documents])
    elif len(documents) > 1:
        context['title'] = _(u'Are you sure you wish to clear all the page transformations for documents: %s?') % ', '.join([unicode(d) for d in documents])

    return render_to_response('generic_confirm.html', context,
        context_instance=RequestContext(request))


def document_multiple_clear_transformations(request):
    return document_clear_transformations(request, document_id_list=request.GET.get('id_list', []))


def document_missing_list(request):
    check_permissions(request.user, [PERMISSION_DOCUMENT_VIEW])

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', None)))

    if request.method != 'POST':
        return render_to_response('generic_confirm.html', {
            'previous': previous,
            'message': _(u'On large databases this operation may take some time to execute.'),
        }, context_instance=RequestContext(request))
    else:
        missing_id_list = []
        for document in Document.objects.only('id',):
            if not STORAGE_BACKEND().exists(document.file):
                missing_id_list.append(document.pk)

        return render_to_response('generic_list.html', {
            'object_list': Document.objects.in_bulk(missing_id_list).values(),
            'title': _(u'missing documents'),
        }, context_instance=RequestContext(request))


def document_page_view(request, document_page_id):
    check_permissions(request.user, [PERMISSION_DOCUMENT_VIEW])

    document_page = get_object_or_404(DocumentPage, pk=document_page_id)

    zoom = int(request.GET.get('zoom', DEFAULT_ZOOM_LEVEL))
    rotation = int(request.GET.get('rotation', DEFAULT_ROTATION))
    document_page_form = DocumentPageForm(instance=document_page, zoom=zoom, rotation=rotation)

    base_title = _(u'details for: %s') % document_page

    if zoom != DEFAULT_ZOOM_LEVEL:
        zoom_text = u'(%d%%)' % zoom
    else:
        zoom_text = u''

    if rotation != 0 and rotation != 360:
        rotation_text = u'(%d&deg;)' % rotation
    else:
        rotation_text = u''

    return render_to_response('generic_detail.html', {
        'page': document_page,
        'navigation_object_name': 'page',
        'web_theme_hide_menus': True,
        'form': document_page_form,
        'title': u' '.join([base_title, zoom_text, rotation_text]),
        'zoom': zoom,
        'rotation': rotation,
    }, context_instance=RequestContext(request))


def document_page_view_reset(request, document_page_id):
    return HttpResponseRedirect(reverse('document_page_view', args=[document_page_id]))


def document_page_text(request, document_page_id):
    check_permissions(request.user, [PERMISSION_DOCUMENT_VIEW])

    document_page = get_object_or_404(DocumentPage, pk=document_page_id)
    document_page_form = DocumentPageForm_text(instance=document_page)

    return render_to_response('generic_detail.html', {
        'page': document_page,
        'navigation_object_name': 'page',
        'web_theme_hide_menus': True,
        'form': document_page_form,
        'title': _(u'details for: %s') % document_page,
    }, context_instance=RequestContext(request))


def document_page_edit(request, document_page_id):
    check_permissions(request.user, [PERMISSION_DOCUMENT_EDIT])

    document_page = get_object_or_404(DocumentPage, pk=document_page_id)

    if request.method == 'POST':
        form = DocumentPageForm_edit(request.POST, instance=document_page)
        if form.is_valid():
            document_page.page_label = form.cleaned_data['page_label']
            document_page.content = form.cleaned_data['content']
            document_page.save()
            messages.success(request, _(u'Document page edited successfully.'))
            return HttpResponseRedirect(document_page.get_absolute_url())
    else:
        form = DocumentPageForm_edit(instance=document_page)

    return render_to_response('generic_form.html', {
        'form': form,
        'page': document_page,
        'navigation_object_name': 'page',
        'title': _(u'edit: %s') % document_page,
        'web_theme_hide_menus': True,
    }, context_instance=RequestContext(request))


def document_page_navigation_next(request, document_page_id):
    check_permissions(request.user, [PERMISSION_DOCUMENT_VIEW])
    view = resolve_to_name(urlparse.urlparse(request.META.get('HTTP_REFERER', u'/')).path)

    document_page = get_object_or_404(DocumentPage, pk=document_page_id)
    if document_page.page_number >= document_page.document.documentpage_set.count():
        messages.warning(request, _(u'There are no more pages in this document'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', u'/'))
    else:
        document_page = get_object_or_404(DocumentPage, document=document_page.document, page_number=document_page.page_number + 1)
        return HttpResponseRedirect(reverse(view, args=[document_page.pk]))


def document_page_navigation_previous(request, document_page_id):
    check_permissions(request.user, [PERMISSION_DOCUMENT_VIEW])
    view = resolve_to_name(urlparse.urlparse(request.META.get('HTTP_REFERER', u'/')).path)

    document_page = get_object_or_404(DocumentPage, pk=document_page_id)
    if document_page.page_number <= 1:
        messages.warning(request, _(u'You are already at the first page of this document'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', u'/'))
    else:
        document_page = get_object_or_404(DocumentPage, document=document_page.document, page_number=document_page.page_number - 1)
        return HttpResponseRedirect(reverse(view, args=[document_page.pk]))


def document_page_navigation_first(request, document_page_id):
    check_permissions(request.user, [PERMISSION_DOCUMENT_VIEW])
    view = resolve_to_name(urlparse.urlparse(request.META.get('HTTP_REFERER', u'/')).path)

    document_page = get_object_or_404(DocumentPage, pk=document_page_id)
    document_page = get_object_or_404(DocumentPage, document=document_page.document, page_number=1)
    return HttpResponseRedirect(reverse(view, args=[document_page.pk]))


def document_page_navigation_last(request, document_page_id):
    check_permissions(request.user, [PERMISSION_DOCUMENT_VIEW])
    view = resolve_to_name(urlparse.urlparse(request.META.get('HTTP_REFERER', u'/')).path)

    document_page = get_object_or_404(DocumentPage, pk=document_page_id)
    document_page = get_object_or_404(DocumentPage, document=document_page.document, page_number=document_page.document.documentpage_set.count())
    return HttpResponseRedirect(reverse(view, args=[document_page.pk]))


def document_list_recent(request):
    return document_list(
        request,
        object_list=[recent_document.document for recent_document in RecentDocument.objects.filter(user=request.user)],
        title=_(u'recent documents'),
        extra_context={
            'recent_count': RECENT_COUNT
        }
    )


def transform_page(request, document_page_id, zoom_function=None, rotation_function=None):
    check_permissions(request.user, [PERMISSION_DOCUMENT_VIEW])
    view = resolve_to_name(urlparse.urlparse(request.META.get('HTTP_REFERER', u'/')).path)

    document_page = get_object_or_404(DocumentPage, pk=document_page_id)
    # Get the query string from the referer url
    query = urlparse.urlparse(request.META.get('HTTP_REFERER', u'/')).query
    # Parse the query string and get the zoom value
    # parse_qs return a dictionary whose values are lists
    zoom = int(urlparse.parse_qs(query).get('zoom', ['100'])[0])
    rotation = int(urlparse.parse_qs(query).get('rotation', ['0'])[0])

    if zoom_function:
        zoom = zoom_function(zoom)

    if rotation_function:
        rotation = rotation_function(rotation)

    return HttpResponseRedirect(
        u'?'.join([
            reverse(view, args=[document_page.pk]),
            urlencode({'zoom': zoom, 'rotation': rotation})
        ])
    )


def document_page_zoom_in(request, document_page_id):
    return transform_page(
        request,
        document_page_id,
        zoom_function=lambda x: ZOOM_MAX_LEVEL if x + ZOOM_PERCENT_STEP > ZOOM_MAX_LEVEL else x + ZOOM_PERCENT_STEP
    )


def document_page_zoom_out(request, document_page_id):
    return transform_page(
        request,
        document_page_id,
        zoom_function=lambda x: ZOOM_MIN_LEVEL if x - ZOOM_PERCENT_STEP < ZOOM_MIN_LEVEL else x - ZOOM_PERCENT_STEP
    )


def document_page_rotate_right(request, document_page_id):
    return transform_page(
        request,
        document_page_id,
        rotation_function=lambda x: (x + ROTATION_STEP) % 360
    )


def document_page_rotate_left(request, document_page_id):
    return transform_page(
        request,
        document_page_id,
        rotation_function=lambda x: (x - ROTATION_STEP) % 360
    )


def document_print(request, document_id):
    check_permissions(request.user, [PERMISSION_DOCUMENT_VIEW])

    document = get_object_or_404(Document, pk=document_id)

    RecentDocument.objects.add_document_for_user(request.user, document)

    post_redirect = None
    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', post_redirect or document.get_absolute_url())))

    new_window_url = None
    html_redirect = None

    if request.method == 'POST':
        form = PrintForm(request.POST)
        if form.is_valid():
            hard_copy_arguments = {}
            # Get page range
            if form.cleaned_data['page_range']:
                hard_copy_arguments['page_range'] = form.cleaned_data['page_range']

            # Compute page width and height
            if form.cleaned_data['custom_page_width'] and form.cleaned_data['custom_page_height']:
                page_width = form.cleaned_data['custom_page_width']
                page_height = form.cleaned_data['custom_page_height']
            elif form.cleaned_data['page_size']:
                page_width, page_height = dict(PAGE_SIZE_DIMENSIONS)[form.cleaned_data['page_size']]

            # Page orientation
            if form.cleaned_data['page_orientation'] == PAGE_ORIENTATION_LANDSCAPE:
                page_width, page_height = page_height, page_width

            hard_copy_arguments['page_width'] = page_width
            hard_copy_arguments['page_height'] = page_height

            new_url = [reverse('document_hard_copy', args=[document_id])]
            if hard_copy_arguments:
                new_url.append(urlquote(hard_copy_arguments))

            new_window_url = u'?'.join(new_url)
            new_window_url_name = u'document_hard_copy'
            #html_redirect = next
            #messages.success(request, _(u'Preparing document hardcopy.'))
    else:
        form = PrintForm()

    return render_to_response('generic_form.html', {
        'form': form,
        'object': document,
        'title': _(u'print: %s') % document,
        'next': next,
        'html_redirect': html_redirect if html_redirect else html_redirect,
        'new_window_url': new_window_url if new_window_url else new_window_url
    }, context_instance=RequestContext(request))


def document_hard_copy(request, document_id):
    #TODO: FIXME
    check_permissions(request.user, [PERMISSION_DOCUMENT_VIEW])

    document = get_object_or_404(Document, pk=document_id)

    RecentDocument.objects.add_document_for_user(request.user, document)

    #arguments, warnings = calculate_converter_arguments(document, size=PRINT_SIZE, file_format=DEFAULT_FILE_FORMAT)

    # Pre-generate
    #convert_document(document, **arguments)

    # Extract dimension values ignoring any unit
    page_width = request.GET.get('page_width', dict(PAGE_SIZE_DIMENSIONS)[DEFAULT_PAPER_SIZE][0])
    page_height = request.GET.get('page_height', dict(PAGE_SIZE_DIMENSIONS)[DEFAULT_PAPER_SIZE][1])

    # TODO: Replace with regex to extact numeric portion
    width = float(page_width.split('i')[0].split('c')[0].split('m')[0])
    height = float(page_height.split('i')[0].split('c')[0].split('m')[0])

    page_range = request.GET.get('page_range', u'')
    if page_range:
        page_range = parse_range(page_range)

        pages = document.documentpage_set.filter(page_number__in=page_range)
    else:
        pages = document.documentpage_set.all()

    return render_to_response('document_print.html', {
        'object': document,
        'page_aspect': width / height,
        'page_orientation': PAGE_ORIENTATION_LANDSCAPE if width / height > 1 else PAGE_ORIENTATION_PORTRAIT,
        'page_orientation_landscape': True if width / height > 1 else False,
        'page_orientation_portrait': False if width / height > 1 else True,
        'page_range': page_range,
        'page_width': page_width,
        'page_height': page_height,
        'pages': pages,
    }, context_instance=RequestContext(request))


def document_type_list(request):
    check_permissions(request.user, [PERMISSION_DOCUMENT_VIEW])

    context = {
        'object_list': DocumentType.objects.all(),
        'title': _(u'document types'),
        'hide_link': True,
        'list_object_variable_name': 'document_type',
    }

    return render_to_response('generic_list.html', context,
        context_instance=RequestContext(request))


def document_type_document_list(request, document_type_id):
    check_permissions(request.user, [PERMISSION_DOCUMENT_VIEW])

    document_type = get_object_or_404(DocumentType, pk=document_type_id)

    return document_list(
        request,
        object_list=Document.objects.filter(document_type=document_type),
        title=_(u'documents of type "%s"') % document_type,
        extra_context={
            'object_name': _(u'document type'),
            'navigation_object_name': 'document_type',
            'document_type': document_type,
        }
    )


def document_type_edit(request, document_type_id):
    check_permissions(request.user, [PERMISSION_DOCUMENT_TYPE_EDIT])
    document_type = get_object_or_404(DocumentType, pk=document_type_id)

    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', reverse('document_type_list'))))

    if request.method == 'POST':
        form = DocumentTypeForm(instance=document_type, data=request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, _(u'Document type edited successfully'))
                return HttpResponseRedirect(next)
            except Exception, e:
                messages.error(request, _(u'Error editing document type; %s') % e)
    else:
        form = DocumentTypeForm(instance=document_type)

    return render_to_response('generic_form.html', {
        'title': _(u'edit document type: %s') % document_type,
        'form': form,
        #'object': document_type,
        #'object_name': _(u'document type'),
        'object_name': _(u'document type'),
        'navigation_object_name': 'document_type',
        'document_type': document_type,        
        'next': next
    },
    context_instance=RequestContext(request))


def document_type_delete(request, document_type_id):
    check_permissions(request.user, [PERMISSION_DOCUMENT_TYPE_DELETE])
    document_type = get_object_or_404(DocumentType, pk=document_type_id)

    post_action_redirect = reverse('document_type_list')

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', '/')))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', '/')))

    if request.method == 'POST':
        try:
            Document.objects.filter(document_type=document_type).update(document_type=None)
            document_type.delete()
            messages.success(request, _(u'Document type: %s deleted successfully.') % document_type)
        except Exception, e:
            messages.error(request, _(u'Document type: %(document_type)s delete error: %(error)s') % {
                'document_type': document_type, 'error': e})

        return HttpResponseRedirect(next)

    context = {
        'object_name': _(u'document type'),
        'delete_view': True,
        'previous': previous,
        'next': next,

        'object_name': _(u'document type'),
        'navigation_object_name': 'document_type',
        'document_type': document_type,

        'title': _(u'Are you sure you wish to delete the document type: %s?') % document_type,
        'message': _(u'The document type of all documents using this document type will be set to none.'),
        'form_icon': u'layout_delete.png',
    }

    return render_to_response('generic_confirm.html', context,
        context_instance=RequestContext(request))


def document_type_create(request):
    check_permissions(request.user, [PERMISSION_DOCUMENT_TYPE_CREATE])

    if request.method == 'POST':
        form = DocumentTypeForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, _(u'Document type created successfully'))
                return HttpResponseRedirect(reverse('document_type_list'))
            except Exception, e:
                messages.error(request, _(u'Error creating document type; %(error)s') % {
                    'error': e})
    else:
        form = DocumentTypeForm()

    return render_to_response('generic_form.html', {
        'title': _(u'create document type'),
        'form': form,
    },
    context_instance=RequestContext(request))


def document_type_filename_list(request, document_type_id):
    check_permissions(request.user, [PERMISSION_DOCUMENT_VIEW])
    document_type = get_object_or_404(DocumentType, pk=document_type_id)

    context = {
        'object_list': document_type.documenttypefilename_set.all(),
        'title': _(u'filenames for document type: %s') % document_type,
        'object_name': _(u'document type'),
        'navigation_object_name': 'document_type',
        'document_type': document_type,
        'list_object_variable_name': 'filename',
        'hide_link': True,
        'extra_columns': [
            {
                'name': _(u'enabled'),
                'attribute': encapsulate(lambda x: two_state_template(x.enabled)),
            }
        ]
    }

    return render_to_response('generic_list.html', context,
        context_instance=RequestContext(request))


def document_type_filename_edit(request, document_type_filename_id):
    check_permissions(request.user, [PERMISSION_DOCUMENT_TYPE_EDIT])
    document_type_filename = get_object_or_404(DocumentTypeFilename, pk=document_type_filename_id)

    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', reverse('document_type_filename_list', args=[document_type_filename.document_type_id]))))

    if request.method == 'POST':
        form = DocumentTypeFilenameForm(instance=document_type_filename, data=request.POST)
        if form.is_valid():
            try:
                document_type_filename.filename = form.cleaned_data['filename']
                document_type_filename.enabled = form.cleaned_data['enabled']
                document_type_filename.save()
                messages.success(request, _(u'Document type filename edited successfully'))
                return HttpResponseRedirect(next)
            except Exception, e:
                messages.error(request, _(u'Error editing document type filename; %s') % e)
    else:
        form = DocumentTypeFilenameForm(instance=document_type_filename)

    return render_to_response('generic_form.html', {
        'title': _(u'edit filename "%(filename)s" from document type "%(document_type)s"') % {
            'document_type': document_type_filename.document_type, 'filename': document_type_filename
        },
        'form': form,
        'next': next,
        'filename': document_type_filename,
        'document_type': document_type_filename.document_type,
        'navigation_object_list': [
            {'object': 'document_type', 'name': _(u'document type')},
            {'object': 'filename', 'name': _(u'document type filename')}
        ],
    },
    context_instance=RequestContext(request))


def document_type_filename_delete(request, document_type_filename_id):
    check_permissions(request.user, [PERMISSION_DOCUMENT_TYPE_EDIT])
    document_type_filename = get_object_or_404(DocumentTypeFilename, pk=document_type_filename_id)

    post_action_redirect = reverse('document_type_filename_list', args=[document_type_filename.document_type_id])

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', '/')))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', '/')))

    if request.method == 'POST':
        try:
            document_type_filename.delete()
            messages.success(request, _(u'Document type filename: %s deleted successfully.') % document_type_filename)
        except Exception, e:
            messages.error(request, _(u'Document type filename: %(document_type_filename)s delete error: %(error)s') % {
                'document_type_filename': document_type_filename, 'error': e})

        return HttpResponseRedirect(next)

    context = {
        'object_name': _(u'document type filename'),
        'delete_view': True,
        'previous': previous,
        'next': next,
        'filename': document_type_filename,
        'document_type': document_type_filename.document_type,
        'navigation_object_list': [
            {'object': 'document_type', 'name': _(u'document type')},
            {'object': 'filename', 'name': _(u'document type filename')}
        ],
        'title': _(u'Are you sure you wish to delete the filename: %(filename)s, from document type "%(document_type)s"?') % {
            'document_type': document_type_filename.document_type, 'filename': document_type_filename
        },
        'form_icon': u'database_delete.png',
    }

    return render_to_response('generic_confirm.html', context,
        context_instance=RequestContext(request))


def document_type_filename_create(request, document_type_id):
    check_permissions(request.user, [PERMISSION_DOCUMENT_TYPE_EDIT])

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
                messages.success(request, _(u'Document type filename created successfully'))
                return HttpResponseRedirect(reverse('document_type_filename_list', args=[document_type_id]))
            except Exception, e:
                messages.error(request, _(u'Error creating document type filename; %(error)s') % {
                    'error': e})
    else:
        form = DocumentTypeFilenameForm_create()

    return render_to_response('generic_form.html', {
        'title': _(u'create filename for document type: %s') % document_type,
        'form': form,
        'document_type': document_type,
    },
    context_instance=RequestContext(request))
