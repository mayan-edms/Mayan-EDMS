from urllib import unquote_plus

from django.utils.translation import ugettext as _
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.contrib import messages
from django.views.generic.list_detail import object_detail, object_list
from django.core.urlresolvers import reverse
from django.views.generic.create_update import create_object, delete_object, update_object
from django.forms.formsets import formset_factory
from django.core.files.base import File
from django.conf import settings
from django.utils.http import urlencode


from filetransfers.api import serve_file
from converter.api import convert, in_cache
from common.utils import pretty_size

from utils import from_descriptor_to_tempfile

from models import Document, DocumentMetadata, DocumentType, MetadataType
from forms import DocumentTypeSelectForm, DocumentCreateWizard, \
        MetadataForm, DocumentForm, DocumentForm_edit, DocumentForm_view, \
        StagingDocumentForm, DocumentTypeMetadataType
    
from staging import StagingFile

from documents.conf.settings import DELETE_STAGING_FILE_AFTER_UPLOAD
from documents.conf.settings import USE_STAGING_DIRECTORY
from documents.conf.settings import FILESYSTEM_FILESERVING_ENABLE
from documents.conf.settings import STAGING_FILES_PREVIEW_SIZE
from documents.conf.settings import PREVIEW_SIZE
from documents.conf.settings import THUMBNAIL_SIZE

def document_list(request):
    return object_list(
        request,
        queryset=Document.objects.all(),
        template_name='generic_list.html',
        extra_context={
            'title':_(u'documents'),
        },
    )

def document_create(request, multiple=True):
    MetadataFormSet = formset_factory(MetadataForm, extra=0)
    wizard = DocumentCreateWizard(form_list=[DocumentTypeSelectForm, MetadataFormSet], multiple=multiple)
    return wizard(request)

def document_create_sibling(request, document_id, multiple=True):
    document = get_object_or_404(Document, pk=document_id)
    urldata = []
    for id, metadata in enumerate(document.documentmetadata_set.all()):
        if hasattr(metadata, 'value'):
            urldata.append(('metadata%s_id' % id,metadata.metadata_type.id))   
            urldata.append(('metadata%s_value' % id,metadata.value))
        
    if multiple:
        view = 'upload_multiple_documents_with_type'
    else:
        view = 'upload_document_with_type'
    
    url = reverse(view, args=[document.document_type.id])
    return HttpResponseRedirect('%s?%s' % (url, urlencode(urldata)))


def _decode_metadata_from_url(url_dict):
    metadata_dict = {
        'id':{},
        'value':{}
    }
    metadata_list = []
    #Match out of order metadata_type ids with metadata values from request
    for key, value in url_dict.items():
        if 'metadata' in key:
            index, element = key[8:].split('_')
            metadata_dict[element][index] = value
        
    #Convert the nested dictionary into a list of id+values dictionaries
    for order, id in metadata_dict['id'].items():
        if order in metadata_dict['value'].keys():
            metadata_list.append({'id':id, 'value':metadata_dict['value'][order]})

    return metadata_list
    
    
def _save_metadata_list(metadata_list, document):
    for item in metadata_list:
        _save_metadata(item, document)
        
        
def _save_metadata(metadata_dict, document):
    #Use matched metadata now to create document metadata
    #for key, value in zip(metadata_dict['id'].values(), metadata_dict['value'].values()):
    document_metadata, created = DocumentMetadata.objects.get_or_create(
        document=document,
        metadata_type=get_object_or_404(MetadataType, pk=metadata_dict['id']),
    )
    #Handle 'plus sign as space' in the url
    document_metadata.value=unquote_plus(metadata_dict['value'])
    document_metadata.save()


def upload_document_with_type(request, document_type_id, multiple=True):
    document_type = get_object_or_404(DocumentType, pk=document_type_id)
    local_form = DocumentForm(prefix='local', initial={'document_type':document_type})
    if USE_STAGING_DIRECTORY:
        staging_form = StagingDocumentForm(prefix='staging', 
            initial={'document_type':document_type})
    
    if request.method == 'POST':
        if 'local-submit' in request.POST.keys():
            local_form = DocumentForm(request.POST, request.FILES,
                prefix='local', initial={'document_type':document_type})
            if local_form.is_valid():
                instance = local_form.save()
                if 'document_type_available_filenames' in local_form.cleaned_data:
                    if local_form.cleaned_data['document_type_available_filenames']:
                        instance.file_filename = local_form.cleaned_data['document_type_available_filenames'].filename
                        instance.save()
            
                _save_metadata_list(_decode_metadata_from_url(request.GET), instance)
                messages.success(request, _(u'Document uploaded successfully.'))
                try:
                    instance.create_fs_links()
                except Exception, e:
                    messages.error(request, e)
                    
                if multiple:
                    return HttpResponseRedirect(request.get_full_path())
                else:
                    return HttpResponseRedirect(reverse('document_list'))
        elif 'staging-submit' in request.POST.keys() and USE_STAGING_DIRECTORY:
            staging_form = StagingDocumentForm(request.POST, request.FILES,
                prefix='staging', initial={'document_type':document_type})
            if staging_form.is_valid():
                staging_file_id = staging_form.cleaned_data['staging_file_id']
                
                try:
                    staging_file = StagingFile.get(staging_file_id)
                except Exception, e:
                    messages.error(request, e)   
                else:
                    try:
                        document = Document(file=staging_file.upload(), document_type=document_type)
                        document.save()
                    except Exception, e:
                        messages.error(request, e)   
                    else:
                        
                        if 'document_type_available_filenames' in staging_form.cleaned_data:
                            if staging_form.cleaned_data['document_type_available_filenames']:
                                document.file_filename = staging_form.cleaned_data['document_type_available_filenames'].filename
                                document.save()
                                                
                        _save_metadata_list(_decode_metadata_from_url(request.GET), document)
                        messages.success(request, _(u'Staging file: %s, uploaded successfully.') % staging_file.filename)
                        try:
                            document.create_fs_links()
                        except Exception, e:
                            messages.error(request, e)
                
                        if DELETE_STAGING_FILE_AFTER_UPLOAD:
                            try:
                                staging_file.delete()
                                messages.success(request, _(u'Staging file: %s, deleted successfully.') % staging_file.filename)
                            except Exception, e:
                                messages.error(request, e)

            if multiple:
                return HttpResponseRedirect(request.META['HTTP_REFERER'])
            else:
                return HttpResponseRedirect(reverse('document_list'))                


    context = {
        'document_type_id':document_type_id,
        'form_list':[
            {
                'form':local_form,
                'title':_(u'upload a local document')
            },
        ],
    }
    
    if USE_STAGING_DIRECTORY:
        try:
            filelist = StagingFile.get_all()
        except Exception, e:
            messages.error(request, e)
            filelist = []
        finally:
            context.update({
                'subtemplates_dict':[
                    {
                        'name':'generic_list_subtemplate.html',
                        'title':_(u'files in staging'),
                        'object_list':filelist,
                        'hide_link':True,
                    },
                ],
            })
            context['form_list'].append(
                {
                    'form':staging_form,
                    'title':_(u'upload a document from staging'),
                },
            )
    
    return render_to_response('generic_form.html', context,
        context_instance=RequestContext(request))
        
        
def document_view(request, document_id):
    document = get_object_or_404(Document, pk=document_id)
    form = DocumentForm_view(instance=document, extra_fields=[
        {'label':_(u'Filename'), 'field':'file_filename'},
        {'label':_(u'File extension'), 'field':'file_extension'},
        {'label':_(u'File mimetype'), 'field':'file_mimetype'},
        {'label':_(u'File size'), 'field':lambda x: pretty_size(x.file.storage.size(x.file.path)) if x.exists() else '-'},
        {'label':_(u'Exists in storage'), 'field':'exists'},
        {'label':_(u'Date added'), 'field':lambda x: x.date_added.date()},
        {'label':_(u'Time added'), 'field':lambda x: unicode(x.date_added.time()).split('.')[0]},
        {'label':_(u'Checksum'), 'field':'checksum'},
        {'label':_(u'UUID'), 'field':'uuid'},
    ])
    
    subtemplates_dict = [
            {
                'name':'generic_list_subtemplate.html',
                'title':_(u'metadata'),
                'object_list':document.documentmetadata_set.all(),
                'extra_columns':[{'name':_(u'value'), 'attribute':'value'}],
                'hide_link':True,
            },
        ]
    
    if FILESYSTEM_FILESERVING_ENABLE:
        subtemplates_dict.append({
            'name':'generic_list_subtemplate.html',
            'title':_(u'index links'),
            'object_list':document.documentmetadataindex_set.all(),
            'hide_link':True})
    
    return render_to_response('generic_detail.html', {
        'form':form,
        'object':document,
        'subtemplates_dict':subtemplates_dict,
    }, context_instance=RequestContext(request))


def document_delete(request, document_id):
    document = get_object_or_404(Document, pk=document_id)
        
    return delete_object(request, model=Document, object_id=document_id, 
        template_name='generic_confirm.html', 
        post_delete_redirect=reverse('document_list'),
        extra_context={
            'delete_view':True,
            'object':document,
            'object_name':_(u'document'),
        })
        
        
def document_edit(request, document_id):
    document = get_object_or_404(Document, pk=document_id)
    if request.method == 'POST':
        form = DocumentForm_edit(request.POST, initial={'document_type':document.document_type})
        if form.is_valid():
            try:
                document.delete_fs_links()
            except Exception, e:
                messages.error(request, e)
                return HttpResponseRedirect(reverse('document_list'))

            document.file_filename = form.cleaned_data['new_filename']

            if 'document_type_available_filenames' in form.cleaned_data:
                if form.cleaned_data['document_type_available_filenames']:
                    document.file_filename = form.cleaned_data['document_type_available_filenames'].filename
                
            document.save()
            
            messages.success(request, _(u'Document:%s edited successfully.') % document)
            
            try:
                document.create_fs_links()
                messages.success(request, _(u'Document filesystem links updated successfully.'))                
            except Exception, e:
                messages.error(request, e)
                return HttpResponseRedirect(reverse('document_list'))
                
            return HttpResponseRedirect(reverse('document_list'))
    else:
        form = DocumentForm_edit(instance=document, initial={
            'new_filename':document.file_filename, 'document_type':document.document_type})

    return render_to_response('generic_form.html', {
        'form':form,
        'object':document,
    
    }, context_instance=RequestContext(request))


def document_edit_metadata(request, document_id):
    document = get_object_or_404(Document, pk=document_id)
    MetadataFormSet = formset_factory(MetadataForm, extra=0)

    initial=[]
    for item in DocumentTypeMetadataType.objects.filter(document_type=document.document_type):
        initial.append({
            'metadata_type':item.metadata_type,
            'document_type':document.document_type,
            'value':document.documentmetadata_set.get(metadata_type=item.metadata_type).value if document.documentmetadata_set.filter(metadata_type=item.metadata_type) else None
        })
    #for metadata in document.documentmetadata_set.all():
    #    initial.append({
    #        'metadata_type':metadata.metadata_type,
    #        'document_type':document.document_type,
    #        'value':metadata.value,
    #    })    

    formset = MetadataFormSet(initial=initial)
    if request.method == 'POST':
        formset = MetadataFormSet(request.POST)
        if formset.is_valid():
            _save_metadata_list(formset.cleaned_data, document)
            #for item in formset.cleaned_data:
            #    _save_metadata(item, document)
            try:
                document.delete_fs_links()
            except Exception, e:
                messages.error(request, e)
                return HttpResponseRedirect(reverse('document_list'))
           
            messages.success(request, _(u'Document metadata edited successfully.'))
            
            try:
                document.create_fs_links()
                messages.success(request, _(u'Document filesystem links updated successfully.'))                
            except Exception, e:
                messages.error(request, e)
                return HttpResponseRedirect(reverse('document_list'))
                
            return HttpResponseRedirect(reverse('document_list'))
        
        
    return render_to_response('generic_form.html', {
        'form_display_mode_table':True,
        'form':formset,
        'object':document,
    
    }, context_instance=RequestContext(request))
    

def get_document_image(request, document_id, size=PREVIEW_SIZE):
    document = get_object_or_404(Document, pk=document_id)
    
    filepath = in_cache(document.uuid, size)
   
    if filepath:
        return serve_file(request, File(file=open(filepath, 'r')))
    else:
        try:
            document.file.open()
            desc = document.file.storage.open(document.file.path)
            filepath = from_descriptor_to_tempfile(desc, document.uuid)
            output_file = convert(filepath, size)
            return serve_file(request, File(file=open(output_file, 'r')))
        except Exception, e:
            if size == THUMBNAIL_SIZE:
                return serve_file(request, File(file=open('%simages/picture_error.png' % settings.MEDIA_ROOT, 'r')))
            else:
                return serve_file(request, File(file=open('%simages/1297211435_error.png' % settings.MEDIA_ROOT, 'r')))
            #messages.error(request, e)
            #return HttpResponse(e)


def document_thumbnail(request, document_id):
    return get_document_image(request, document_id, THUMBNAIL_SIZE)


def document_preview(request, document_id):
    return get_document_image(request, document_id, PREVIEW_SIZE)
        
        
def document_download(request, document_id):
    document = get_object_or_404(Document, pk=document_id)
    try:
        #Test permissions and trigger exception
        document.file.open()
        return serve_file(request, document.file, save_as=document.get_fullname())
    except Exception, e:
        messages.error(request, e)
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


def staging_file_preview(request, staging_file_id):
    try:
        filepath = StagingFile.get(staging_file_id).filepath
        output_file = convert(filepath, STAGING_FILES_PREVIEW_SIZE)
        return serve_file(request, File(file=open(output_file, 'r')))
    except Exception, e:
        return serve_file(request, File(file=open('%simages/1297211435_error.png' % settings.MEDIA_ROOT, 'r')))        
     
