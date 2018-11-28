from __future__ import unicode_literals

import json

from ..models import UserMailer

from .literals import (
    TEST_EMAIL_FROM_ADDRESS, TEST_USER_MAILER_BACKEND_PATH,
    TEST_USER_MAILER_LABEL
)


class MailerTestMixin(object):
    def _create_user_mailer(self):
        self.user_mailer = UserMailer.objects.create(
            default=True,
            enabled=True,
            label=TEST_USER_MAILER_LABEL,
            backend_path=TEST_USER_MAILER_BACKEND_PATH,
            backend_data=json.dumps(
                {
                    'from': TEST_EMAIL_FROM_ADDRESS
                }
            )
        )
