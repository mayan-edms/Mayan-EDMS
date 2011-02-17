from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.contrib import messages
from django.views.generic.list_detail import object_detail, object_list
from django.core.urlresolvers import reverse
#from django.views.generic.create_update import create_object, delete_object, update_object
from django.conf import settings
from django.utils.translation import ugettext as _

from permissions.api import check_permissions, Unauthorized
from documents.models import Document

from ocr import PERMISSION_OCR_DOCUMENT

from models import DocumentQueue, QueueDocument

from tasks import do_document_ocr_task

def submit_document(request, document_id, queue_name='default'):
    permissions = [PERMISSION_OCR_DOCUMENT]
    try:
        check_permissions(request.user, 'ocr', permissions)
    except Unauthorized, e:
        raise Http404(e)
        
    document = get_object_or_404(Document, pk=document_id)
    
    document_queue = get_object_or_404(DocumentQueue, name=queue_name)
    do_document_ocr_task.delay(document.id)
    ##document_queue.add_document(document)
    #queue_document = QueueDocument(document_queue=document_queue, document=document)
    #queue_document.save()


    #add.delay(1,2)

    messages.success(request, _(u'Document: %s was added to the OCR queue: %s.') % (document, document_queue.label))
    return HttpResponseRedirect(request.META['HTTP_REFERER'])    
