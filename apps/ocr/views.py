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

from ocr import OCR_DOCUMENT_OCR
from api import ocr_document

def submit_document(request, document_id):
    permissions = [OCR_DOCUMENT_OCR]
    try:
        check_permissions(request.user, 'ocr', permissions)
    except Unauthorized, e:
        raise Http404(e)
        
    document = get_object_or_404(Document, pk=document_id)
    
    try:
        result = ocr_document(document)
    except Exception, e:
        messages.error(request, e)
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
   
    messages.success(request, _(u'Document OCR was successful.'))
    return HttpResponseRedirect(request.META['HTTP_REFERER'])    
