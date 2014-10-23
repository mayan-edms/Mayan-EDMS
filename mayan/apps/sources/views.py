from __future__ import absolute_import

import tempfile

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.http import urlencode
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _

from acls.models import AccessEntry
from common.utils import encapsulate
from documents.exceptions import NewDocumentVersionNotAllowed
from documents.models import DocumentType, Document
from documents.permissions import (PERMISSION_DOCUMENT_CREATE,
                                   PERMISSION_DOCUMENT_NEW_VERSION)
from metadata.api import decode_metadata_from_url, metadata_repr_as_list
from permissions.models import Permission

from .forms import (NewDocumentForm, SourceTransformationForm,
                    SourceTransformationForm_create)
from .literals import (SOURCE_CHOICE_STAGING, SOURCE_CHOICE_WEB_FORM,
                       SOURCE_UNCOMPRESS_CHOICE_ASK, SOURCE_UNCOMPRESS_CHOICE_Y)
from .models import (InteractiveSource, Source, StagingFolderSource,
                     SourceTransformation, WebFormSource)
from .permissions import (PERMISSION_SOURCES_SETUP_CREATE,
                          PERMISSION_SOURCES_SETUP_DELETE,
                          PERMISSION_SOURCES_SETUP_EDIT,
                          PERMISSION_SOURCES_SETUP_VIEW)
from .tasks import task_upload_document
from .utils import get_class, get_form_class, get_upload_form_class


def document_create_siblings(request, document_id):
    Permission.objects.check_permissions(request.user, [PERMISSION_DOCUMENT_CREATE])

    document = get_object_or_404(Document, pk=document_id)
    query_dict = {}
    for pk, metadata in enumerate(document.metadata.all()):
        query_dict['metadata%s_id' % pk] = metadata.metadata_type_id
        query_dict['metadata%s_value' % pk] = metadata.value

    query_dict['document_type_id'] = document.document_type_id

    url = reverse('sources:upload_interactive')
    return HttpResponseRedirect('%s?%s' % (url, urlencode(query_dict)))


def return_function(obj):
    return lambda context: context['source'].source_type == obj.source_type and context['source'].pk == obj.pk


def get_tab_link_for_source(source, document=None):
    if document:
        view = u'sources:upload_version'
        args = [document.pk, source.pk]
    else:
        view = u'sources:upload_interactive'
        args = [source.pk]

    return {
        'text': source.title,
        'view': view,
        'args': args,
        'keep_query': True,
        'conditional_highlight': return_function(source),
    }


def get_active_tab_links(document=None):
    tab_links = []

    web_forms = WebFormSource.objects.filter(enabled=True)
    for web_form in web_forms:
        tab_links.append(get_tab_link_for_source(web_form, document))

    staging_folders = StagingFolderSource.objects.filter(enabled=True)
    for staging_folder in staging_folders:
        tab_links.append(get_tab_link_for_source(staging_folder, document))

    return {
        'tab_links': tab_links,
        SOURCE_CHOICE_WEB_FORM: web_forms,
        SOURCE_CHOICE_STAGING: staging_folders,
    }


def upload_new_version(request, document_id):
    document = get_object_or_404(Document, pk=document_pk)
    #    try:
    #        Permission.objects.check_permissions(request.user, [PERMISSION_DOCUMENT_NEW_VERSION])
    #    except PermissionDenied:
    #        AccessEntry.objects.check_access(PERMISSION_DOCUMENT_NEW_VERSION, request.user, document)
    #    results = get_active_tab_links(document)

    #    messages.success(request, _(u'New document version queued for uploaded and will be available shortly.'))
    #    return HttpResponseRedirect(reverse('documents:document_version_list', args=[document.pk]))

    #    title = _(u'Upload a new version from source: %s') % source.title
    # TODO: move to version upload
    #if document:
    #context['object'] = document
    pass


def upload_interactive(request, source_id=None):
    subtemplates_list = []

    Permission.objects.check_permissions(request.user, [PERMISSION_DOCUMENT_CREATE])
    results = get_active_tab_links()

    context = {}

    if InteractiveSource.objects.filter(enabled=True).count() == 0:
        subtemplates_list.append(
            {
                'name': 'main/generic_subtemplate.html',
                'context': {
                    'title': _(u'Upload sources'),
                    'paragraphs': [
                        _(u'No interactive document sources have been defined or none have been enabled.'),
                    ],
                }
            })

    document_type = get_object_or_404(DocumentType, pk=request.GET['document_type_id'])

    if source_id:
        source = get_object_or_404(Source.objects.filter(enabled=True).select_subclasses(), pk=source_id)
    else:
        source = InteractiveSource.objects.filter(enabled=True).select_subclasses().first()

    if source:
        upload_form_class = get_upload_form_class(source.source_type)

        context['source'] = source

        if request.method == 'POST':
            upload_form = upload_form_class(
                request.POST, request.FILES,
                show_expand=(source.uncompress == SOURCE_UNCOMPRESS_CHOICE_ASK),
                source=source,
                prefix='source'
            )
            document_form = NewDocumentForm(
                data=request.POST,
                document_type=document_type,
                prefix='document')

            if upload_form.is_valid() and document_form.is_valid():
                try:
                    if source.uncompress == SOURCE_UNCOMPRESS_CHOICE_ASK:
                        expand = upload_form.cleaned_data.get('expand')
                    else:
                        if source.uncompress == SOURCE_UNCOMPRESS_CHOICE_Y:
                            expand = True
                        else:
                            expand = False

                    # TODO: move this to model: "get_file_object(request, upload_form)"
                    if isinstance(source, WebFormSource):
                        staging_file = None
                        file_object = request.FILES['source-file']
                    else:
                        staging_file = source.get_file(encoded_filename=upload_form.cleaned_data['staging_file_id'])
                        file_object = staging_file.as_file()

                    temporary_file = tempfile.NamedTemporaryFile(delete=False)
                    for chunk in file_object.chunks():
                        temporary_file.write(chunk)

                    temporary_file.close()
                    file_object.close()

                    # TODO: move this to model: "post_upload(request)"
                    if isinstance(source, StagingFolderSource):
                        if source.delete_after_upload:
                            try:
                                staging_file.delete()
                            except Exception as exception:
                                messages.error(request, _(u'Error deleting staging file; %s') % exception)

                    if not request.user.is_anonymous():
                        user_id = request.user.pk
                    else:
                        user_id = None

                    # Determine how to name the new document
                    label = file_object.name

                    if 'document_type_available_filenames' in document_form.cleaned_data:
                        if document_form.cleaned_data['document_type_available_filenames']:
                            label = document_form.cleaned_data['document_type_available_filenames'].filename

                    task_upload_document.apply_async(kwargs=dict(
                        source_id=source.pk,
                        file_path=temporary_file.name,
                        label=label,
                        document_type_id=document_type.pk,
                        expand=expand,
                        metadata_dict_list=decode_metadata_from_url(request.GET),
                        user_id=user_id,
                        description=document_form.cleaned_data.get('description'),
                        language=document_form.cleaned_data.get('language')
                    ), queue='uploads')

                    messages.success(request, _(u'New document queued for uploaded and will be available shortly.'))
                    return HttpResponseRedirect(request.get_full_path())
                except Exception as exception:
                    if settings.DEBUG:
                        raise
                    messages.error(request, _(u'Unhandled exception: %s') % exception)
        else:
            upload_form = upload_form_class(
                show_expand=(source.uncompress == SOURCE_UNCOMPRESS_CHOICE_ASK),
                source=source,
                prefix='source',
            )
            document_form = NewDocumentForm(
                document_type=document_type,
                prefix='document')

        title = _(u'Upload a local document from source: %s') % source.title

        if isinstance(source, StagingFolderSource):
            try:
                staging_filelist = list(source.get_files())
            except Exception as exception:
                messages.error(request, exception)
                staging_filelist = []
            finally:
                subtemplates_list = [
                    {
                        'name': 'main/generic_multiform_subtemplate.html',
                        'context': {
                            'forms': [upload_form, document_form],
                            'title': title,
                        }
                    },
                    {
                        'name': 'main/generic_list_subtemplate.html',
                        'context': {
                            'title': _(u'Files in staging path'),
                            'object_list': staging_filelist,
                            'hide_link': True,
                        }
                    },
                ]
        else:
            subtemplates_list.append({
                'name': 'main/generic_multiform_subtemplate.html',
                'context': {
                    'forms': [upload_form, document_form],
                    'title': title,
                    'is_multipart': True
                },
            })

    context.update({
        'document_type_id': document_type.pk,
        'subtemplates_list': subtemplates_list,
        'temporary_navigation_links': {
            'form_header': {
                'sources:upload_version': {
                    'links': results['tab_links']
                },
                'sources:upload_interactive': {
                    'links': results['tab_links']
                }
            }
        },
    })

    context.update(
        {
            'sidebar_subtemplates_list': [
                {
                    'name': 'main/generic_subtemplate.html',
                    'context': {
                        'title': _(u'Current document type'),
                        'paragraphs': [document_type if document_type else _(u'None')],
                        'side_bar': True,
                    }
                },
                {
                    'name': 'main/generic_subtemplate.html',
                    'context': {
                        'title': _(u'Current metadata'),
                        'paragraphs': metadata_repr_as_list(decode_metadata_from_url(request.GET)),
                        'side_bar': True,
                    }
                }
            ],
        }
    )

    return render_to_response('main/generic_form.html', context,
                              context_instance=RequestContext(request))


def staging_file_delete(request, staging_folder_pk, encoded_filename):
    Permission.objects.check_permissions(request.user, [PERMISSION_DOCUMENT_CREATE, PERMISSION_DOCUMENT_NEW_VERSION])
    staging_folder = get_object_or_404(StagingFolderSource, pk=staging_folder_pk)

    staging_file = staging_folder.get_file(encoded_filename=encoded_filename)
    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))))
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))))

    if request.method == 'POST':
        try:
            staging_file.delete()
            messages.success(request, _(u'Staging file delete successfully.'))
        except Exception as exception:
            messages.error(request, _(u'Staging file delete error; %s.') % exception)
        return HttpResponseRedirect(next)

    results = get_active_tab_links()

    return render_to_response('main/generic_confirm.html', {
        'source': staging_folder,
        'delete_view': True,
        'object': staging_file,
        'next': next,
        'previous': previous,
        'form_icon': u'delete.png',
        'temporary_navigation_links': {'form_header': {'staging_file_delete': {'links': results['tab_links']}}},
    }, context_instance=RequestContext(request))


# Setup views
def setup_source_list(request):
    Permission.objects.check_permissions(request.user, [PERMISSION_SOURCES_SETUP_VIEW])

    context = {
        'object_list': Source.objects.select_subclasses(),
        'title': _('Sources'),
        'hide_link': True,
        'list_object_variable_name': 'source',
        'extra_columns': [
            {
                'name': _('Type'),
                'attribute': encapsulate(lambda x: x.class_fullname())
            },
        ]
    }

    return render_to_response('main/generic_list.html', context,
                              context_instance=RequestContext(request))


def setup_source_edit(request, source_id):
    Permission.objects.check_permissions(request.user, [PERMISSION_SOURCES_SETUP_EDIT])

    source = get_object_or_404(Source.objects.select_subclasses(), pk=source_id)
    form_class = get_form_class(source.source_type)

    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))))

    if request.method == 'POST':
        form = form_class(instance=source, data=request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, _(u'Source edited successfully'))
                return HttpResponseRedirect(next)
            except Exception as exception:
                messages.error(request, _(u'Error editing source; %s') % exception)
    else:
        form = form_class(instance=source)

    return render_to_response('main/generic_form.html', {
        'title': _(u'Edit source: %s') % source.fullname(),
        'form': form,
        'source': source,
        'navigation_object_name': 'source',
        'next': next,
        'object_name': _(u'Source'),
        'source_type': source.source_type,
    }, context_instance=RequestContext(request))


def setup_source_delete(request, source_id):
    Permission.objects.check_permissions(request.user, [PERMISSION_SOURCES_SETUP_DELETE])
    source = get_object_or_404(Source.objects.select_subclasses(), pk=source_id)
    redirect_view = reverse('sources:setup_source_list')

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', redirect_view)))

    if request.method == 'POST':
        try:
            source.delete()
            messages.success(request, _(u'Source "%s" deleted successfully.') % source)
        except Exception as exception:
            messages.error(request, _(u'Error deleting source "%(source)s": %(error)s') % {
                'source': source, 'error': exception
            })
        return HttpResponseRedirect(reverse(redirect_view))

    context = {
        'title': _(u'Are you sure you wish to delete the source: %s?') % source.fullname(),
        'source': source,
        'object_name': _(u'Source'),
        'navigation_object_name': 'source',
        'delete_view': True,
        'previous': previous,
        'source_type': source.source_type,
    }

    return render_to_response('main/generic_confirm.html', context,
                              context_instance=RequestContext(request))


def setup_source_create(request, source_type):
    Permission.objects.check_permissions(request.user, [PERMISSION_SOURCES_SETUP_CREATE])

    cls = get_class(source_type)
    form_class = get_form_class(source_type)

    if request.method == 'POST':
        form = form_class(data=request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, _(u'Source created successfully'))
                return HttpResponseRedirect(reverse('sources:setup_source_list'))
            except Exception as exception:
                messages.error(request, _(u'Error creating source; %s') % exception)
    else:
        form = form_class()

    return render_to_response('main/generic_form.html', {
        'title': _(u'Create new source of type: %s') % cls.class_fullname(),
        'form': form,
        'source_type': source_type,
        'navigation_object_name': 'source',
    }, context_instance=RequestContext(request))


def setup_source_transformation_list(request, source_id):
    Permission.objects.check_permissions(request.user, [PERMISSION_SOURCES_SETUP_EDIT])

    source = get_object_or_404(Source.objects.select_subclasses(), pk=source_id)

    context = {
        'object_list': SourceTransformation.transformations.get_for_object(source),
        'title': _(u'Transformations for: %s') % source.fullname(),
        'source': source,
        'object_name': _(u'Source'),
        'navigation_object_name': 'source',
        'list_object_variable_name': 'transformation',
        'extra_columns': [
            {'name': _(u'Order'), 'attribute': 'order'},
            {'name': _(u'Transformation'), 'attribute': encapsulate(lambda x: x.get_transformation_display())},
            {'name': _(u'Arguments'), 'attribute': 'arguments'}
        ],
        'hide_link': True,
        'hide_object': True,
    }

    return render_to_response('main/generic_list.html', context,
                              context_instance=RequestContext(request))


def setup_source_transformation_edit(request, transformation_id):
    Permission.objects.check_permissions(request.user, [PERMISSION_SOURCES_SETUP_EDIT])

    source_transformation = get_object_or_404(SourceTransformation, pk=transformation_id)
    redirect_view = reverse('sources:setup_source_transformation_list', args=[source_transformation.content_object.pk])
    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', redirect_view)))

    if request.method == 'POST':
        form = SourceTransformationForm(instance=source_transformation, data=request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, _(u'Source transformation edited successfully'))
                return HttpResponseRedirect(next)
            except Exception as exception:
                messages.error(request, _(u'Error editing source transformation; %s') % exception)
    else:
        form = SourceTransformationForm(instance=source_transformation)

    return render_to_response('main/generic_form.html', {
        'title': _(u'Edit transformation: %s') % source_transformation,
        'form': form,
        'source': source_transformation.content_object,
        'transformation': source_transformation,
        'navigation_object_list': [
            {'object': 'source', 'name': _(u'Source')},
            {'object': 'transformation', 'name': _(u'Transformation')}
        ],
        'next': next,
    }, context_instance=RequestContext(request))


def setup_source_transformation_delete(request, transformation_id):
    Permission.objects.check_permissions(request.user, [PERMISSION_SOURCES_SETUP_EDIT])

    source_transformation = get_object_or_404(SourceTransformation, pk=transformation_id)
    redirect_view = reverse('sources:setup_source_transformation_list', args=[source_transformation.content_object.pk])
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', redirect_view)))

    if request.method == 'POST':
        try:
            source_transformation.delete()
            messages.success(request, _(u'Source transformation deleted successfully.'))
        except Exception as exception:
            messages.error(request, _(u'Error deleting source transformation; %(error)s') % {
                'error': exception}
            )
        return HttpResponseRedirect(redirect_view)

    return render_to_response('main/generic_confirm.html', {
        'delete_view': True,
        'transformation': source_transformation,
        'source': source_transformation.content_object,
        'navigation_object_list': [
            {'object': 'source', 'name': _(u'Source')},
            {'object': 'transformation', 'name': _(u'Transformation')}
        ],
        'title': _(u'Are you sure you wish to delete source transformation "%(transformation)s"') % {
            'transformation': source_transformation.get_transformation_display(),
        },
        'previous': previous,
        'form_icon': u'shape_square_delete.png',
    }, context_instance=RequestContext(request))


def setup_source_transformation_create(request, source_id):
    Permission.objects.check_permissions(request.user, [PERMISSION_SOURCES_SETUP_EDIT])

    source = get_object_or_404(Source.objects.select_subclasses(), pk=source_id)

    redirect_view = reverse('sources:setup_source_transformation_list', args=[source.pk])

    if request.method == 'POST':
        form = SourceTransformationForm_create(request.POST)
        if form.is_valid():
            try:
                source_tranformation = form.save(commit=False)
                source_tranformation.content_object = source
                source_tranformation.save()
                messages.success(request, _(u'Source transformation created successfully'))
                return HttpResponseRedirect(redirect_view)
            except Exception as exception:
                messages.error(request, _(u'Error creating source transformation; %s') % exception)
    else:
        form = SourceTransformationForm_create()

    return render_to_response('main/generic_form.html', {
        'form': form,
        'source': source,
        'object_name': _(u'Source'),
        'navigation_object_name': 'source',
        'title': _(u'Create new transformation for source: %s') % source,
    }, context_instance=RequestContext(request))
