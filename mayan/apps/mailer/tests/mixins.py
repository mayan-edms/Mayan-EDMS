from __future__ import unicode_literals

import json

from ..models import UserMailer

from .literals import (
    TEST_EMAIL_ADDRESS,
    TEST_EMAIL_FROM_ADDRESS,
    TEST_USER_MAILER_BACKEND_PATH,
    TEST_USER_MAILER_LABEL
)


class MailerTestMixin(object):
    def _create_test_user_mailer(self):
        self.test_user_mailer = UserMailer.objects.create(
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


class MailerViewTestMixin(object):
    def _request_test_document_link_send_view(self):
        return self.post(
            viewname='mailer:send_document_link', kwargs={
                'pk': self.test_document.pk
            }, data={
                'email': getattr(
                    self, 'test_email_address', TEST_EMAIL_ADDRESS
                ),
                'user_mailer': self.test_user_mailer.pk
            },
        )

    def _request_test_document_send_view(self):
        return self.post(
            viewname='mailer:send_document', kwargs={
                'pk': self.test_document.pk
            }, data={
                'email': getattr(
                    self, 'test_email_address', TEST_EMAIL_ADDRESS
                ),
                'user_mailer': self.test_user_mailer.pk
            }
        )

    def _request_test_user_mailer_create_view(self):
        return self.post(
            viewname='mailer:user_mailer_create', kwargs={
                'class_path': TEST_USER_MAILER_BACKEND_PATH
            }, data={
                'default': True,
                'enabled': True,
                'label': TEST_USER_MAILER_LABEL,
            }
        )

    def _request_test_user_mailer_delete_view(self):
        return self.post(
            viewname='mailer:user_mailer_delete', kwargs={
                'pk': self.test_user_mailer.pk
            }
        )

    def _request_test_user_mailer_list_view(self):
        return self.get(
            viewname='mailer:user_mailer_list',
        )

    def _request_test_user_mailer_test_view(self):
        return self.post(
            viewname='mailer:user_mailer_test', kwargs={
                'pk': self.test_user_mailer.pk
            }, data={
                'email': getattr(
                    self, 'test_email_address', TEST_EMAIL_ADDRESS
                )
            }
        )
