from __future__ import absolute_import

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.utils.safestring import mark_safe
from django.conf import settings
from django.core.exceptions import PermissionDenied

from documents.permissions import (PERMISSION_DOCUMENT_CREATE,
    PERMISSION_DOCUMENT_NEW_VERSION)
from documents.models import DocumentType, Document
from documents.conf.settings import THUMBNAIL_SIZE
from documents.exceptions import NewDocumentVersionNotAllowed
from metadata.api import decode_metadata_from_url, metadata_repr_as_list
from permissions.models import Permission
from common.utils import encapsulate
import sendfile
from acls.models import AccessEntry

from sources.models import (WebForm, StagingFolder, SourceTransformation,
    WatchFolder)
from sources.literals import (SOURCE_CHOICE_WEB_FORM, SOURCE_CHOICE_STAGING,
    SOURCE_CHOICE_WATCH)
from sources.literals import (SOURCE_UNCOMPRESS_CHOICE_Y,
    SOURCE_UNCOMPRESS_CHOICE_ASK)
from sources.staging import create_staging_file_class
from sources.forms import (StagingDocumentForm, WebFormForm,
    WatchFolderSetupForm)
from sources.forms import WebFormSetupForm, StagingFolderSetupForm
from sources.forms import SourceTransformationForm, SourceTransformationForm_create
from .permissions import (PERMISSION_SOURCES_SETUP_VIEW,
    PERMISSION_SOURCES_SETUP_EDIT, PERMISSION_SOURCES_SETUP_DELETE,
    PERMISSION_SOURCES_SETUP_CREATE)


def return_function(obj):
    return lambda context: context['source'].source_type == obj.source_type and context['source'].pk == obj.pk


def get_tab_link_for_source(source, document=None):
    if document:
        view = u'upload_version'
        args = [document.pk, u'"%s"' % source.source_type, source.pk]
    else:
        view = u'upload_interactive'
        args = [u'"%s"' % source.source_type, source.pk]

    return {
        'text': source.title,
        'view': view,
        'args': args,
        'famfam': source.icon,
        'keep_query': True,
        'conditional_highlight': return_function(source),
    }


def get_active_tab_links(document=None):
    tab_links = []

    web_forms = WebForm.objects.filter(enabled=True)
    for web_form in web_forms:
        tab_links.append(get_tab_link_for_source(web_form, document))

    staging_folders = StagingFolder.objects.filter(enabled=True)
    for staging_folder in staging_folders:
        tab_links.append(get_tab_link_for_source(staging_folder, document))

    return {
        'tab_links': tab_links,
        SOURCE_CHOICE_WEB_FORM: web_forms,
        SOURCE_CHOICE_STAGING: staging_folders
    }


def upload_interactive(request, source_type=None, source_id=None, document_pk=None):
    subtemplates_list = []

    if document_pk:
        document = get_object_or_404(Document, pk=document_pk)
        try:
            Permission.objects.check_permissions(request.user, [PERMISSION_DOCUMENT_NEW_VERSION])
        except PermissionDenied:
            AccessEntry.objects.check_access(PERMISSION_DOCUMENT_NEW_VERSION, request.user, document)

        results = get_active_tab_links(document)
    else:
        Permission.objects.check_permissions(request.user, [PERMISSION_DOCUMENT_CREATE])
        document = None
        results = get_active_tab_links()

    context = {}

    if results[SOURCE_CHOICE_WEB_FORM].count() == 0 and results[SOURCE_CHOICE_STAGING].count() == 0:
        source_setup_link = mark_safe('<a href="%s">%s</a>' % (reverse('setup_web_form_list'), ugettext(u'here')))
        subtemplates_list.append(
            {
                'name': 'generic_subtemplate.html',
                'context': {
                    'title': _(u'Upload sources'),
                    'paragraphs': [
                        _(u'No interactive document sources have been defined or none have been enabled.'),
                        _(u'Click %(setup_link)s to add or enable some document sources.') % {
                            'setup_link': source_setup_link
                        }
                    ],
                }
            })

    document_type_id = request.GET.get('document_type_id', None)
    if document_type_id:
        document_type = get_object_or_404(DocumentType, pk=document_type_id[0])
    else:
        document_type = None

    if source_type is None and source_id is None:
        if results[SOURCE_CHOICE_WEB_FORM].count():
            source_type = results[SOURCE_CHOICE_WEB_FORM][0].source_type
            source_id = results[SOURCE_CHOICE_WEB_FORM][0].pk
        elif results[SOURCE_CHOICE_STAGING].count():
            source_type = results[SOURCE_CHOICE_STAGING][0].source_type
            source_id = results[SOURCE_CHOICE_STAGING][0].pk

    if source_type and source_id:
        if source_type == SOURCE_CHOICE_WEB_FORM:
            web_form = get_object_or_404(WebForm, pk=source_id)
            context['source'] = web_form
            if request.method == 'POST':
                form = WebFormForm(request.POST, request.FILES,
                    document_type=document_type,
                    show_expand=(web_form.uncompress == SOURCE_UNCOMPRESS_CHOICE_ASK) and not document,
                    source=web_form,
                    instance=document
                )
                if form.is_valid():
                    try:
                        if document:
                            expand = False
                        else:
                            if web_form.uncompress == SOURCE_UNCOMPRESS_CHOICE_ASK:
                                expand = form.cleaned_data.get('expand')
                            else:
                                if web_form.uncompress == SOURCE_UNCOMPRESS_CHOICE_Y:
                                    expand = True
                                else:
                                    expand = False

                        new_filename = get_form_filename(form)

                        result = web_form.upload_file(request.FILES['file'],
                            new_filename, use_file_name=form.cleaned_data.get('use_file_name', False),
                            document_type=document_type,
                            expand=expand,
                            metadata_dict_list=decode_metadata_from_url(request.GET),
                            user=request.user,
                            document=document,
                            new_version_data=form.cleaned_data.get('new_version_data')
                        )
                        if document:
                            messages.success(request, _(u'New document version uploaded successfully.'))
                            return HttpResponseRedirect(reverse('document_view_simple', args=[document.pk]))
                        else:
                            if result['is_compressed'] == None:
                                messages.success(request, _(u'File uploaded successfully.'))

                            if result['is_compressed'] == True:
                                messages.success(request, _(u'File uncompressed successfully and uploaded as individual files.'))

                            if result['is_compressed'] == False:
                                messages.warning(request, _(u'File was not a compressed file, uploaded as it was.'))

                            return HttpResponseRedirect(request.get_full_path())
                    except NewDocumentVersionNotAllowed:
                        messages.error(request, _(u'New version uploads are not allowed for this document.'))
                    except Exception, e:
                        if settings.DEBUG:
                            raise
                        messages.error(request, _(u'Unhandled exception: %s') % e)
            else:
                form = WebFormForm(
                    show_expand=(web_form.uncompress == SOURCE_UNCOMPRESS_CHOICE_ASK) and not document,
                    document_type=document_type,
                    source=web_form,
                    instance=document
                )
            if document:
                title = _(u'upload a new version from source: %s') % web_form.title
            else:
                title = _(u'upload a local document from source: %s') % web_form.title

            subtemplates_list.append({
                'name': 'generic_form_subtemplate.html',
                'context': {
                    'form': form,
                    'title': title,
                },
            })
        elif source_type == SOURCE_CHOICE_STAGING:
            staging_folder = get_object_or_404(StagingFolder, pk=source_id)
            context['source'] = staging_folder
            StagingFile = create_staging_file_class(request, staging_folder.folder_path, source=staging_folder)
            if request.method == 'POST':
                form = StagingDocumentForm(request.POST, request.FILES,
                    cls=StagingFile, document_type=document_type,
                    show_expand=(staging_folder.uncompress == SOURCE_UNCOMPRESS_CHOICE_ASK) and not document,
                    source=staging_folder,
                    instance=document
                )
                if form.is_valid():
                    try:
                        staging_file = StagingFile.get(form.cleaned_data['staging_file_id'])
                        if document:
                            expand = False
                        else:
                            if staging_folder.uncompress == SOURCE_UNCOMPRESS_CHOICE_ASK:
                                expand = form.cleaned_data.get('expand')
                            else:
                                if staging_folder.uncompress == SOURCE_UNCOMPRESS_CHOICE_Y:
                                    expand = True
                                else:
                                    expand = False

                        new_filename = get_form_filename(form)

                        result = staging_folder.upload_file(staging_file.upload(),
                            new_filename, use_file_name=form.cleaned_data.get('use_file_name', False),
                            document_type=document_type,
                            expand=expand,
                            metadata_dict_list=decode_metadata_from_url(request.GET),
                            user=request.user,
                            document=document,
                            new_version_data=form.cleaned_data.get('new_version_data')
                        )
                        if document:
                            messages.success(request, _(u'Document version from staging file: %s, uploaded successfully.') % staging_file.filename)
                        else:
                            if result['is_compressed'] == None:
                                messages.success(request, _(u'Staging file: %s, uploaded successfully.') % staging_file.filename)

                        if result['is_compressed'] == True:
                            messages.success(request, _(u'Staging file: %s, uncompressed successfully and uploaded as individual files.') % staging_file.filename)

                        if result['is_compressed'] == False:
                            messages.warning(request, _(u'Staging file: %s, was not compressed, uploaded as a single file.') % staging_file.filename)

                        if staging_folder.delete_after_upload:
                            transformations, errors = staging_folder.get_transformation_list()
                            staging_file.delete(preview_size=staging_folder.get_preview_size(), transformations=transformations)
                            messages.success(request, _(u'Staging file: %s, deleted successfully.') % staging_file.filename)
                        if document:
                            return HttpResponseRedirect(reverse('document_view_simple', args=[document.pk]))
                        else:
                            return HttpResponseRedirect(request.get_full_path())
                    except NewDocumentVersionNotAllowed:
                        messages.error(request, _(u'New version uploads are not allowed for this document.'))
                    except Exception, e:
                        if settings.DEBUG:
                            raise
                        messages.error(request, _(u'Unhandled exception: %s') % e)
            else:
                form = StagingDocumentForm(cls=StagingFile,
                    document_type=document_type,
                    show_expand=(staging_folder.uncompress == SOURCE_UNCOMPRESS_CHOICE_ASK) and not document,
                    source=staging_folder,
                    instance=document
                )
            try:
                staging_filelist = StagingFile.get_all()
            except Exception, e:
                messages.error(request, e)
                staging_filelist = []
            finally:
                if document:
                    title = _(u'upload a new version from staging source: %s') % staging_folder.title
                else:
                    title = _(u'upload a document from staging source: %s') % staging_folder.title

                subtemplates_list = [
                    {
                        'name': 'generic_form_subtemplate.html',
                        'context': {
                            'form': form,
                            'title': title,
                        }
                    },
                    {
                        'name': 'generic_list_subtemplate.html',
                        'context': {
                            'title': _(u'files in staging path'),
                            'object_list': staging_filelist,
                            'hide_link': True,
                        }
                    },
                ]

    if document:
        context['object'] = document

    context.update({
        'document_type_id': document_type_id,
        'subtemplates_list': subtemplates_list,
        'temporary_navigation_links': {
            'form_header': {
                'upload_version': {
                    'links': results['tab_links']
                },
                'upload_interactive': {
                    'links': results['tab_links']
                }
            }
        },
    })

    if not document:
        context.update(
            {
                'sidebar_subtemplates_list': [
                    {
                        'name': 'generic_subtemplate.html',
                        'context': {
                            'title': _(u'Current document type'),
                            'paragraphs': [document_type if document_type else _(u'None')],
                            'side_bar': True,
                        }
                    },
                    {
                        'name': 'generic_subtemplate.html',
                        'context': {
                            'title': _(u'Current metadata'),
                            'paragraphs': metadata_repr_as_list(decode_metadata_from_url(request.GET)),
                            'side_bar': True,
                        }
                    }
                ],
            }
        )

    return render_to_response('generic_form.html', context,
        context_instance=RequestContext(request))


def get_form_filename(form):
    filename = None
    if form:
        if form.cleaned_data['new_filename']:
            return form.cleaned_data['new_filename']

    if form and 'document_type_available_filenames' in form.cleaned_data:
        if form.cleaned_data['document_type_available_filenames']:
            return form.cleaned_data['document_type_available_filenames'].filename

    return filename


def staging_file_preview(request, source_type, source_id, staging_file_id):
    Permission.objects.check_permissions(request.user, [PERMISSION_DOCUMENT_CREATE, PERMISSION_DOCUMENT_NEW_VERSION])
    staging_folder = get_object_or_404(StagingFolder, pk=source_id)
    StagingFile = create_staging_file_class(request, staging_folder.folder_path)
    transformations, errors = SourceTransformation.transformations.get_for_object_as_list(staging_folder)

    output_file = StagingFile.get(staging_file_id).get_image(
        size=staging_folder.get_preview_size(),
        transformations=transformations
    )
    if errors and (request.user.is_staff or request.user.is_superuser):
        for error in errors:
            messages.warning(request, _(u'Staging file transformation error: %(error)s') % {
                'error': error
            })

    return sendfile.sendfile(request, output_file)


def staging_file_thumbnail(request, source_id, staging_file_id):
    Permission.objects.check_permissions(request.user, [PERMISSION_DOCUMENT_CREATE, PERMISSION_DOCUMENT_NEW_VERSION])
    staging_folder = get_object_or_404(StagingFolder, pk=source_id)
    StagingFile = create_staging_file_class(request, staging_folder.folder_path, source=staging_folder)
    transformations, errors = SourceTransformation.transformations.get_for_object_as_list(staging_folder)

    output_file = StagingFile.get(staging_file_id).get_image(
        size=THUMBNAIL_SIZE,
        transformations=transformations
    )
    if errors and (request.user.is_staff or request.user.is_superuser):
        for error in errors:
            messages.warning(request, _(u'Staging file transformation error: %(error)s') % {
                'error': error
            })

    return sendfile.sendfile(request, output_file)


def staging_file_delete(request, source_type, source_id, staging_file_id):
    Permission.objects.check_permissions(request.user, [PERMISSION_DOCUMENT_CREATE, PERMISSION_DOCUMENT_NEW_VERSION])
    staging_folder = get_object_or_404(StagingFolder, pk=source_id)
    StagingFile = create_staging_file_class(request, staging_folder.folder_path)

    staging_file = StagingFile.get(staging_file_id)
    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', '/')))
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', '/')))

    if request.method == 'POST':
        try:
            transformations, errors = SourceTransformation.transformations.get_for_object_as_list(staging_folder)
            staging_file.delete(
                preview_size=staging_folder.get_preview_size(),
                transformations=transformations
            )
            messages.success(request, _(u'Staging file delete successfully.'))
        except Exception, e:
            messages.error(request, _(u'Staging file delete error; %s.') % e)
        return HttpResponseRedirect(next)

    results = get_active_tab_links()

    return render_to_response('generic_confirm.html', {
        'source': staging_folder,
        'delete_view': True,
        'object': staging_file,
        'next': next,
        'previous': previous,
        'form_icon': u'delete.png',
        'temporary_navigation_links': {'form_header': {'staging_file_delete': {'links': results['tab_links']}}},
    }, context_instance=RequestContext(request))


# Setup views
def setup_source_list(request, source_type):
    Permission.objects.check_permissions(request.user, [PERMISSION_SOURCES_SETUP_VIEW])

    if source_type == SOURCE_CHOICE_WEB_FORM:
        cls = WebForm
    elif source_type == SOURCE_CHOICE_STAGING:
        cls = StagingFolder
    elif source_type == SOURCE_CHOICE_WATCH:
        cls = WatchFolder

    context = {
        'object_list': cls.objects.all(),
        'title': cls.class_fullname_plural(),
        'hide_link': True,
        'list_object_variable_name': 'source',
        'source_type': source_type,
    }

    return render_to_response('generic_list.html', context,
        context_instance=RequestContext(request))


def setup_source_edit(request, source_type, source_id):
    Permission.objects.check_permissions(request.user, [PERMISSION_SOURCES_SETUP_EDIT])

    if source_type == SOURCE_CHOICE_WEB_FORM:
        cls = WebForm
        form_class = WebFormSetupForm
    elif source_type == SOURCE_CHOICE_STAGING:
        cls = StagingFolder
        form_class = StagingFolderSetupForm
    elif source_type == SOURCE_CHOICE_WATCH:
        cls = WatchFolder
        form_class = WatchFolderSetupForm

    source = get_object_or_404(cls, pk=source_id)
    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', '/')))

    if request.method == 'POST':
        form = form_class(instance=source, data=request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, _(u'Source edited successfully'))
                return HttpResponseRedirect(next)
            except Exception, e:
                messages.error(request, _(u'Error editing source; %s') % e)
    else:
        form = form_class(instance=source)

    return render_to_response('generic_form.html', {
        'title': _(u'edit source: %s') % source.fullname(),
        'form': form,
        'source': source,
        'navigation_object_name': 'source',
        'next': next,
        'object_name': _(u'source'),
        'source_type': source_type,
    },
    context_instance=RequestContext(request))


def setup_source_delete(request, source_type, source_id):
    Permission.objects.check_permissions(request.user, [PERMISSION_SOURCES_SETUP_DELETE])
    if source_type == SOURCE_CHOICE_WEB_FORM:
        cls = WebForm
        form_icon = u'application_form_delete.png'
        redirect_view = 'setup_web_form_list'
    elif source_type == SOURCE_CHOICE_STAGING:
        cls = StagingFolder
        form_icon = u'folder_delete.png'
        redirect_view = 'setup_staging_folder_list'
    elif source_type == SOURCE_CHOICE_WATCH:
        cls = WatchFolder
        form_icon = u'folder_delete.png'
        redirect_view = 'setup_watch_folder_list'

    redirect_view = reverse('setup_source_list', args=[source_type])
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', redirect_view)))

    source = get_object_or_404(cls, pk=source_id)

    if request.method == 'POST':
        try:
            source.delete()
            messages.success(request, _(u'Source "%s" deleted successfully.') % source)
        except Exception, e:
            messages.error(request, _(u'Error deleting source "%(source)s": %(error)s') % {
                'source': source, 'error': e
            })

        return HttpResponseRedirect(redirect_view)

    context = {
        'title': _(u'Are you sure you wish to delete the source: %s?') % source.fullname(),
        'source': source,
        'object_name': _(u'source'),
        'navigation_object_name': 'source',
        'delete_view': True,
        'previous': previous,
        'form_icon': form_icon,
        'source_type': source_type,
    }

    return render_to_response('generic_confirm.html', context,
        context_instance=RequestContext(request))


def setup_source_create(request, source_type):
    Permission.objects.check_permissions(request.user, [PERMISSION_SOURCES_SETUP_CREATE])

    if source_type == SOURCE_CHOICE_WEB_FORM:
        cls = WebForm
        form_class = WebFormSetupForm
    elif source_type == SOURCE_CHOICE_STAGING:
        cls = StagingFolder
        form_class = StagingFolderSetupForm
    elif source_type == SOURCE_CHOICE_WATCH:
        cls = WatchFolder
        form_class = WatchFolderSetupForm

    if request.method == 'POST':
        form = form_class(data=request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, _(u'Source created successfully'))
                return HttpResponseRedirect(reverse('setup_web_form_list'))
            except Exception, e:
                messages.error(request, _(u'Error creating source; %s') % e)
    else:
        form = form_class()

    return render_to_response('generic_form.html', {
        'title': _(u'Create new source of type: %s') % cls.class_fullname(),
        'form': form,
        'source_type': source_type,
        'navigation_object_name': 'source',
    },
    context_instance=RequestContext(request))


def setup_source_transformation_list(request, source_type, source_id):
    Permission.objects.check_permissions(request.user, [PERMISSION_SOURCES_SETUP_EDIT])

    if source_type == SOURCE_CHOICE_WEB_FORM:
        cls = WebForm
    elif source_type == SOURCE_CHOICE_STAGING:
        cls = StagingFolder
    elif source_type == SOURCE_CHOICE_WATCH:
        cls = WatchFolder

    source = get_object_or_404(cls, pk=source_id)

    context = {
        'object_list': SourceTransformation.transformations.get_for_object(source),
        'title': _(u'transformations for: %s') % source.fullname(),
        'source': source,
        'object_name': _(u'source'),
        'navigation_object_name': 'source',
        'list_object_variable_name': 'transformation',
        'extra_columns': [
            {'name': _(u'order'), 'attribute': 'order'},
            {'name': _(u'transformation'), 'attribute': encapsulate(lambda x: x.get_transformation_display())},
            {'name': _(u'arguments'), 'attribute': 'arguments'}
            ],
        'hide_link': True,
        'hide_object': True,
    }

    return render_to_response('generic_list.html', context,
        context_instance=RequestContext(request))


def setup_source_transformation_edit(request, transformation_id):
    Permission.objects.check_permissions(request.user, [PERMISSION_SOURCES_SETUP_EDIT])

    source_transformation = get_object_or_404(SourceTransformation, pk=transformation_id)
    redirect_view = reverse('setup_source_transformation_list', args=[source_transformation.content_object.source_type, source_transformation.content_object.pk])
    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', redirect_view)))

    if request.method == 'POST':
        form = SourceTransformationForm(instance=source_transformation, data=request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, _(u'Source transformation edited successfully'))
                return HttpResponseRedirect(next)
            except Exception, e:
                messages.error(request, _(u'Error editing source transformation; %s') % e)
    else:
        form = SourceTransformationForm(instance=source_transformation)

    return render_to_response('generic_form.html', {
        'title': _(u'Edit transformation: %s') % source_transformation,
        'form': form,
        'source': source_transformation.content_object,
        'transformation': source_transformation,
        'navigation_object_list': [
            {'object': 'source', 'name': _(u'source')},
            {'object': 'transformation', 'name': _(u'transformation')}
        ],
        'next': next,
    },
    context_instance=RequestContext(request))


def setup_source_transformation_delete(request, transformation_id):
    Permission.objects.check_permissions(request.user, [PERMISSION_SOURCES_SETUP_EDIT])

    source_transformation = get_object_or_404(SourceTransformation, pk=transformation_id)
    redirect_view = reverse('setup_source_transformation_list', args=[source_transformation.content_object.source_type, source_transformation.content_object.pk])
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', redirect_view)))

    if request.method == 'POST':
        try:
            source_transformation.delete()
            messages.success(request, _(u'Source transformation deleted successfully.'))
        except Exception, e:
            messages.error(request, _(u'Error deleting source transformation; %(error)s') % {
                'error': e}
            )
        return HttpResponseRedirect(redirect_view)

    return render_to_response('generic_confirm.html', {
        'delete_view': True,
        'transformation': source_transformation,
        'source': source_transformation.content_object,
        'navigation_object_list': [
            {'object': 'source', 'name': _(u'source')},
            {'object': 'transformation', 'name': _(u'transformation')}
        ],
        'title': _(u'Are you sure you wish to delete source transformation "%(transformation)s"') % {
            'transformation': source_transformation.get_transformation_display(),
        },
        'previous': previous,
        'form_icon': u'shape_square_delete.png',
    },
    context_instance=RequestContext(request))


def setup_source_transformation_create(request, source_type, source_id):
    Permission.objects.check_permissions(request.user, [PERMISSION_SOURCES_SETUP_EDIT])

    if source_type == SOURCE_CHOICE_WEB_FORM:
        cls = WebForm
    elif source_type == SOURCE_CHOICE_STAGING:
        cls = StagingFolder
    elif source_type == SOURCE_CHOICE_WATCH:
        cls = WatchFolder

    source = get_object_or_404(cls, pk=source_id)

    redirect_view = reverse('setup_source_transformation_list', args=[source.source_type, source.pk])

    if request.method == 'POST':
        form = SourceTransformationForm_create(request.POST)
        if form.is_valid():
            try:
                source_tranformation = form.save(commit=False)
                source_tranformation.content_object = source
                source_tranformation.save()
                messages.success(request, _(u'Source transformation created successfully'))
                return HttpResponseRedirect(redirect_view)
            except Exception, e:
                messages.error(request, _(u'Error creating source transformation; %s') % e)
    else:
        form = SourceTransformationForm_create()

    return render_to_response('generic_form.html', {
        'form': form,
        'source': source,
        'object_name': _(u'source'),
        'navigation_object_name': 'source',
        'title': _(u'Create new transformation for source: %s') % source,
    }, context_instance=RequestContext(request))
