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
from tags.models import TagProperties
from tags import PERMISSION_TAG_CREATE, PERMISSION_TAG_ATTACH, \
    PERMISSION_TAG_DELETE
    

def tag_remove(request, tag_id, document_id):
    check_permissions(request.user, 'tags', [PERMISSION_TAG_DELETE])

    tag = get_object_or_404(Tag, pk=tag_id)
    document = get_object_or_404(Document, pk=document_id)

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', None)))
    tag.delete()
    messages.success(request, _(u'Tag "%s" removed successfully.') % tag)
    
    return HttpResponseRedirect(previous)


def tag_add(request, document_id):
    document = get_object_or_404(Document, pk=document_id)

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', None)))
    
    if request.method == 'POST':
        previous = request.META.get('HTTP_REFERER', '/')
        form = AddTagForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['new_tag']:
                check_permissions(request.user, 'tags', [PERMISSION_TAG_CREATE])
                tag_name = form.cleaned_data['new_tag']
                if Tag.objects.filter(name=tag_name):
                    is_new = False
                else:
                    is_new = True
            elif form.cleaned_data['existing_tags']:
                check_permissions(request.user, 'tags', [PERMISSION_TAG_ATTACH])
                tag_name = form.cleaned_data['existing_tags']
                is_new = False
            else:
                messages.error(request, _(u'Must choose either a new tag or an existing one.'))
                return HttpResponseRedirect(previous)
                    
            if tag_name in document.tags.values_list('name', flat=True):
                messages.warning(request, _(u'Document is already tagged as "%s"') % tag_name)
                return HttpResponseRedirect(previous)
            
            document.tags.add(tag_name)
            
            if is_new:
                tag = Tag.objects.get(name=tag_name)
                TagProperties(tag=tag, color=form.cleaned_data['color']).save()
                
            messages.success(request, _(u'Tag "%s" added successfully.') % tag_name)
    
    return HttpResponseRedirect(previous)


def tag_list(request):
    
    return render_to_response('generic_list.html', {
        'object_list': Tag.objects.all(),
        'title': _(u'tags'),
        'hide_link': True,
    }, context_instance=RequestContext(request))
