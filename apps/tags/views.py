from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from permissions.api import check_permissions

from taggit.models import Tag
from documents.models import Document

from tags.forms import AddTagForm


def tag_remove(request, tag_id, document_id):
#    check_permissions(request.user, 'ocr', [PERMISSION_OCR_DOCUMENT])

    tag = get_object_or_404(Tag, pk=tag_id)
    document = get_object_or_404(Document, pk=document_id)

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', None)))
    tag.delete()
    messages.success(request, _(u'Tag: %s, removed successfully.') % tag)
    
    return HttpResponseRedirect(previous)


def tag_add(request, document_id):
#    check_permissions(request.user, 'ocr', [PERMISSION_OCR_DOCUMENT])

    document = get_object_or_404(Document, pk=document_id)

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', None)))
    #document.tags.add(tag)
    #messages.success(request, _(u'Tag: %s, removed successfully.') % tag)
    #tag = get_object_or_404(Tag, pk=tag_id)
    
    #return HttpResponseRedirect(previous)
    
    
    if request.method == 'POST':
        previous = request.META.get('HTTP_REFERER', '/')
        form = AddTagForm(request.POST)#, user=request.user)
        if form.is_valid():
            if form.cleaned_data['existing_tags']:
                tag = form.cleaned_data['existing_tags']
            elif form.cleaned_data['name']:
                tag = form.cleaned_data['name']
            
            document.tags.add(tag)

    return HttpResponseRedirect(previous)
