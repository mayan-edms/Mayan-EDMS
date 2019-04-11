from __future__ import unicode_literals

import datetime

from django.utils.timezone import now

from ..models import DocumentCheckout


class DocumentCheckoutTestMixin(object):
    def _check_out_document(self, user=None):
        if not user:
            user = self.user

        expiration_datetime = now() + datetime.timedelta(days=1)

        self.test_check_out = DocumentCheckout.objects.check_out_document(
            document=self.document, expiration_datetime=expiration_datetime,
            user=user, block_new_version=True
        )
