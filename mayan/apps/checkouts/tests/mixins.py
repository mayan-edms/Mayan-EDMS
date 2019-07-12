from __future__ import unicode_literals

import datetime

from django.utils.timezone import now

from mayan.apps.common.literals import TIME_DELTA_UNIT_DAYS
from mayan.apps.common.tests.utils import as_id_list

from ..models import DocumentCheckout


class DocumentCheckoutTestMixin(object):
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
            block_new_version=True, document=document,
            expiration_datetime=self._check_out_expiration_datetime,
            user=user
        )


class DocumentCheckoutViewTestMixin(object):
    def _request_test_document_check_in_get_view(self):
        return self.get(
            viewname='checkouts:check_in_document', kwargs={
                'pk': self.test_document.pk
            }
        )

    def _request_test_document_check_in_post_view(self):
        return self.post(
            viewname='checkouts:check_in_document', kwargs={
                'pk': self.test_document.pk
            }
        )

    def _request_test_document_multiple_check_in_post_view(self):
        return self.post(
            viewname='checkouts:check_in_document_multiple', data={
                'id_list': as_id_list(items=self.test_documents)
            }
        )

    def _request_test_document_check_out_view(self):
        return self.post(
            viewname='checkouts:check_out_document', kwargs={
                'pk': self.test_document.pk
            }, data={
                'block_new_version': True,
                'expiration_datetime_0': TIME_DELTA_UNIT_DAYS,
                'expiration_datetime_1': 2
            }
        )

    def _request_test_document_multiple_check_out_post_view(self):
        return self.post(
            viewname='checkouts:check_out_document_multiple', data={
                'block_new_version': True,
                'expiration_datetime_0': TIME_DELTA_UNIT_DAYS,
                'expiration_datetime_1': 2,
                'id_list': as_id_list(items=self.test_documents)
            }
        )

    def _request_test_document_check_out_detail_view(self):
        return self.get(
            viewname='checkouts:check_out_info', kwargs={
                'pk': self.test_document.pk
            }
        )

    def _request_test_document_check_out_list_view(self):
        return self.get(viewname='checkouts:check_out_list')
