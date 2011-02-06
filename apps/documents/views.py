from django.utils.translation import ugettext as _
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.contrib import messages
from django.views.generic.list_detail import object_detail, object_list
from django.core.urlresolvers import reverse
from django.views.generic.create_update import create_object, delete_object, update_object
from django.forms.formsets import formset_factory

from models import Document, DocumentMetadata, DocumentType, MetadataType
from forms import DocumentTypeSelectForm, DocumentCreateWizard, \
        MetadataForm, DocumentForm, DocumentForm_edit, DocumentForm_view
    
from staging import StagingFile

def document_list(request):
    return object_list(
        request,
        queryset=Document.objects.all(),
        template_name='generic_list.html',
        extra_context={
            'title':_(u'documents'),
            'extra_columns':[
                {'name':_(u'filename'), 'attribute':'file_filename'},
                {'name':_(u'extension'), 'attribute':'file_extension'},
                {'name':_(u'mimetype'), 'attribute':'file_mimetype'},
                {'name':_(u'added'), 'attribute':'date_added'},
            ],
        },
    )


def document_create(request, multiple=True):
    MetadataFormSet = formset_factory(MetadataForm, extra=0)
    wizard = DocumentCreateWizard(form_list=[DocumentTypeSelectForm, MetadataFormSet], multiple=multiple)
    return wizard(request)


def _save_metadata_from_request(request, document):
    metadata_dict = {
        'id':{},
        'value':{}
    }
    #Match out of order metadata_type ids with metadata values from request
    for key, value in request.GET.items():
        if 'metadata' in key:
            index, element = key[8:].split('_')
            metadata_dict[element][index] = value
            
    #Use matched metadata now to create document metadata
    for key, value in zip(metadata_dict['id'].values(), metadata_dict['value'].values()):
        document_metadata = DocumentMetadata(
            document=document,
            metadata_type=get_object_or_404(MetadataType, pk=key),
            value=value
        )
        document_metadata.save()
        

def upload_document_with_type(request, document_type_id, multiple=True):
    document_type = get_object_or_404(DocumentType, pk=document_type_id)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, initial={'document_type':document_type})
        if form.is_valid():
            instance = form.save()
            if 'new_filename' in form.cleaned_data:
                if form.cleaned_data['new_filename']:
                    instance.file_filename = form.cleaned_data['new_filename'].filename
                    instance.save()
        
            _save_metadata_from_request(request, instance)
            messages.success(request, _(u'Document uploaded successfully.'))
            try:
                instance.create_fs_links()
            except Exception, e:
                messages.error(request, e)
                
            if multiple:
                return HttpResponseRedirect(request.get_full_path())
            else:
                return HttpResponseRedirect(reverse('document_list'))
    else:
        form = DocumentForm(initial={'document_type':document_type})

    filelist = StagingFile.get_all()
    
    return render_to_response('generic_form.html', {
        'form':form,
        'title':_(u'upload a local document'),
        'document_type_id':document_type_id,
        'subtemplates_dict':[
            {
            'name':'generic_list_subtemplate.html',
            'title':_(u'files in staging'),
            'object_list':filelist,
            },
        ],

    }, context_instance=RequestContext(request))
        
        
def document_view(request, document_id):
    document = get_object_or_404(Document, pk=document_id)
    form = DocumentForm_view(instance=document, extra_fields=[
        {'label':_(u'Filename'), 'field':'file_filename'},
        {'label':_(u'File extension'), 'field':'file_extension'},
        {'label':_(u'File mimetype'), 'field':'file_mimetype'},
        {'label':_(u'Date added'), 'field':'date_added'},
        {'label':_(u'Checksum'), 'field':'checksum'},
        {'label':_(u'UUID'), 'field':'uuid'}
    ])
    
    return render_to_response('generic_detail.html', {
        'form':form,
        'object':document,
        'subtemplates_dict':[
            {
                'name':'generic_list_subtemplate.html',
                'title':_(u'metadata'),
                'object_list':document.documentmetadata_set.all(),
                'extra_columns':[{'name':_(u'qty'), 'attribute':'value'}],
                'hide_link':True,
            },
        ],  
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
        form = DocumentForm_edit(request.POST)
        if form.is_valid():
            try:
                document.delete_fs_links()
            except Exception, e:
                messages.error(request, e)
                return HttpResponseRedirect(reverse('document_list'))
                
            document.file_filename = form.cleaned_data['new_filename']
            document.save()
            
            try:
                document.create_fs_links()
            except Exception, e:
                messages.error(request, e)
                return HttpResponseRedirect(reverse('document_list'))
                
            messages.success(request, _(u'Document edited and filesystem links updated.'))
            return HttpResponseRedirect(reverse('document_list'))
    else:
        form = DocumentForm_edit(instance=document, initial={'new_filename':document.file_filename})

    return render_to_response('generic_form.html', {
        'form':form,
        'object':document,
    
    }, context_instance=RequestContext(request))


def document_create_from_staging(request, file_id, document_type_id, multiple=True):
    document_type = get_object_or_404(DocumentType, pk=document_type_id)
    staging_file = StagingFile.get(id=int(file_id))

    document = Document(file=staging_file.upload(), document_type=document_type)
    document.save()

    #TODO: need to grab url query string from HTTP_REFERER
    _save_metadata_from_request(request, document)
    messages.success(request, _(u'Staging file: %s, uploaded successfully.') % staging_file.filename)
    try:
        document.create_fs_links()
    except Exception, e:
        messages.error(request, e)   
    
    if multiple:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:
        return HttpResponseRedirect(reverse('document_list'))
