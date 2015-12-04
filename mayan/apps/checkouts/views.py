from __future__ import absolute_import, unicode_literals

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from documents.models import Document
from documents.views import DocumentListView

from acls.models import AccessControlList
from common.generics import ConfirmView, SingleObjectCreateView
from common.utils import encapsulate, render_date_object
from permissions import Permission

from .exceptions import DocumentAlreadyCheckedOut, DocumentNotCheckedOut
from .forms import DocumentCheckoutForm
from .literals import STATE_LABELS
from .models import DocumentCheckout
from .permissions import (
    permission_document_checkin, permission_document_checkin_override,
    permission_document_checkout
)


class CheckoutDocumentView(SingleObjectCreateView):
    form_class = DocumentCheckoutForm

    def dispatch(self, request, *args, **kwargs):
        self.document = get_object_or_404(Document, pk=self.kwargs['pk'])

        try:
            Permission.check_permissions(
                request.user, (permission_document_checkout,)
            )
        except PermissionDenied:
            AccessControlList.objects.check_access(
                permission_document_checkout, request.user, self.document
            )

        return super(
            CheckoutDocumentView, self
        ).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        try:
            instance = form.save(commit=False)
            instance.user = self.request.user
            instance.document = self.document
            instance.save()
        except DocumentAlreadyCheckedOut:
            messages.error(self.request, _('Document already checked out.'))
        except Exception as exception:
            messages.error(
                self.request,
                _('Error trying to check out document; %s') % exception
            )
        else:
            messages.success(
                self.request,
                _('Document "%s" checked out successfully.') % self.document
            )

        return HttpResponseRedirect(self.get_success_url())

    def get_extra_context(self):
        return {
            'object': self.document,
            'title': _('Check out document: %s') % self.document
        }

    def get_post_action_redirect(self):
        return reverse('checkouts:checkout_info', args=(self.document.pk,))


class CheckoutListView(DocumentListView):
    extra_context = {
        'title': _('Documents checked out'),
        'hide_links': True,
        'extra_columns': (
            {
                'name': _('User'),
                'attribute': encapsulate(
                    lambda document: document.checkout_info().user.get_full_name() or document.checkout_info().user
                )
            },
            {
                'name': _('Checkout time and date'),
                'attribute': encapsulate(
                    lambda document: document.checkout_info().checkout_datetime
                )
            },
            {
                'name': _('Checkout expiration'),
                'attribute': encapsulate(
                    lambda document: document.checkout_info().expiration_datetime
                )
            },
        ),
    }

    def get_document_queryset(self):
        return DocumentCheckout.objects.checked_out_documents()


def checkout_info(request, document_pk):
    document = get_object_or_404(Document, pk=document_pk)
    try:
        Permission.check_permissions(
            request.user, (
                permission_document_checkout, permission_document_checkin
            )
        )
    except PermissionDenied:
        AccessControlList.objects.check_access(
            (permission_document_checkout, permission_document_checkin),
            request.user, document
        )

    paragraphs = [
        _('Document status: %s') % STATE_LABELS[document.checkout_state()]
    ]

    if document.is_checked_out():
        checkout_info = document.checkout_info()
        paragraphs.append(
            _('User: %s') % (
                checkout_info.user.get_full_name() or checkout_info.user
            )
        )
        paragraphs.append(
            _(
                'Check out time: %s'
            ) % render_date_object(checkout_info.checkout_datetime)
        )
        paragraphs.append(
            _(
                'Check out expiration: %s'
            ) % render_date_object(checkout_info.expiration_datetime)
        )
        paragraphs.append(
            _(
                'New versions allowed: %s'
            ) % (_('Yes') if not checkout_info.block_new_version else _('No'))
        )

    return render_to_response(
        'appearance/generic_template.html', {
            'paragraphs': paragraphs,
            'object': document,
            'title': _('Check out details for document: %s') % document
        },
        context_instance=RequestContext(request)
    )


class DocumentCheckinView(ConfirmView):
    def get_extra_context(self):
        document = self.get_object()

        context = {
            'object': document,
        }

        if document.checkout_info().user != self.request.user:
            context['title'] = _(
                'You didn\'t originally checked out this document. '
                'Forcefully check in the document: %s?'
            ) % document
        else:
            context['title'] = _('Check in the document: %s?') % document

        return context

    def get_object(self):
        return get_object_or_404(Document, pk=self.kwargs['pk'])

    def get_post_action_redirect(self):
        return reverse('checkouts:checkout_info', args=(self.get_object().pk,))

    def view_action(self):
        document = self.get_object()

        if document.checkout_info().user == self.request.user:
            try:
                Permission.check_permissions(
                    self.request.user, (permission_document_checkin,)
                )
            except PermissionDenied:
                AccessControlList.objects.check_access(
                    permission_document_checkin, self.request.user, document
                )
        else:
            try:
                Permission.check_permissions(
                    self.request.user, (permission_document_checkin_override,)
                )
            except PermissionDenied:
                AccessControlList.objects.check_access(
                    permission_document_checkin_override, self.request.user,
                    document
                )

        try:
            document.check_in(user=self.request.user)
        except DocumentNotCheckedOut:
            messages.error(
                self.request, _('Document has not been checked out.')
            )
        except Exception as exception:
            messages.error(
                self.request,
                _('Error trying to check in document; %s') % exception
            )
        else:
            messages.success(
                self.request,
                _('Document "%s" checked in successfully.') % document
            )
