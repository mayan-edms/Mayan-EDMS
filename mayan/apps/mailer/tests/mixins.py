import json

from ..models import UserMailer

from .literals import (
    TEST_EMAIL_ADDRESS, TEST_EMAIL_FROM_ADDRESS,
    TEST_USER_MAILER_BACKEND_PATH, TEST_USER_MAILER_LABEL
)


class DocumentMailerViewTestMixin:
    def _request_test_document_send_link_single_view(self):
        return self.post(
            viewname='mailer:send_document_link_single', kwargs={
                'document_id': self.test_document.pk
            }, data={
                'email': getattr(
                    self, 'test_email_address', TEST_EMAIL_ADDRESS
                ),
                'user_mailer': self.test_user_mailer.pk
            },
        )

    def _request_test_document_send_link_multiple_view(self):
        return self.post(
            viewname='mailer:send_document_link_multiple', query={
                'id_list': self.test_document.pk
            }, data={
                'email': getattr(
                    self, 'test_email_address', TEST_EMAIL_ADDRESS
                ),
                'user_mailer': self.test_user_mailer.pk
            },
        )


class DocumentFileMailerViewTestMixin:
    def _request_test_document_file_send_link_single_view(self):
        return self.post(
            viewname='mailer:send_document_file_link_single', kwargs={
                'document_file_id': self.test_document_file.pk
            }, data={
                'email': getattr(
                    self, 'test_email_address', TEST_EMAIL_ADDRESS
                ),
                'user_mailer': self.test_user_mailer.pk
            }
        )

    def _request_test_document_file_send_link_multiple_view(self):
        return self.post(
            viewname='mailer:send_document_file_link_multiple', query={
                'id_list': self.test_document_file.pk
            }, data={
                'email': getattr(
                    self, 'test_email_address', TEST_EMAIL_ADDRESS
                ),
                'user_mailer': self.test_user_mailer.pk
            }
        )

    def _request_test_document_file_attachment_send_single_view(self):
        return self.post(
            viewname='mailer:send_document_file_attachment_single', kwargs={
                'document_file_id': self.test_document_file.pk
            }, data={
                'email': getattr(
                    self, 'test_email_address', TEST_EMAIL_ADDRESS
                ),
                'user_mailer': self.test_user_mailer.pk
            }
        )

    def _request_test_document_file_attachment_send_multiple_view(self):
        return self.post(
            viewname='mailer:send_document_file_attachment_multiple', query={
                'id_list': self.test_document_file.pk
            }, data={
                'email': getattr(
                    self, 'test_email_address', TEST_EMAIL_ADDRESS
                ),
                'user_mailer': self.test_user_mailer.pk
            }
        )


class DocumentVersionMailerViewTestMixin:
    def _request_test_document_version_send_link_single_view(self):
        return self.post(
            viewname='mailer:send_document_version_link_single', kwargs={
                'document_version_id': self.test_document_version.pk
            }, data={
                'email': getattr(
                    self, 'test_email_address', TEST_EMAIL_ADDRESS
                ),
                'user_mailer': self.test_user_mailer.pk
            },
        )

    def _request_test_document_version_send_link_multiple_view(self):
        return self.post(
            viewname='mailer:send_document_version_link_multiple', query={
                'id_list': self.test_document_version.pk
            }, data={
                'email': getattr(
                    self, 'test_email_address', TEST_EMAIL_ADDRESS
                ),
                'user_mailer': self.test_user_mailer.pk
            },
        )

    def _request_test_document_version_attachment_send_single_view(self):
        return self.post(
            viewname='mailer:send_document_version_attachment_single',
            kwargs={
                'document_version_id': self.test_document_version.pk
            }, data={
                'email': getattr(
                    self, 'test_email_address', TEST_EMAIL_ADDRESS
                ),
                'user_mailer': self.test_user_mailer.pk
            }
        )

    def _request_test_document_version_attachment_send_multiple_view(self):
        return self.post(
            viewname='mailer:send_document_version_attachment_multiple',
            query={
                'id_list': self.test_document_version.pk
            }, data={
                'email': getattr(
                    self, 'test_email_address', TEST_EMAIL_ADDRESS
                ),
                'user_mailer': self.test_user_mailer.pk
            }
        )


class MailerTestMixin:
    def _create_test_user_mailer(self):
        self.test_user_mailer = UserMailer.objects.create(
            default=True,
            enabled=True,
            label=TEST_USER_MAILER_LABEL,
            backend_path=TEST_USER_MAILER_BACKEND_PATH,
            backend_data=json.dumps(
                obj={
                    'from': TEST_EMAIL_FROM_ADDRESS
                }
            )
        )


class MailerViewTestMixin:
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
                'mailer_id': self.test_user_mailer.pk
            }
        )

    def _request_test_user_mailer_list_view(self):
        return self.get(
            viewname='mailer:user_mailer_list'
        )

    def _request_test_user_mailer_log_entry_view(self):
        return self.get(
            viewname='mailer:user_mailer_log', kwargs={
                'mailer_id': self.test_user_mailer.pk
            }
        )

    def _request_test_user_mailer_test_view(self):
        return self.post(
            viewname='mailer:user_mailer_test', kwargs={
                'mailer_id': self.test_user_mailer.pk
            }, data={
                'email': getattr(
                    self, 'test_email_address', TEST_EMAIL_ADDRESS
                )
            }
        )
