from __future__ import absolute_import

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.views.generic.list_detail import object_list
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied

from permissions.models import Permission
from documents.models import Document
from documents.widgets import document_link, document_thumbnail
from common.utils import encapsulate
from acls.models import AccessEntry
from job_processor.exceptions import JobQueuePushError

from .permissions import (PERMISSION_OCR_DOCUMENT,
    PERMISSION_OCR_DOCUMENT_DELETE, PERMISSION_OCR_QUEUE_ENABLE_DISABLE,
    PERMISSION_OCR_CLEAN_ALL_PAGES, PERMISSION_OCR_QUEUE_EDIT)
from .api import clean_pages


#            {'name': _(u'document'), 'attribute': encapsulate(lambda x: document_link(x.document_version.document) if hasattr(x, 'document_version') else _(u'Missing document.'))},
#            {'name': _(u'version'), 'attribute': 'document_version'},
#            {'name': _(u'thumbnail'), 'attribute': encapsulate(lambda x: document_thumbnail(x.document_version.document))},
#            {'name': _('submitted'), 'attribute': encapsulate(lambda x: unicode(x.datetime_submitted).split('.')[0]), 'keep_together':True},


def submit_document_multiple(request):
    for item_id in request.GET.get('id_list', '').split(','):
        submit_document(request, item_id)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def submit_document(request, document_id):
    document = get_object_or_404(Document, pk=document_id)

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_OCR_DOCUMENT])
    except PermissionDenied:
        AccessEntry.objects.check_access(PERMISSION_OCR_DOCUMENT, request.user, document)

    return submit_document_to_queue(request, document=document,
        post_submit_redirect=request.META.get('HTTP_REFERER', '/'))


def submit_document_to_queue(request, document, post_submit_redirect=None):
    """
    This view is meant to be reusable
    """

    try:
        document.submit_for_ocr()
        messages.success(request, _(u'Document: %(document)s was added to the OCR queue sucessfully.') % {
            'document': document})
    except JobQueuePushError:
        messages.warning(request, _(u'Document: %(document)s is already queued.') % {
        'document': document})
    except Exception, e:
        messages.error(request, e)

    if post_submit_redirect:
        return HttpResponseRedirect(post_submit_redirect)


def all_document_ocr_cleanup(request):
    Permission.objects.check_permissions(request.user, [PERMISSION_OCR_CLEAN_ALL_PAGES])

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', None)))
    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', None)))

    if request.method != 'POST':
        return render_to_response('generic_confirm.html', {
            'previous': previous,
            'next': next,
            'title': _(u'Are you sure you wish to clean up all the pages content?'),
            'message': _(u'On large databases this operation may take some time to execute.'),
            'form_icon': u'text_strikethroungh.png',
        }, context_instance=RequestContext(request))
    else:
        try:
            clean_pages()
            messages.success(request, _(u'Document pages content clean up complete.'))
        except Exception, e:
            messages.error(request, _(u'Document pages content clean up error: %s') % e)

        return HttpResponseRedirect(next)


def display_link(obj):
    output = []
    if hasattr(obj, 'get_absolute_url'):
        output.append(u'<a href="%(url)s">%(obj)s</a>' % {
            'url': obj.get_absolute_url(),
            'obj': obj
        })
    if output:
        return u''.join(output)
    else:
        return obj
