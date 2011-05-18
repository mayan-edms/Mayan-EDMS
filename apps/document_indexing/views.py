from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.safestring import mark_safe

from document_indexing.models import IndexInstance
from document_indexing.api import get_breadcrumbs, get_instance_link


def index_instance_list(request, index_id=None):
    #TODO: check_permissions
    #check_permissions(request.user, 'documents', [PERMISSION_DOCUMENT_VIEW])

    if index_id:
        index_instance = get_object_or_404(IndexInstance, pk=index_id)
        index_instance_list = [index for index in index_instance.get_children()]
        breadcrumbs = get_breadcrumbs(index_instance)
        if index_instance.documents.count():
            for document in index_instance.documents.all():
                index_instance_list.append(document)
    else:
        index_instance_list = IndexInstance.objects.filter(parent=None)
        breadcrumbs = get_instance_link()

    title = mark_safe(_(u'contents for index: %s') % breadcrumbs)
        
    return render_to_response('generic_list.html', {
        'object_list': index_instance_list,
        'title': title,
        'hide_links': True,
    }, context_instance=RequestContext(request))
    
