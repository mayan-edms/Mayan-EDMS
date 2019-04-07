from __future__ import unicode_literals

import datetime

from django.utils.timezone import now

from ..models import DocumentCheckout


class DocumentCheckoutTestMixin(object):
    def _checkout_document(self):
        expiration_datetime = now() + datetime.timedelta(days=1)

        DocumentCheckout.objects.checkout_document(
            document=self.document, expiration_datetime=expiration_datetime,
            user=self.user, block_new_version=True
        )
        self.assertTrue(self.document.is_checked_out())
