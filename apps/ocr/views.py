import datetime

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

from ocr import PERMISSION_OCR_DOCUMENT, PERMISSION_OCR_DOCUMENT_DELETE, \
    PERMISSION_OCR_QUEUE_ENABLE_DISABLE
from models import DocumentQueue, QueueDocument, add_document_to_queue
from tasks import do_document_ocr_task
from literals import QUEUEDOCUMENT_STATE_PENDING, \
    QUEUEDOCUMENT_STATE_PROCESSING, QUEUEDOCUMENT_STATE_ERROR, \
    DOCUMENTQUEUE_STATE_STOPPED, DOCUMENTQUEUE_STATE_ACTIVE
from forms import DocumentQueueForm_view

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
            'title':_(u'documents in queue: %s') % document_queue,
            'hide_object':True,
            'object':document_queue,
            'object_name':_(u'document queue'),
            'extra_columns':[
                {'name':'document', 'attribute': lambda x: '<a href="%s">%s</a>' % (x.document.get_absolute_url(), x.document) if hasattr(x, 'document') else _(u'Missing document.')},
                {'name':'submitted', 'attribute': lambda x: unicode(x.datetime_submitted).split('.')[0], 'keep_together':True},
                {'name':'state', 'attribute': lambda x: x.get_state_display()},
                {'name':'result', 'attribute':'result'},
            ],
            'sidebar_subtemplates_list':[
                {
                    'title':_(u'document queue properties'),
                    'name':'generic_detail_subtemplate.html',
                    'form':DocumentQueueForm_view(instance=document_queue),
                }],
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


def re_queue_document(request, queue_document_id):
    permissions = [PERMISSION_OCR_DOCUMENT]
    try:
        check_permissions(request.user, 'ocr', permissions)
    except Unauthorized, e:
        raise Http404(e)
            
    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', None)))
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', None)))
    queue_document = get_object_or_404(QueueDocument, pk=queue_document_id)

    try:
        queue_document.document
    except Document.DoesNotExist:
        messages.error(request, _(u'This document no longer exists.'))
        return HttpResponseRedirect(previous)

    if queue_document.state == QUEUEDOCUMENT_STATE_PENDING:
        messages.warning(request, _(u'This document is already queued and pending processing.'))
        return HttpResponseRedirect(previous)
    elif queue_document.state == QUEUEDOCUMENT_STATE_PROCESSING:
        messages.warning(request, _(u'This document is already being processed and can\'t be re-queded.'))
        return HttpResponseRedirect(previous)

    if request.method == 'POST':
        try:
            if queue_document.state == QUEUEDOCUMENT_STATE_ERROR:
                queue_document.datetime_submitted = datetime.datetime.now()
                queue_document.state = QUEUEDOCUMENT_STATE_PENDING
                queue_document.save()
                messages.success(request, _(u'Document: %(document)s was re-queued to the OCR queue: %(queue)s') % {
                    'document':queue_document.document, 'queue':queue_document.document_queue.label})

        except Exception, e:
            messages.error(request, e)
        return HttpResponseRedirect(next)

    
        
    return render_to_response('generic_confirm.html', {
        'object':queue_document,
        'title':_(u'Are you sure you wish to re-queue document: %s') % queue_document,
        'next':next,
        'previous':previous,
    }, context_instance=RequestContext(request))


def document_queue_disable(request, document_queue_id):
    permissions = [PERMISSION_OCR_QUEUE_ENABLE_DISABLE]
    try:
        check_permissions(request.user, 'ocr', permissions)
    except Unauthorized, e:
        raise Http404(e)

    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', None)))
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', None)))    
    document_queue = get_object_or_404(DocumentQueue, pk=document_queue_id)
    
    if document_queue.state == DOCUMENTQUEUE_STATE_STOPPED:
        messages.warning(request, _(u'Document queue: %s, already stopped.') % document_queue)
        return HttpResponseRedirect(previous)

    if request.method == 'POST':
        document_queue.state = DOCUMENTQUEUE_STATE_STOPPED
        document_queue.save()
        messages.success(request, _(u'Document queue: %s, stopped successfully.') % document_queue)
        return HttpResponseRedirect(next)
    
    return render_to_response('generic_confirm.html', {
        'object':document_queue,
        'title':_(u'Are you sure you wish to disable document queue: %s') % document_queue,
        'next':next,
        'previous':previous,
    }, context_instance=RequestContext(request))    
    

def document_queue_enable(request, document_queue_id):
    permissions = [PERMISSION_OCR_QUEUE_ENABLE_DISABLE]
    try:
        check_permissions(request.user, 'ocr', permissions)
    except Unauthorized, e:
        raise Http404(e)

    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', None)))
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', None)))    
    document_queue = get_object_or_404(DocumentQueue, pk=document_queue_id)
    
    if document_queue.state == DOCUMENTQUEUE_STATE_ACTIVE:
        messages.warning(request, _(u'Document queue: %s, already active.') % document_queue)
        return HttpResponseRedirect(previous)

    if request.method == 'POST':
        document_queue.state = DOCUMENTQUEUE_STATE_ACTIVE
        document_queue.save()
        messages.success(request, _(u'Document queue: %s, activated successfully.') % document_queue)
        return HttpResponseRedirect(next)
    
    return render_to_response('generic_confirm.html', {
        'object':document_queue,
        'title':_(u'Are you sure you wish to activate document queue: %s') % document_queue,
        'next':next,
        'previous':previous,
    }, context_instance=RequestContext(request))        
