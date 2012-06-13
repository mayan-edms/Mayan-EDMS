from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.core.urlresolvers import reverse

from documents.views import document_list
from documents.models import Document
from django.core.exceptions import PermissionDenied

from permissions.models import Permission
from acls.models import AccessEntry
from common.utils import get_object_name

from .models import DocumentCheckout
from .permissions import PERMISSION_DOCUMENT_CHECKOUT, PERMISSION_DOCUMENT_CHECKIN
from .forms import DocumentCheckoutForm
from .exceptions import DocumentAlreadyCheckedOut, DocumentNotCheckedOut
from .literals import STATE_CHECKED_OUT, STATE_CHECKED_IN, STATE_ICONS, STATE_LABELS
from .widgets import checkout_widget

def checkout_list(request):
    return document_list(request, object_list=DocumentCheckout.objects.checked_out_documents(), title=_(u'checked out documents'))


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
        paragraphs.append(_(u'Checkout time: %s') % checkout_info.checkout_datetime)
        paragraphs.append(_(u'Checkout expiration: %s') % checkout_info.expiration_datetime)
        
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
        if form.is_valid():
            try:
                document_checkout = form.save(commit=False)
                document_checkout.user_object = request.user
                #document_checkout.clean()
                document_checkout.save()
            except DocumentAlreadyCheckedOut:
                messages.error(request, _(u'Document already checked out.'))
            except Exception, exc:
                messages.error(request, _(u'Error trying to check out document; %s') % exc)
            else:
                messages.success(request, _(u'Document "%s" checked out successfully.') % document)
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
    # TODO: add forcefull checkin
    # TODO: check user
    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_DOCUMENT_CHECKIN])
    except PermissionDenied:
        AccessEntry.objects.check_access(PERMISSION_DOCUMENT_CHECKIN, request.user, document)

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', '/')))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', '/')))

    if request.method == 'POST':
        try:
            document.check_in()
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
        'title': _(u'Are you sure you wish to check in document: %s') % document
    }

    return render_to_response('generic_confirm.html', context,
        context_instance=RequestContext(request))


def document_delete(request, document_id=None, document_id_list=None):
    post_action_redirect = None

    if document_id:
        documents = [get_object_or_404(Document, pk=document_id)]
        post_action_redirect = reverse('document_list_recent')
    elif document_id_list:
        documents = [get_object_or_404(Document, pk=document_id) for document_id in document_id_list.split(',')]
    else:
        messages.error(request, _(u'Must provide at least one document.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_DOCUMENT_DELETE])
    except PermissionDenied:
        documents = AccessEntry.objects.filter_objects_by_access(PERMISSION_DOCUMENT_DELETE, request.user, documents, exception_on_empty=True)

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', '/')))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', '/')))

    if request.method == 'POST':
        for document in documents:
            try:
                warnings = delete_indexes(document)
                if request.user.is_staff or request.user.is_superuser:
                    for warning in warnings:
                        messages.warning(request, warning)

                document.delete()
                #create_history(HISTORY_DOCUMENT_DELETED, data={'user': request.user, 'document': document})
                messages.success(request, _(u'Document deleted successfully.'))
            except Exception, e:
                messages.error(request, _(u'Document: %(document)s delete error: %(error)s') % {
                    'document': document, 'error': e
                })

        return HttpResponseRedirect(next)

    context = {
        'object_name': _(u'document'),
        'delete_view': True,
        'previous': previous,
        'next': next,
        'form_icon': u'page_delete.png',
    }
    if len(documents) == 1:
        context['object'] = documents[0]
        context['title'] = _(u'Are you sure you wish to delete the document: %s?') % ', '.join([unicode(d) for d in documents])
    elif len(documents) > 1:
        context['title'] = _(u'Are you sure you wish to delete the documents: %s?') % ', '.join([unicode(d) for d in documents])

    return render_to_response('generic_confirm.html', context,
        context_instance=RequestContext(request))    
