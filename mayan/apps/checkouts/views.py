from __future__ import absolute_import, unicode_literals

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from documents.models import Document
from documents.views import document_list

from acls.models import AccessEntry
from common.utils import encapsulate, get_object_name
from permissions.models import Permission

from .exceptions import DocumentAlreadyCheckedOut, DocumentNotCheckedOut
from .forms import DocumentCheckoutForm
from .literals import STATE_LABELS
from .models import DocumentCheckout
from .permissions import (
    PERMISSION_DOCUMENT_CHECKIN, PERMISSION_DOCUMENT_CHECKIN_OVERRIDE,
    PERMISSION_DOCUMENT_CHECKOUT
)


def checkout_list(request):
    return document_list(
        request,
        object_list=DocumentCheckout.objects.checked_out_documents(),
        title=_('Documents checked out'),
        extra_context={
            'extra_columns': [
                {'name': _('Checkout user'), 'attribute': encapsulate(lambda document: get_object_name(document.checkout_info().user_object, display_object_type=False))},
                {'name': _('Checkout time and date'), 'attribute': encapsulate(lambda document: document.checkout_info().checkout_datetime)},
                {'name': _('Checkout expiration'), 'attribute': encapsulate(lambda document: document.checkout_info().expiration_datetime)},
            ],
        }
    )


def checkout_info(request, document_pk):
    document = get_object_or_404(Document, pk=document_pk)
    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_DOCUMENT_CHECKOUT, PERMISSION_DOCUMENT_CHECKIN])
    except PermissionDenied:
        AccessEntry.objects.check_accesses([PERMISSION_DOCUMENT_CHECKOUT, PERMISSION_DOCUMENT_CHECKIN], request.user, document)

    paragraphs = [_('Document status: %s') % STATE_LABELS[document.checkout_state()]]

    if document.is_checked_out():
        checkout_info = document.checkout_info()
        paragraphs.append(_('User: %s') % get_object_name(checkout_info.user_object, display_object_type=False))
        paragraphs.append(_('Check out time: %s') % checkout_info.checkout_datetime)
        paragraphs.append(_('Check out expiration: %s') % checkout_info.expiration_datetime)
        paragraphs.append(_('New versions allowed: %s') % (_('Yes') if not checkout_info.block_new_version else _('No')))

    return render_to_response('main/generic_template.html', {
        'paragraphs': paragraphs,
        'object': document,
        'title': _('Check out details for document: %s') % document
    }, context_instance=RequestContext(request))


def checkout_document(request, document_pk):
    document = get_object_or_404(Document, pk=document_pk)
    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_DOCUMENT_CHECKOUT])
    except PermissionDenied:
        AccessEntry.objects.check_access(PERMISSION_DOCUMENT_CHECKOUT, request.user, document)

    if request.method == 'POST':
        form = DocumentCheckoutForm(data=request.POST, initial={'document': document})
        if form.is_valid():
            try:
                document_checkout = form.save(commit=False)
                document_checkout.user_object = request.user
                document_checkout.document = document
                document_checkout.save()
            except DocumentAlreadyCheckedOut:
                messages.error(request, _('Document already checked out.'))
                return HttpResponseRedirect(reverse('checkouts:checkout_info', args=[document.pk]))
            except Exception as exception:
                messages.error(request, _('Error trying to check out document; %s') % exception)
            else:
                messages.success(request, _('Document "%s" checked out successfully.') % document)
                return HttpResponseRedirect(reverse('checkouts:checkout_info', args=[document.pk]))
    else:
        form = DocumentCheckoutForm(initial={'document': document})

    return render_to_response('main/generic_form.html', {
        'form': form,
        'object': document,
        'title': _('Check out document: %s') % document
    }, context_instance=RequestContext(request))


def checkin_document(request, document_pk):
    document = get_object_or_404(Document, pk=document_pk)
    post_action_redirect = reverse('checkouts:checkout_info', args=[document.pk])

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', reverse('main:home'))))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', reverse('main:home'))))

    if not document.is_checked_out():
        messages.error(request, _('Document has not been checked out.'))
        return HttpResponseRedirect(previous)

    # If the user trying to check in the document is the same as the check out
    # user just check for the normal permission otherwise check for the forceful
    # checkin permission
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

    if request.method == 'POST':
        try:
            document.check_in(user=request.user)
        except DocumentNotCheckedOut:
            messages.error(request, _('Document has not been checked out.'))
        except Exception as exception:
            messages.error(request, _('Error trying to check in document; %s') % exception)
        else:
            messages.success(request, _('Document "%s" checked in successfully.') % document)
            return HttpResponseRedirect(next)

    context = {
        'delete_view': False,
        'previous': previous,
        'next': next,
        'object': document,
    }

    if document.checkout_info().user_object != request.user:
        context['title'] = _('You didn\'t originally checked out this document.  Are you sure you wish to forcefully check in document: %s?') % document
    else:
        context['title'] = _('Are you sure you wish to check in document: %s?') % document

    return render_to_response('main/generic_confirm.html', context,
                              context_instance=RequestContext(request))
