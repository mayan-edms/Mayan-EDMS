from __future__ import unicode_literals

import datetime

from django.utils.timezone import now

from ..models import DocumentCheckout


class DocumentCheckoutTestMixin(object):
    _test_document_check_out_seconds = 0.1

    def _check_out_test_document(self, user=None):
        if not user:
            user = self._test_case_user

        self._check_out_expiration_datetime = now() + datetime.timedelta(
            seconds=self._test_document_check_out_seconds
        )

        self.test_check_out = DocumentCheckout.objects.check_out_document(
            block_new_version=True, document=self.test_document,
            expiration_datetime=self._check_out_expiration_datetime,
            user=user
        )
