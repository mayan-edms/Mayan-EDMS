from __future__ import absolute_import, unicode_literals

from django.core import mail

from documents.tests.test_models import GenericDocumentTestCase

from .literals import (
    TEST_BODY_HTML, TEST_EMAIL_ADDRESS, TEST_RECIPIENTS_MULTIPLE_COMMA,
    TEST_RECIPIENTS_MULTIPLE_COMMA_RESULT, TEST_RECIPIENTS_MULTIPLE_SEMICOLON,
    TEST_RECIPIENTS_MULTIPLE_SEMICOLON_RESULT, TEST_RECIPIENTS_MULTIPLE_MIXED,
    TEST_RECIPIENTS_MULTIPLE_MIXED_RESULT,
)
from .mixins import MailerTestMixin


class ModelTestCase(MailerTestMixin, GenericDocumentTestCase):
    def test_send_simple(self):
        self._create_user_mailer()
        self.user_mailer.send(to=TEST_EMAIL_ADDRESS)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [TEST_EMAIL_ADDRESS])

    def test_send_simple_with_html(self):
        self._create_user_mailer()
        self.user_mailer.send(to=TEST_EMAIL_ADDRESS, body=TEST_BODY_HTML)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [TEST_EMAIL_ADDRESS])
        self.assertEqual(mail.outbox[0].alternatives[0][0], TEST_BODY_HTML)

    def test_send_attachment(self):
        self._create_user_mailer()
        self.user_mailer.send_document(
            to=TEST_EMAIL_ADDRESS, document=self.document, as_attachment=True
        )

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [TEST_EMAIL_ADDRESS])
        with self.document.open() as file_object:
            self.assertEqual(
                mail.outbox[0].attachments[0], (
                    self.document.label, file_object.read(),
                    self.document.file_mimetype
                )
            )

    def test_send_multiple_recipients_comma(self):
        self._create_user_mailer()
        self.user_mailer.send(to=TEST_RECIPIENTS_MULTIPLE_COMMA)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].to, TEST_RECIPIENTS_MULTIPLE_COMMA_RESULT
        )

    def test_send_multiple_recipients_semicolon(self):
        self._create_user_mailer()
        self.user_mailer.send(to=TEST_RECIPIENTS_MULTIPLE_SEMICOLON)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].to, TEST_RECIPIENTS_MULTIPLE_SEMICOLON_RESULT
        )

    def test_send_multiple_recipient_mixed(self):
        self._create_user_mailer()
        self.user_mailer.send(to=TEST_RECIPIENTS_MULTIPLE_MIXED)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].to, TEST_RECIPIENTS_MULTIPLE_MIXED_RESULT
        )
