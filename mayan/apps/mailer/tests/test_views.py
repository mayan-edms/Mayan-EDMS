from django.core import mail

from mayan.apps.tests.tests.base import GenericViewTestCase
from mayan.apps.documents.tests.base import GenericDocumentViewTestCase

from ..models import UserMailer
from ..permissions import (
    permission_mailing_link, permission_mailing_send_document,
    permission_user_mailer_create, permission_user_mailer_delete,
    permission_user_mailer_use, permission_user_mailer_view
)

from .literals import (
    TEST_EMAIL_ADDRESS, TEST_EMAIL_FROM_ADDRESS, TEST_RECIPIENTS_MULTIPLE_COMMA,
    TEST_RECIPIENTS_MULTIPLE_COMMA_RESULT, TEST_RECIPIENTS_MULTIPLE_MIXED,
    TEST_RECIPIENTS_MULTIPLE_MIXED_RESULT, TEST_RECIPIENTS_MULTIPLE_SEMICOLON,
    TEST_RECIPIENTS_MULTIPLE_SEMICOLON_RESULT
)
from .mailers import TestBackend
from .mixins import MailerTestMixin, MailerViewTestMixin


class MailerViewsTestCase(MailerTestMixin, MailerViewTestMixin, GenericViewTestCase):
    def test_user_mailer_create_view_no_permissions(self):
        self.grant_permission(permission=permission_user_mailer_view)

        response = self._request_test_user_mailer_create_view()
        self.assertNotContains(
            response, text=TestBackend.label, status_code=403
        )

        self.assertEqual(UserMailer.objects.count(), 0)

    def test_user_mailer_create_view_with_permissions(self):
        self.grant_permission(permission=permission_user_mailer_create)
        self.grant_permission(permission=permission_user_mailer_view)

        response = self._request_test_user_mailer_create_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(UserMailer.objects.count(), 1)

    def test_user_mailer_delete_view_no_permissions(self):
        self._create_test_user_mailer()

        response = self._request_test_user_mailer_delete_view()
        self.assertEqual(response.status_code, 404)

        self.assertQuerysetEqual(
            UserMailer.objects.all(), (repr(self.test_user_mailer),)
        )

    def test_user_mailer_delete_view_with_access(self):
        self._create_test_user_mailer()

        self.grant_access(
            obj=self.test_user_mailer, permission=permission_user_mailer_delete
        )

        response = self._request_test_user_mailer_delete_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(UserMailer.objects.count(), 0)

    def test_user_mailer_list_view_no_permissions(self):
        self._create_test_user_mailer()

        response = self._request_test_user_mailer_list_view()
        self.assertNotContains(
            response, text=self.test_user_mailer.label, status_code=200
        )

    def test_user_mailer_list_view_with_access(self):
        self._create_test_user_mailer()

        self.grant_access(
            obj=self.test_user_mailer, permission=permission_user_mailer_view
        )

        response = self._request_test_user_mailer_list_view()
        self.assertContains(
            response=response, text=self.test_user_mailer.label, status_code=200
        )

    def test_user_mailer_list_bad_data_view_with_access(self):
        self._create_test_user_mailer()
        self.test_user_mailer.backend_path = 'bad.backend.path'
        self.test_user_mailer.backend_data = '{"bad_field": "bad_data"}'
        self.test_user_mailer.save()

        self.grant_access(
            obj=self.test_user_mailer, permission=permission_user_mailer_view
        )

        response = self._request_test_user_mailer_list_view()
        self.assertContains(
            response=response, text=self.test_user_mailer.label, status_code=200
        )

    def test_user_mailer_test_view_no_permissions(self):
        self._create_test_user_mailer()

        response = self._request_test_user_mailer_test_view()
        self.assertEqual(response.status_code, 404)

        self.assertEqual(len(mail.outbox), 0)

    def test_user_mailer_test_view_with_access(self):
        self._create_test_user_mailer()

        self.grant_access(
            obj=self.test_user_mailer, permission=permission_user_mailer_use
        )

        response = self._request_test_user_mailer_test_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, TEST_EMAIL_FROM_ADDRESS)
        self.assertEqual(mail.outbox[0].to, [TEST_EMAIL_ADDRESS])

    def test_send_multiple_recipients_comma(self):
        self._create_test_user_mailer()

        self.grant_access(
            obj=self.test_user_mailer, permission=permission_user_mailer_use
        )

        self.test_email_address = TEST_RECIPIENTS_MULTIPLE_COMMA
        response = self._request_test_user_mailer_test_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, TEST_EMAIL_FROM_ADDRESS)
        self.assertEqual(
            mail.outbox[0].to, TEST_RECIPIENTS_MULTIPLE_COMMA_RESULT
        )

    def test_send_multiple_recipients_mixed(self):
        self._create_test_user_mailer()

        self.grant_access(
            obj=self.test_user_mailer, permission=permission_user_mailer_use
        )

        self.test_email_address = TEST_RECIPIENTS_MULTIPLE_MIXED
        response = self._request_test_user_mailer_test_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, TEST_EMAIL_FROM_ADDRESS)
        self.assertEqual(
            mail.outbox[0].to, TEST_RECIPIENTS_MULTIPLE_MIXED_RESULT
        )

    def test_send_multiple_recipients_semicolon(self):
        self._create_test_user_mailer()

        self.grant_access(
            obj=self.test_user_mailer, permission=permission_user_mailer_use
        )

        self.test_email_address = TEST_RECIPIENTS_MULTIPLE_SEMICOLON

        response = self._request_test_user_mailer_test_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, TEST_EMAIL_FROM_ADDRESS)
        self.assertEqual(
            mail.outbox[0].to, TEST_RECIPIENTS_MULTIPLE_SEMICOLON_RESULT
        )


class MailDocumentViewsTestCase(MailerTestMixin, MailerViewTestMixin, GenericDocumentViewTestCase):
    def test_mail_link_view_no_permissions(self):
        self._create_test_user_mailer()

        response = self._request_test_document_link_send_view()
        self.assertEqual(response.status_code, 404)

    def test_mail_link_view_with_access(self):
        self._create_test_user_mailer()

        self.grant_access(
            obj=self.test_document, permission=permission_mailing_link
        )
        self.grant_access(
            obj=self.test_user_mailer, permission=permission_user_mailer_use
        )

        response = self._request_test_document_link_send_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, TEST_EMAIL_FROM_ADDRESS)
        self.assertEqual(mail.outbox[0].to, [TEST_EMAIL_ADDRESS])

    def test_mail_document_view_no_permissions(self):
        self._create_test_user_mailer()

        response = self._request_test_document_send_view()
        self.assertEqual(response.status_code, 404)

    def test_mail_document_view_with_access(self):
        self._create_test_user_mailer()

        self.grant_access(
            obj=self.test_document, permission=permission_mailing_send_document
        )
        self.grant_access(
            obj=self.test_user_mailer, permission=permission_user_mailer_use
        )

        response = self._request_test_document_send_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, TEST_EMAIL_FROM_ADDRESS)
        self.assertEqual(mail.outbox[0].to, [TEST_EMAIL_ADDRESS])

    def test_mail_link_view_recipients_comma(self):
        self._create_test_user_mailer()

        self.grant_access(
            obj=self.test_document, permission=permission_mailing_link
        )
        self.grant_access(
            obj=self.test_user_mailer, permission=permission_user_mailer_use
        )

        self.test_email_address = TEST_RECIPIENTS_MULTIPLE_COMMA

        response = self._request_test_document_link_send_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, TEST_EMAIL_FROM_ADDRESS)
        self.assertEqual(
            mail.outbox[0].to, TEST_RECIPIENTS_MULTIPLE_COMMA_RESULT
        )

    def test_mail_link_view_recipients_mixed(self):
        self._create_test_user_mailer()

        self.grant_access(
            obj=self.test_document, permission=permission_mailing_link
        )
        self.grant_access(
            obj=self.test_user_mailer, permission=permission_user_mailer_use
        )

        self.test_email_address = TEST_RECIPIENTS_MULTIPLE_MIXED

        response = self._request_test_document_link_send_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, TEST_EMAIL_FROM_ADDRESS)
        self.assertEqual(
            mail.outbox[0].to, TEST_RECIPIENTS_MULTIPLE_MIXED_RESULT
        )

    def test_mail_link_view_recipients_semicolon(self):
        self._create_test_user_mailer()

        self.grant_access(
            obj=self.test_document, permission=permission_mailing_link
        )
        self.grant_access(
            obj=self.test_user_mailer, permission=permission_user_mailer_use
        )

        self.test_email_address = TEST_RECIPIENTS_MULTIPLE_SEMICOLON

        response = self._request_test_document_link_send_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, TEST_EMAIL_FROM_ADDRESS)
        self.assertEqual(
            mail.outbox[0].to, TEST_RECIPIENTS_MULTIPLE_SEMICOLON_RESULT
        )

    def test_mail_document_view_recipients_comma(self):
        self._create_test_user_mailer()

        self.grant_access(
            obj=self.test_document, permission=permission_mailing_send_document
        )
        self.grant_access(
            obj=self.test_user_mailer, permission=permission_user_mailer_use
        )

        self.test_email_address = TEST_RECIPIENTS_MULTIPLE_COMMA

        response = self._request_test_document_send_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, TEST_EMAIL_FROM_ADDRESS)
        self.assertEqual(
            mail.outbox[0].to, TEST_RECIPIENTS_MULTIPLE_COMMA_RESULT
        )

    def test_mail_document_view_recipients_mixed(self):
        self._create_test_user_mailer()

        self.grant_access(
            obj=self.test_document, permission=permission_mailing_send_document
        )
        self.grant_access(
            obj=self.test_user_mailer, permission=permission_user_mailer_use
        )

        self.test_email_address = TEST_RECIPIENTS_MULTIPLE_MIXED

        response = self._request_test_document_send_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, TEST_EMAIL_FROM_ADDRESS)
        self.assertEqual(
            mail.outbox[0].to, TEST_RECIPIENTS_MULTIPLE_MIXED_RESULT
        )

    def test_mail_document_view_recipients_semicolon(self):
        self._create_test_user_mailer()

        self.grant_access(
            obj=self.test_document, permission=permission_mailing_send_document
        )
        self.grant_access(
            obj=self.test_user_mailer, permission=permission_user_mailer_use
        )

        self.test_email_address = TEST_RECIPIENTS_MULTIPLE_SEMICOLON

        response = self._request_test_document_send_view()
        self.assertEqual(response.status_code, 302)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, TEST_EMAIL_FROM_ADDRESS)
        self.assertEqual(
            mail.outbox[0].to, TEST_RECIPIENTS_MULTIPLE_SEMICOLON_RESULT
        )
