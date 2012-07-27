from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied

from documents.views import document_list
from documents.models import Document

from permissions.models import Permission
from acls.models import AccessEntry
from common.utils import get_object_name
from common.utils import encapsulate

from .models import DocumentCheckout
from .permissions import (PERMISSION_DOCUMENT_CHECKOUT, PERMISSION_DOCUMENT_CHECKIN,
    PERMISSION_DOCUMENT_CHECKIN_OVERRIDE)
from .forms import DocumentCheckoutForm
from .exceptions import DocumentAlreadyCheckedOut, DocumentNotCheckedOut
from .widgets import checkout_widget


def checkout_list(request):

    return document_list(
        request,
        object_list=DocumentCheckout.objects.checked_out_documents(),
        title=_(u'checked out documents'),
        extra_context={
                'extra_columns': [
                    {'name': _(u'checkout user'), 'attribute': encapsulate(lambda document: get_object_name(document.checkout_info().user_object, display_object_type=False))},
                    {'name': _(u'checkout time and date'), 'attribute': encapsulate(lambda document: document.checkout_info().checkout_datetime)},
                    {'name': _(u'checkout expiration'), 'attribute': encapsulate(lambda document: document.checkout_info().expiration_datetime)},
                ],
        }
    )


def checkout_info(request, document_pk):
    document = get_object_or_404(Document, pk=document_pk)
    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_DOCUMENT_CHECKOUT, PERMISSION_DOCUMENT_CHECKIN])
    except PermissionDenied:
        AccessEntry.objects.check_accesses([PERMISSION_DOCUMENT_CHECKOUT, PERMISSION_DOCUMENT_CHECKIN], request.user, document)

    paragraphs = [checkout_widget(document)]

    if document.is_checked_out():
        checkout_info = document.checkout_info()
        paragraphs.append(_(u'User: %s') % get_object_name(checkout_info.user_object, display_object_type=False))
        paragraphs.append(_(u'Check out time: %s') % checkout_info.checkout_datetime)
        paragraphs.append(_(u'Check out expiration: %s') % checkout_info.expiration_datetime)
        paragraphs.append(_(u'New versions allowed: %s') % (_(u'yes') if not checkout_info.block_new_version else _(u'no')))

    return render_to_response('generic_template.html', {
        'paragraphs': paragraphs,
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
        form = DocumentCheckoutForm(data=request.POST, initial={'document': document})
        try:
            if form.is_valid():
                try:
                    document_checkout = form.save(commit=False)
                    document_checkout.user_object = request.user
                    document_checkout.save()
                except Exception, exc:
                    messages.error(request, _(u'Error trying to check out document; %s') % exc)
                else:
                    messages.success(request, _(u'Document "%s" checked out successfully.') % document)
                    return HttpResponseRedirect(reverse('checkout_info', args=[document.pk]))
        except DocumentAlreadyCheckedOut:
            messages.error(request, _(u'Document already checked out.'))
            return HttpResponseRedirect(reverse('checkout_info', args=[document.pk]))
    else:
        form = DocumentCheckoutForm(initial={'document': document})

    return render_to_response('generic_form.html', {
        'form': form,
        'object': document,
        'title': _(u'Check out document: %s') % document
    }, context_instance=RequestContext(request))


def checkin_document(request, document_pk):
    document = get_object_or_404(Document, pk=document_pk)
    post_action_redirect = reverse('checkout_info', args=[document.pk])

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', '/')))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', '/')))

    # If the user trying to check in the document is the same as the check out
    # user just check for the normal permission otherwise check for the forceful
    # checkin permission
    try:
        if document.checkout_info().user_object == request.user:
            try:
                Permission.objects.check_permissions(request.user, [PERMISSION_DOCUMENT_CHECKIN])
            except PermissionDenied:
                AccessEntry.objects.check_access(PERMISSION_DOCUMENT_CHECKIN, request.user, document)
        else:
            try:
                Permission.objects.check_permissions(request.user, [PERMISSION_DOCUMENT_CHECKIN_OVERRIDE])
            except PermissionDenied:
                AccessEntry.objects.check_access(PERMISSION_DOCUMENT_CHECKIN_OVERRIDE, request.user, document)
    except DocumentNotCheckedOut:
        messages.error(request, _(u'Document has not been checked out.'))
        return HttpResponseRedirect(previous)

    if request.method == 'POST':
        try:
            document.check_in(user=request.user)
        except DocumentNotCheckedOut:
            messages.error(request, _(u'Document has not been checked out.'))
        except Exception, exc:
            messages.error(request, _(u'Error trying to check in document; %s') % exc)
        else:
            messages.success(request, _(u'Document "%s" checked in successfully.') % document)
            return HttpResponseRedirect(next)

    context = {
        'object_name': _(u'document'),
        'delete_view': False,
        'previous': previous,
        'next': next,
        'form_icon': u'basket_remove.png',
        'object': document,
    }

    if document.checkout_info().user_object != request.user:
        context['title'] = _(u'You didn\'t originally checked out this document.  Are you sure you wish to forcefully check in document: %s?') % document
    else:
        context['title'] = _(u'Are you sure you wish to check in document: %s?') % document

    return render_to_response('generic_confirm.html', context,
        context_instance=RequestContext(request))
