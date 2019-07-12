from __future__ import absolute_import, unicode_literals

from django.urls import reverse
from django.utils.translation import ugettext_lazy as _, ungettext

from mayan.apps.acls.models import AccessControlList
from mayan.apps.common.generics import (
    MultipleObjectConfirmActionView, MultipleObjectFormActionView,
    SingleObjectDetailView
)
from mayan.apps.documents.models import Document
from mayan.apps.documents.views import DocumentListView

from .forms import DocumentCheckoutForm, DocumentCheckoutDefailForm
from .icons import icon_check_out_info
from .models import DocumentCheckout
from .permissions import (
    permission_document_check_in, permission_document_check_in_override,
    permission_document_check_out, permission_document_check_out_detail_view
)


class DocumentCheckinView(MultipleObjectConfirmActionView):
    error_message = 'Unable to check in document "%(instance)s". %(exception)s'
    model = Document
    pk_url_kwarg = 'pk'
    success_message_singular = '%(count)d document checked in.'
    success_message_plural = '%(count)d documents checked in.'

    def get_extra_context(self):
        queryset = self.get_object_list()

        result = {
            'title': ungettext(
                singular='Check in %(count)d document',
                plural='Check in %(count)d documents',
                number=queryset.count()
            ) % {
                'count': queryset.count(),
            }
        }

        if queryset.count() == 1:
            result.update(
                {
                    'object': queryset.first(),
                    'title': _(
                        'Check in document: %s'
                    ) % queryset.first()
                }
            )

        return result

    def get_post_object_action_url(self):
        if self.action_count == 1:
            return reverse(
                viewname='checkouts:document_checkout_info',
                kwargs={'pk': self.action_id_list[0]}
            )
        else:
            super(DocumentCheckinView, self).get_post_action_redirect()

    def get_source_queryset(self):
        # object_permission is None to disable restricting queryset mixin
        # and restrict the queryset ourselves from two permissions

        source_queryset = super(DocumentCheckinView, self).get_source_queryset()

        check_in_queryset = AccessControlList.objects.restrict_queryset(
            permission=permission_document_check_in, queryset=source_queryset,
            user=self.request.user
        )

        check_in_override_queryset = AccessControlList.objects.restrict_queryset(
            permission=permission_document_check_in_override,
            queryset=source_queryset, user=self.request.user
        )

        return check_in_queryset | check_in_override_queryset

    def object_action(self, form, instance):
        DocumentCheckout.business_logic.check_in_document(
            document=instance, user=self.request.user
        )


class DocumentCheckoutView(MultipleObjectFormActionView):
    error_message = 'Unable to checkout document "%(instance)s". %(exception)s'
    form_class = DocumentCheckoutForm
    model = Document
    object_permission = permission_document_check_out
    pk_url_kwarg = 'pk'
    success_message_singular = '%(count)d document checked out.'
    success_message_plural = '%(count)d documents checked out.'

    def get_extra_context(self):
        queryset = self.get_object_list()

        result = {
            'title': ungettext(
                singular='Checkout %(count)d document',
                plural='Checkout %(count)d documents',
                number=queryset.count()
            ) % {
                'count': queryset.count(),
            }
        }

        if queryset.count() == 1:
            result.update(
                {
                    'object': queryset.first(),
                    'title': _(
                        'Check out document: %s'
                    ) % queryset.first()
                }
            )

        return result

    def get_post_object_action_url(self):
        if self.action_count == 1:
            return reverse(
                viewname='checkouts:document_checkout_info',
                kwargs={'pk': self.action_id_list[0]}
            )
        else:
            super(DocumentCheckoutView, self).get_post_action_redirect()

    def object_action(self, form, instance):
        DocumentCheckout.objects.check_out_document(
            block_new_version=form.cleaned_data['block_new_version'],
            document=instance,
            expiration_datetime=form.cleaned_data['expiration_datetime'],
            user=self.request.user,
        )


class DocumentCheckoutDetailView(SingleObjectDetailView):
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


class DocumentCheckoutListView(DocumentListView):
    def get_document_queryset(self):
        return AccessControlList.objects.restrict_queryset(
            permission=permission_document_check_out_detail_view,
            queryset=DocumentCheckout.objects.checked_out_documents(),
            user=self.request.user
        )

    def get_extra_context(self):
        context = super(DocumentCheckoutListView, self).get_extra_context()
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
