from __future__ import absolute_import, unicode_literals

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.models import AccessControlList
from mayan.apps.common.generics import (
    ConfirmView, SingleObjectCreateView, SingleObjectDetailView
)
from mayan.apps.common.utils import encapsulate
from mayan.apps.documents.models import Document
from mayan.apps.documents.views import DocumentListView

from .exceptions import DocumentAlreadyCheckedOut, DocumentNotCheckedOut
from .forms import DocumentCheckoutForm, DocumentCheckoutDefailForm
from .icons import icon_check_out_info
from .models import DocumentCheckout
from .permissions import (
    permission_document_check_in, permission_document_check_in_override,
    permission_document_check_out, permission_document_check_out_detail_view
)


class DocumentCheckInView(ConfirmView):
    def get_extra_context(self):
        document = self.get_object()

        context = {
            'object': document,
        }

        if document.get_check_out_info().user != self.request.user:
            context['title'] = _(
                'You didn\'t originally checked out this document. '
                'Forcefully check in the document: %s?'
            ) % document
        else:
            context['title'] = _('Check in the document: %s?') % document

        return context

    def get_object(self):
        return get_object_or_404(klass=Document, pk=self.kwargs['pk'])

    def get_post_action_redirect(self):
        return reverse(
            viewname='checkouts:check_out_info', kwargs={
                'pk': self.get_object().pk
            }
        )

    def view_action(self):
        document = self.get_object()

        if document.get_check_out_info().user == self.request.user:
            AccessControlList.objects.check_access(
                obj=document, permissions=(permission_document_check_in,),
                user=self.request.user
            )
        else:
            AccessControlList.objects.check_access(
                obj=document,
                permissions=(permission_document_check_in_override,),
                user=self.request.user
            )

        try:
            document.check_in(user=self.request.user)
        except DocumentNotCheckedOut:
            messages.error(
                message=_('Document has not been checked out.'),
                request=self.request
            )
        else:
            messages.success(
                message=_(
                    'Document "%s" checked in successfully.'
                ) % document, request=self.request
            )


class DocumentCheckOutDetailView(SingleObjectDetailView):
    form_class = DocumentCheckoutDefailForm
    model = Document
    object_permission = permission_document_check_out_detail_view

    def get_extra_context(self):
        return {
            'object': self.object,
            'title': _(
                'Check out details for document: %s'
            ) % self.object
        }


class DocumentCheckOutView(SingleObjectCreateView):
    form_class = DocumentCheckoutForm

    def dispatch(self, request, *args, **kwargs):
        self.document = get_object_or_404(klass=Document, pk=self.kwargs['pk'])

        AccessControlList.objects.check_access(
            obj=self.document, permissions=(permission_document_check_out,),
            user=request.user
        )

        return super(
            DocumentCheckOutView, self
        ).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        try:
            instance = form.save(commit=False)
            instance.user = self.request.user
            instance.document = self.document
            instance.save()
        except DocumentAlreadyCheckedOut:
            messages.error(
                message=_('Document already checked out.'),
                request=self.request
            )
        else:
            messages.success(
                message=_(
                    'Document "%s" checked out successfully.'
                ) % self.document, request=self.request
            )

        return HttpResponseRedirect(redirect_to=self.get_success_url())

    def get_extra_context(self):
        return {
            'object': self.document,
            'title': _('Check out document: %s') % self.document
        }

    def get_post_action_redirect(self):
        return reverse(
            viewname='checkouts:check_out_info', kwargs={
                'pk': self.document.pk
            }
        )


class DocumentCheckOutListView(DocumentListView):
    def get_document_queryset(self):
        return AccessControlList.objects.restrict_queryset(
            permission=permission_document_check_out_detail_view,
            queryset=DocumentCheckout.objects.checked_out_documents(),
            user=self.request.user
        )

    def get_extra_context(self):
        context = super(DocumentCheckOutListView, self).get_extra_context()
        context.update(
            {
                'extra_columns': (
                    {
                        'name': _('User'),
                        'attribute': encapsulate(
                            lambda document: document.get_check_out_info().user.get_full_name() or document.get_check_out_info().user
                        )
                    },
                    {
                        'name': _('Checkout time and date'),
                        'attribute': encapsulate(
                            lambda document: document.get_check_out_info().checkout_datetime
                        )
                    },
                    {
                        'name': _('Checkout expiration'),
                        'attribute': encapsulate(
                            lambda document: document.get_check_out_info().expiration_datetime
                        )
                    },
                ),
                'no_results_icon': icon_check_out_info,
                'no_results_text': _(
                    'Checking out a document blocks certain document '
                    'operations for a predetermined amount of '
                    'time.'
                ),
                'no_results_title': _('No documents have been checked out'),
                'title': _('Documents checked out'),
            }
        )
        return context
