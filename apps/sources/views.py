import os
import zipfile

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

from converter.exceptions import UnkownConvertError, UnknownFormat
from documents.literals import PICTURE_ERROR_SMALL, PICTURE_ERROR_MEDIUM, \
    PICTURE_UNKNOWN_SMALL, PICTURE_UNKNOWN_MEDIUM
from documents.literals import PERMISSION_DOCUMENT_CREATE
from documents.literals import HISTORY_DOCUMENT_CREATED
from documents.models import RecentDocument, Document, DocumentType
from document_indexing.api import update_indexes
from history.api import create_history
from metadata.api import save_metadata_list, \
    decode_metadata_from_url, metadata_repr_as_list
from permissions.api import check_permissions
import sendfile

from sources.models import WebForm, StagingFolder
from sources.models import SOURCE_CHOICE_WEB_FORM, SOURCE_CHOICE_STAGING
from sources.models import SOURCE_UNCOMPRESS_CHOICE_Y, \
    SOURCE_UNCOMPRESS_CHOICE_ASK
from sources.staging import create_staging_file_class
from sources.forms import StagingDocumentForm, WebFormForm


def upload_interactive(request, source_type=None, source_id=None):
    check_permissions(request.user, [PERMISSION_DOCUMENT_CREATE])

    subtemplates_list = []

    tab_links = []

    context = {}

    web_forms = WebForm.objects.filter(enabled=True)
    for web_form in web_forms:
        tab_links.append({
            'text': web_form.title,
            'view': 'upload_interactive',
            'args': [u'"%s"' % web_form.source_type, web_form.pk],
            'famfam': web_form.icon,
            'keep_query': True,
            'conditional_highlight': lambda context: context['source'].source_type == web_form.source_type and context['source'].pk == web_form.pk,
        })

    staging_folders = StagingFolder.objects.filter(enabled=True)
    for staging_folder in staging_folders:
        tab_links.append({
            'text': staging_folder.title,
            'view': 'upload_interactive',
            'args': [u'"%s"' % staging_folder.source_type, staging_folder.pk],
            'famfam': staging_folder.icon,
            'keep_query': True,
            'conditional_highlight': lambda context: context['source'].source_type == staging_folder.source_type and context['source'].pk == staging_folder.pk,
        })

    if web_forms.count() == 0 and staging_folders.count() == 0:
        subtemplates_list.append(
            {
                'name': 'generic_subtemplate.html',
                'context': {
                    'title': _(u'Upload sources'),
                    'paragraphs': [
                        _(u'Not document sources have been defined or there are no sources enabled.')
                        # TODO: Add link to setup
                    ],
                }
            })

    document_type_id = request.GET.get('document_type_id', None)
    if document_type_id:
        document_type = get_object_or_404(DocumentType, pk=document_type_id[0])
    else:
        document_type = None

    subtemplates_list = []

    if source_type is None and source_id is None:
        if web_forms.count():
            source_type = web_forms[0].source_type
            source_id = web_forms[0].pk
        elif staging_folders.count():
            source_type = staging_folders[0].source_type
            source_id = staging_folders[0].pk

    if source_type and source_id:
        if source_type == SOURCE_CHOICE_WEB_FORM:
            web_form = get_object_or_404(WebForm, pk=source_id)
            context['source'] = web_form
            if request.method == 'POST':
                form = WebFormForm(request.POST, request.FILES,
                    document_type=document_type,
                    show_expand=(web_form.uncompress == SOURCE_UNCOMPRESS_CHOICE_ASK)
                )
                if form.is_valid():
                    try:
                        if web_form.uncompress == SOURCE_UNCOMPRESS_CHOICE_ASK:
                            expand = form.cleaned_data['expand']
                        else:
                            if web_form.uncompress == SOURCE_UNCOMPRESS_CHOICE_Y:
                                expand = True
                            else:
                                expand = False
                        if (not expand) or (expand and not _handle_zip_file(request, request.FILES['file'], document_type)):
                            instance = form.save()
                            instance.save()
                            if document_type:
                                instance.document_type = document_type
                            _handle_save_document(request, instance, form)
                            messages.success(request, _(u'Document uploaded successfully.'))
                    except Exception, e:
                        messages.error(request, e)

                    return HttpResponseRedirect(request.get_full_path())

            form = WebFormForm(show_expand=(web_form.uncompress==SOURCE_UNCOMPRESS_CHOICE_ASK), document_type=document_type)

            subtemplates_list.append({
                'name': 'generic_form_subtemplate.html',
                'context': {
                    'form': form,
                    'title': _(u'upload a local document from source: %s') % web_form.title,
                },
            })
        elif source_type == SOURCE_CHOICE_STAGING:
            staging_folder = get_object_or_404(StagingFolder, pk=source_id)
            context['source'] = staging_folder
            StagingFile = create_staging_file_class(request, staging_folder.folder_path)
            if request.method == 'POST':
                form = StagingDocumentForm(request.POST, request.FILES,
                    cls=StagingFile, document_type=document_type,
                    show_expand=(staging_folder.uncompress==SOURCE_UNCOMPRESS_CHOICE_ASK)
                )
                if form.is_valid():
                    try:
                        staging_file = StagingFile.get(form.cleaned_data['staging_file_id'])
                        if staging_folder.uncompress == SOURCE_UNCOMPRESS_CHOICE_ASK:
                            expand = form.cleaned_data['expand']
                        else:
                            if staging_folder.uncompress == SOURCE_UNCOMPRESS_CHOICE_Y:
                                expand = True
                            else:
                                expand = False                        
                        if (not expand) or (expand and not _handle_zip_file(request, staging_file.upload(), document_type)):
                            document = Document(file=staging_file.upload())
                            if document_type:
                                document.document_type = document_type
                            document.save()
                            _handle_save_document(request, document, form)
                            messages.success(request, _(u'Staging file: %s, uploaded successfully.') % staging_file.filename)

                        if staging_folder.delete_after_upload:
                            staging_file.delete(staging_folder.get_preview_size())
                            messages.success(request, _(u'Staging file: %s, deleted successfully.') % staging_file.filename)
                    except Exception, e:
                        messages.error(request, e)

                    return HttpResponseRedirect(request.get_full_path())
                                    
            form = StagingDocumentForm(cls=StagingFile,
                document_type=document_type, 
                show_expand=(staging_folder.uncompress==SOURCE_UNCOMPRESS_CHOICE_ASK)
            )
            try:
                staging_filelist = StagingFile.get_all()
            except Exception, e:
                messages.error(request, e)
                staging_filelist = []
            finally:
                subtemplates_list = [
                    {
                        'name': 'generic_form_subtemplate.html',
                        'context': {
                            'form': form,
                            'title': _(u'upload a document from staging source: %s') % staging_folder.title,
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

    context.update({
        'document_type_id': document_type_id,
        'subtemplates_list': subtemplates_list,
        'sidebar_subtemplates_list': [
            {
                'name': 'generic_subtemplate.html',
                'context': {
                    'title': _(u'Current metadata'),
                    'paragraphs': metadata_repr_as_list(decode_metadata_from_url(request.GET)),
                    'side_bar': True,
                }
            }],
        'temporary_navigation_links': {'form_header': {'upload_interactive': {'links': tab_links}}}
    })
    return render_to_response('generic_form.html', context,
        context_instance=RequestContext(request))    


def _handle_save_document(request, document, form=None):
    RecentDocument.objects.add_document_for_user(request.user, document)
    
    if form:
        if form.cleaned_data['new_filename']:
            document.file_filename = form.cleaned_data['new_filename']
            document.save()

    if form and 'document_type_available_filenames' in form.cleaned_data:
        if form.cleaned_data['document_type_available_filenames']:
            document.file_filename = form.cleaned_data['document_type_available_filenames'].filename
            document.save()

    save_metadata_list(decode_metadata_from_url(request.GET), document, create=True)

    warnings = update_indexes(document)
    if request.user.is_staff or request.user.is_superuser:
        for warning in warnings:
            messages.warning(request, warning)

    create_history(HISTORY_DOCUMENT_CREATED, document, {'user': request.user})


def _handle_zip_file(request, uploaded_file, document_type=None):
    filename = getattr(uploaded_file, 'filename', getattr(uploaded_file, 'name', ''))
    if filename.lower().endswith('zip'):
        zfobj = zipfile.ZipFile(uploaded_file)
        for filename in zfobj.namelist():
            if not filename.endswith('/'):
                zip_document = Document(file=SimpleUploadedFile(
                    name=filename, content=zfobj.read(filename)))
                if document_type:
                    zip_document.document_type = document_type
                zip_document.save()
                _handle_save_document(request, zip_document)
                messages.success(request, _(u'Extracted file: %s, uploaded successfully.') % filename)
        #Signal that uploaded file was a zip file
        return True
    else:
        #Otherwise tell parent to handle file
        return False
        
        
def staging_file_preview(request, source_type, source_id, staging_file_id):
    check_permissions(request.user, [PERMISSION_DOCUMENT_CREATE])
    staging_folder = get_object_or_404(StagingFolder, pk=source_id)
    StagingFile = create_staging_file_class(request, staging_folder.folder_path)
    try:
        output_file, errors = StagingFile.get(staging_file_id).preview(staging_folder.get_preview_size())
        if errors and (request.user.is_staff or request.user.is_superuser):
            for error in errors:
                messages.warning(request, _(u'Staging file transformation error: %(error)s') % {
                    'error': error
                })

    except UnkownConvertError, e:
        if request.user.is_staff or request.user.is_superuser:
            messages.error(request, e)

        output_file = os.path.join(settings.MEDIA_ROOT, u'images', PICTURE_ERROR_MEDIUM)
    except UnknownFormat:
        output_file = os.path.join(settings.MEDIA_ROOT, u'images', PICTURE_UNKNOWN_MEDIUM)
    except Exception, e:
        if request.user.is_staff or request.user.is_superuser:
            messages.error(request, e)
        output_file = os.path.join(settings.MEDIA_ROOT, u'images', PICTURE_ERROR_MEDIUM)
    finally:
        return sendfile.sendfile(request, output_file)


def staging_file_delete(request, source_type, source_id, staging_file_id):
    check_permissions(request.user, [PERMISSION_DOCUMENT_CREATE])
    staging_folder = get_object_or_404(StagingFolder, pk=source_id)
    StagingFile = create_staging_file_class(request, staging_folder.folder_path)    

    staging_file = StagingFile.get(staging_file_id)
    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', None)))
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', None)))

    if request.method == 'POST':
        try:
            staging_file.delete(staging_folder.get_preview_size())
            messages.success(request, _(u'Staging file delete successfully.'))
        except Exception, e:
            messages.error(request, e)
        return HttpResponseRedirect(next)

    return render_to_response('generic_confirm.html', {
        'source': staging_folder,
        'delete_view': True,
        'object': staging_file,
        'next': next,
        'previous': previous,
        'form_icon': u'delete.png',
    }, context_instance=RequestContext(request))
