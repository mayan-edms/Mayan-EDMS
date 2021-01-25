import datetime

from django.utils.timezone import now

from mayan.apps.common.literals import TIME_DELTA_UNIT_DAYS
from mayan.apps.testing.tests.utils import as_id_list

from ..models import DocumentCheckout


class DocumentCheckoutsAPIViewTestMixin:
    def _request_test_document_check_out_create_api_view(self):
        return self.post(
            viewname='rest_api:checkout-document-list', data={
                'document_pk': self.test_document.pk,
                'expiration_datetime': '2099-01-01T12:00'
            }
        )

    def _request_test_document_check_out_delete_api_view(self):
        return self.delete(
            viewname='rest_api:checkedout-document-view',
            kwargs={'checkout_id': self.test_check_out.pk}
        )

    def _request_test_document_check_out_detail_api_view(self):
        return self.get(
            viewname='rest_api:checkedout-document-view',
            kwargs={'checkout_id': self.test_check_out.pk}
        )

    def _request_test_document_check_out_list_api_view(self):
        return self.get(viewname='rest_api:checkout-document-list')


class DocumentCheckoutTestMixin:
    _test_document_check_out_seconds = 0.1

    def _check_out_test_document(self, document=None, user=None):
        if not document:
            document = self.test_document

        if not user:
            user = self._test_case_user

        self._check_out_expiration_datetime = now() + datetime.timedelta(
            seconds=self._test_document_check_out_seconds
        )

        self.test_check_out = DocumentCheckout.objects.check_out_document(
            block_new_file=True, document=document,
            expiration_datetime=self._check_out_expiration_datetime,
            user=user
        )


class DocumentCheckoutViewTestMixin:
    def _request_test_document_check_in_get_view(self):
        return self.get(
            viewname='checkouts:check_in_document', kwargs={
                'document_id': self.test_document.pk
            }
        )

    def _request_test_document_check_in_post_view(self, follow=False):
        return self.post(
            viewname='checkouts:check_in_document', kwargs={
                'document_id': self.test_document.pk
            }, follow=follow
        )

    def _request_test_document_multiple_check_in_post_view(self):
        return self.post(
            viewname='checkouts:check_in_document_multiple', data={
                'id_list': as_id_list(items=self.test_documents)
            }
        )

    def _request_test_document_check_out_get_view(self):
        return self.get(
            viewname='checkouts:check_out_document', kwargs={
                'document_id': self.test_document.pk
            },
        )

    def _request_test_document_check_out_post_view(self, follow=False):
        return self.post(
            viewname='checkouts:check_out_document', kwargs={
                'document_id': self.test_document.pk
            }, data={
                'expiration_datetime_unit': TIME_DELTA_UNIT_DAYS,
                'expiration_datetime_amount': 99,
                'block_new_file': True
            }, follow=follow
        )

    def _request_test_document_multiple_check_out_post_view(self):
        return self.post(
            viewname='checkouts:check_out_document_multiple', data={
                'block_new_file': True,
                'expiration_datetime_unit': TIME_DELTA_UNIT_DAYS,
                'expiration_datetime_amount': 99,
                'id_list': as_id_list(items=self.test_documents)
            }
        )

    def _request_test_document_check_out_detail_view(self):
        return self.get(
            viewname='checkouts:check_out_info', kwargs={
                'document_id': self.test_document.pk
            }
        )

    def _request_test_document_check_out_list_view(self):
        return self.get(viewname='checkouts:check_out_list')
