from __future__ import unicode_literals

from ..models import Message

from .literals import TEST_LABEL, TEST_MESSAGE


class MOTDTestMixin(object):
    def _create_test_message(self):
        self.test_message = Message.objects.create(
            label=TEST_LABEL, message=TEST_MESSAGE
        )
