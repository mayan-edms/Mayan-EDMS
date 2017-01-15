from __future__ import unicode_literals

from django.core import mail

from documents.tests.test_views import GenericDocumentViewTestCase

from ..permissions import (
    permission_mailing_link, permission_mailing_send_document
)

TEST_EMAIL_ADDRESS = 'test@example.com'


class MailerViewsTestCase(GenericDocumentViewTestCase):
    def test_mail_link_view_no_permissions(self):
        self.login_user()

        response = self.post(
            'mailer:send_document_link', args=(self.document.pk,),
            data={'email': TEST_EMAIL_ADDRESS},
        )

        self.assertEqual(response.status_code, 302)

    def test_mail_link_view_with_permission(self):
        self.login_user()

        self.grant(permission_mailing_link)

        response = self.post(
            'mailer:send_document_link', args=(self.document.pk,),
            data={'email': TEST_EMAIL_ADDRESS},
            follow=True
        )

        self.assertContains(
            response, 'queued', status_code=200
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [TEST_EMAIL_ADDRESS])

    def test_mail_document_view_no_permissions(self):
        self.login_user()

        response = self.post(
            'mailer:send_document', args=(self.document.pk,),
            data={'email': TEST_EMAIL_ADDRESS},
        )

        self.assertEqual(response.status_code, 302)

    def test_mail_document_view_with_permission(self):
        self.login_user()

        self.grant(permission_mailing_send_document)

        response = self.post(
            'mailer:send_document', args=(self.document.pk,),
            data={'email': TEST_EMAIL_ADDRESS},
            follow=True
        )

        self.assertContains(
            response, 'queued', status_code=200
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [TEST_EMAIL_ADDRESS])
