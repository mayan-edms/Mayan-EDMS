from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.core.urlresolvers import reverse
#from django.utils.html import mark_safe
from django.conf import settings

from documents.views import document_list
from documents.models import Document
from permissions.exceptions import PermissionDenied
from permissions.models import Permission
from acls.models import AccessEntry

from .models import DocumentCheckout
from .permissions import PERMISSION_DOCUMENT_CHECKOUT, PERMISSION_DOCUMENT_CHECKIN
from .forms import DocumentCheckoutForm
from .exceptions import DocumentAlreadyCheckedOut


def checkout_list(request):
    return document_list(request, object_list=DocumentCheckout.objects.checked_out(), title=_(u'checked out documents'))


def checkout_info(request, document_pk):
    document = get_object_or_404(Document, pk=document_pk)
    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_DOCUMENT_CHECKOUT, PERMISSION_DOCUMENT_CHECKIN])
    except PermissionDenied:
        AccessEntry.objects.check_access([PERMISSION_DOCUMENT_CHECKOUT, PERMISSION_DOCUMENT_CHECKIN], request.user, document)

    if document.is_checked_out():
        content = 'checkedout'
    else:
        content = _(u'Document has not been checked out.')
    #<p>{{ content|safe }}</p>
    #{% endif %}

    #{% for paragraph in paragraphs %}
    #<p>{{ paragraph|safe }}</p>#
        
    return render_to_response('generic_template.html', {
        'content': content,
        'object': document,
        'title': _(u'Check out details for document: %s') % document
    }, context_instance=RequestContext(request))    


def checkout_document(request, document_pk):
    document = get_object_or_404(Document, pk=document_pk)
    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_DOCUMENT_CHECKOUT])
    except PermissionDenied:
        AccessEntry.objects.check_access(PERMISSION_DOCUMENT_CHECKOUT, request.user, document)

    if request.method == 'POST':
        form = DocumentCheckoutForm(request.POST)
        if form.is_valid():
            try:
                document_checkout = form.save()
            except DocumentAlreadyCheckedOut:
                messages.error(request, _(u'Document already checked out.'))
            except Exception, exc:
                messages.error(request, _(u'Error trying to check out document; %s') % exc)
            else:
                messages.success(request, _(u'Document "%s" checked out successfully.') % document)
                return HttpResponseRedirect(document_checkout.get_absolute_url())
    else:
        form = DocumentCheckoutForm()#document=document, initial={
            #'new_filename': document.filename})

    return render_to_response('generic_form.html', {
        'form': form,
        'object': document,
        'title': _(u'Check out document: %s') % document
    }, context_instance=RequestContext(request))    


def checkin_document(request, document_pk):
    document = get_object_or_404(Document, pk=document_pk)
    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_DOCUMENT_CHECKIN])
    except PermissionDenied:
        AccessEntry.objects.check_access(PERMISSION_DOCUMENT_CHECKIN, request.user, document)

    if request.method == 'POST':
        try:
            document.check_in()
        except DocumentAlreadyCheckedOut:
            messages.error(request, _(u'Document already checked out.'))
        except Exception, exc:
            messages.error(request, _(u'Error trying to check in document; %s') % exc)
        else:
            messages.success(request, _(u'Document "%s" checked out successfully.') % document)
            return HttpResponseRedirect(reverse('checkout_info', args=[document.pk]))

    return render_to_response('generic_form.html', {
        'object': document,
        'title': _(u'Check in document: %s') % document
    }, context_instance=RequestContext(request))
