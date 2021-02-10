from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.models import AccessControlList
from mayan.apps.documents.models import Document
from mayan.apps.documents.views.document_views import DocumentListView
from mayan.apps.views.exceptions import ActionError
from mayan.apps.views.generics import (
    MultipleObjectConfirmActionView, MultipleObjectFormActionView,
    SingleObjectDetailView
)

from .exceptions import DocumentAlreadyCheckedOut, DocumentNotCheckedOut
from .forms import DocumentCheckOutForm, DocumentCheckOutDetailForm
from .icons import icon_check_out_info
from .models import DocumentCheckout
from .permissions import (
    permission_document_check_in, permission_document_check_in_override,
    permission_document_check_out, permission_document_check_out_detail_view
)


class DocumentCheckInView(MultipleObjectConfirmActionView):
    error_message = _(
        'Unable to check in document "%(instance)s"; %(exception)s'
    )
    pk_url_kwarg = 'document_id'
    success_message_single = _(
        'Document "%(object)s" checked in successfully.'
    )
    success_message_singular = _(
        '%(count)d document checked in successfully.'
    )
    success_message_plural = _(
        '%(count)d documents checked in successfully.'
    )
    title_single = _('Check in document "%(object)s".')
    title_singular = _('Check in %(count)d document.')
    title_plural = _('Check in %(count)d documents.')

    def get_extra_context(self):
        context = {
            'submit_label': _('Check in'),
        }

        if self.object_list.count() == 1:
            context.update(
                {
                    'object': self.object_list.first(),
                }
            )

        return context

    def get_post_object_action_url(self):
        if self.action_count == 1:
            return reverse(
                viewname='checkouts:check_out_info', kwargs={
                    'document_id': self.action_id_list[0]
                }
            )
        else:
            super().get_post_action_redirect()

    def get_source_queryset(self):
        # object_permission is None to disable restricting queryset mixin
        # and restrict the queryset ourselves from two permissions.
        document_queryset = Document.valid.all()

        check_in_queryset = AccessControlList.objects.restrict_queryset(
            permission=permission_document_check_in, queryset=document_queryset,
            user=self.request.user
        )

        check_in_override_queryset = AccessControlList.objects.restrict_queryset(
            permission=permission_document_check_in_override,
            queryset=document_queryset, user=self.request.user
        )

        return check_in_queryset | check_in_override_queryset

    def object_action(self, form, instance):
        try:
            DocumentCheckout.business_logic.check_in_document(
                document=instance, user=self.request.user
            )
        except DocumentNotCheckedOut as exception:
            raise ActionError(exception)


class DocumentCheckOutView(MultipleObjectFormActionView):
    error_message = _(
        'Unable to checkout document "%(instance)s"; %(exception)s'
    )
    form_class = DocumentCheckOutForm
    object_permission = permission_document_check_out
    pk_url_kwarg = 'document_id'
    source_queryset = Document.valid
    success_message_single = _(
        'Document "%(object)s" checked out successfully.'
    )
    success_message_singular = _(
        '%(count)d document checked out successfully.'
    )
    success_message_plural = _(
        '%(count)d documents checked out successfully.'
    )
    title_single = _('Checkout document "%(object)s".')
    title_singular = _('Checkout %(count)d document.')
    title_plural = _('Checkout %(count)d documents.')

    def get_extra_context(self):
        context = {
            'submit_label': _('Checkout'),
        }

        if self.object_list.count() == 1:
            context.update(
                {
                    'object': self.object_list.first(),
                }
            )

        return context

    def get_post_object_action_url(self):
        if self.action_count == 1:
            return reverse(
                viewname='checkouts:check_out_info', kwargs={
                    'document_id': self.action_id_list[0]
                }
            )
        else:
            super().get_post_action_redirect()

    def object_action(self, form, instance):
        try:
            DocumentCheckout.objects.check_out_document(
                block_new_file=form.cleaned_data['block_new_file'],
                document=instance,
                expiration_datetime=form.cleaned_data['expiration_datetime'],
                user=self.request.user,
            )
        except DocumentAlreadyCheckedOut as exception:
            raise ActionError(exception)


class DocumentCheckOutDetailView(SingleObjectDetailView):
    form_class = DocumentCheckOutDetailForm
    object_permission = permission_document_check_out_detail_view
    pk_url_kwarg = 'document_id'
    source_queryset = Document.valid

    def get_extra_context(self):
        return {
            'object': self.object,
            'title': _(
                'Check out details for document: %s'
            ) % self.object
        }


class DocumentCheckOutListView(DocumentListView):
    def get_document_queryset(self):
        queryset = AccessControlList.objects.restrict_queryset(
            permission=permission_document_check_out_detail_view,
            queryset=DocumentCheckout.objects.checked_out_documents(),
            user=self.request.user
        )
        return Document.valid.filter(pk__in=queryset.values('pk'))

    def get_extra_context(self):
        context = super().get_extra_context()
        context.update(
            {
                'no_results_icon': icon_check_out_info,
                'no_results_text': _(
                    'Checking out a document, blocks certain operations '
                    'for a predetermined amount of time.'
                ),
                'no_results_title': _('No documents have been checked out'),
                'title': _('Checked out documents'),
            }
        )
        return context
