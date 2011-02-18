from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.contrib import messages
from django.views.generic.list_detail import object_detail, object_list
from django.core.urlresolvers import reverse
from django.views.generic.create_update import create_object, delete_object, update_object
from django.conf import settings
from django.utils.translation import ugettext as _

from permissions.api import check_permissions, Unauthorized
from documents.models import Document

from ocr import PERMISSION_OCR_DOCUMENT, PERMISSION_OCR_DOCUMENT_DELETE

from models import DocumentQueue, QueueDocument, add_document_to_queue

from tasks import do_document_ocr_task


def queue_document_list(request, queue_name='default'):
    permissions = [PERMISSION_OCR_DOCUMENT]
    try:
        check_permissions(request.user, 'ocr', permissions)
    except Unauthorized, e:
        raise Http404(e)
        
    document_queue = get_object_or_404(DocumentQueue, name=queue_name)
            
    return object_list(
        request,
        queryset=document_queue.queuedocument_set.all(),
        template_name='generic_list.html',
        extra_context={
            'title':_(u'queued documents'),
            'hide_object':True,
            'extra_columns':[
                {'name':'document', 'attribute': 'document'},
                {'name':'submitted', 'attribute': lambda x: unicode(x.datetime_submitted).split('.')[0]},
                {'name':'state', 'attribute': lambda x: x.get_state_display()},
                {'name':'result', 'attribute':'result'},
            ],
        },
    )    
        
        
def queue_document_delete(request, queue_document_id):
    permissions = [PERMISSION_OCR_DOCUMENT_DELETE]
    try:
        check_permissions(request.user, 'ocr', permissions)
    except Unauthorized, e:
        raise Http404(e)
            
    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', None)))
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', None)))
        
    return delete_object(request, model=QueueDocument, object_id=queue_document_id, 
        template_name='generic_confirm.html', 
        post_delete_redirect=reverse('queue_document_list'),
        extra_context={
            'delete_view':True,
            'next':next,
            'previous':previous,
            'object_name':_(u'queued document'),
        })
    


def submit_document(request, document_id, queue_name='default'):
    permissions = [PERMISSION_OCR_DOCUMENT]
    try:
        check_permissions(request.user, 'ocr', permissions)
    except Unauthorized, e:
        raise Http404(e)
        
    document = get_object_or_404(Document, pk=document_id)
    
    document_queue = get_object_or_404(DocumentQueue, name=queue_name)
    add_document_to_queue(document, document_queue.name)

    messages.success(request, _(u'Document: %(document)s was added to the OCR queue: %(queue)s.') % {
        'document':document, 'queue':document_queue.label})
    return HttpResponseRedirect(request.META['HTTP_REFERER'])    
