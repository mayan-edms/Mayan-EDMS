from django.core import mail

from mayan.apps.documents.literals import DOCUMENT_VERSION_EXPORT_MIMETYPE
from mayan.apps.documents.tests.base import GenericDocumentTestCase
from mayan.apps.testing.tests.base import BaseTestCase

from ..events import event_email_sent
from ..literals import MODEL_SEND_FUNCTION_DOTTED_PATH

from .literals import (
    TEST_EMAIL_BODY_HTML, TEST_EMAIL_ADDRESS, TEST_EMAIL_FROM_ADDRESS,
    TEST_RECIPIENTS_MULTIPLE_COMMA, TEST_RECIPIENTS_MULTIPLE_COMMA_RESULT,
    TEST_RECIPIENTS_MULTIPLE_SEMICOLON,
    TEST_RECIPIENTS_MULTIPLE_SEMICOLON_RESULT, TEST_RECIPIENTS_MULTIPLE_MIXED,
    TEST_RECIPIENTS_MULTIPLE_MIXED_RESULT,
)
from .mixins import MailerTestMixin


class MailingModelTestCase(MailerTestMixin, BaseTestCase):
    def test_method_get_absolute_url(self):
        self._create_test_user_mailer()

        self.assertTrue(self.test_user_mailer.get_absolute_url())

    def test_send_simple(self):
        self._create_test_user_mailer()

        self._clear_events()

        self.test_user_mailer.send(to=TEST_EMAIL_ADDRESS)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, TEST_EMAIL_FROM_ADDRESS)
        self.assertEqual(mail.outbox[0].to, [TEST_EMAIL_ADDRESS])

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self.test_user_mailer)
        self.assertEqual(events[0].target, self.test_user_mailer)
        self.assertEqual(events[0].verb, event_email_sent.id)

    def test_send_simple_with_html(self):
        self._create_test_user_mailer()

        self._clear_events()

        self.test_user_mailer.send(
            to=TEST_EMAIL_ADDRESS, body=TEST_EMAIL_BODY_HTML
        )

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, TEST_EMAIL_FROM_ADDRESS)
        self.assertEqual(mail.outbox[0].to, [TEST_EMAIL_ADDRESS])
        self.assertEqual(
            mail.outbox[0].alternatives[0][0], TEST_EMAIL_BODY_HTML
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self.test_user_mailer)
        self.assertEqual(events[0].target, self.test_user_mailer)
        self.assertEqual(events[0].verb, event_email_sent.id)

    def test_send_multiple_recipients_comma(self):
        self._create_test_user_mailer()

        self._clear_events()

        self.test_user_mailer.send(to=TEST_RECIPIENTS_MULTIPLE_COMMA)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, TEST_EMAIL_FROM_ADDRESS)
        self.assertEqual(
            mail.outbox[0].to, TEST_RECIPIENTS_MULTIPLE_COMMA_RESULT
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self.test_user_mailer)
        self.assertEqual(events[0].target, self.test_user_mailer)
        self.assertEqual(events[0].verb, event_email_sent.id)

    def test_send_multiple_recipients_semicolon(self):
        self._create_test_user_mailer()

        self._clear_events()

        self.test_user_mailer.send(to=TEST_RECIPIENTS_MULTIPLE_SEMICOLON)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, TEST_EMAIL_FROM_ADDRESS)
        self.assertEqual(
            mail.outbox[0].to, TEST_RECIPIENTS_MULTIPLE_SEMICOLON_RESULT
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self.test_user_mailer)
        self.assertEqual(events[0].target, self.test_user_mailer)
        self.assertEqual(events[0].verb, event_email_sent.id)

    def test_send_multiple_recipient_mixed(self):
        self._create_test_user_mailer()

        self._clear_events()

        self.test_user_mailer.send(to=TEST_RECIPIENTS_MULTIPLE_MIXED)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, TEST_EMAIL_FROM_ADDRESS)
        self.assertEqual(
            mail.outbox[0].to, TEST_RECIPIENTS_MULTIPLE_MIXED_RESULT
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self.test_user_mailer)
        self.assertEqual(events[0].target, self.test_user_mailer)
        self.assertEqual(events[0].verb, event_email_sent.id)

    def test_send_to_cc(self):
        self._create_test_user_mailer()

        self._clear_events()

        self.test_user_mailer.send(
            cc=TEST_EMAIL_ADDRESS, to=TEST_EMAIL_ADDRESS
        )

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, TEST_EMAIL_FROM_ADDRESS)
        self.assertEqual(mail.outbox[0].to, [TEST_EMAIL_ADDRESS])
        self.assertEqual(mail.outbox[0].cc, [TEST_EMAIL_ADDRESS])

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self.test_user_mailer)
        self.assertEqual(events[0].target, self.test_user_mailer)
        self.assertEqual(events[0].verb, event_email_sent.id)

    def test_send_to_bcc(self):
        self._create_test_user_mailer()

        self._clear_events()

        self.test_user_mailer.send(
            bcc=TEST_EMAIL_ADDRESS, to=TEST_EMAIL_ADDRESS
        )

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, TEST_EMAIL_FROM_ADDRESS)
        self.assertEqual(mail.outbox[0].to, [TEST_EMAIL_ADDRESS])
        self.assertEqual(mail.outbox[0].bcc, [TEST_EMAIL_ADDRESS])

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self.test_user_mailer)
        self.assertEqual(events[0].target, self.test_user_mailer)
        self.assertEqual(events[0].verb, event_email_sent.id)

    def test_send_with_reply_to(self):
        self._create_test_user_mailer()

        self._clear_events()

        self.test_user_mailer.send(
            reply_to=TEST_EMAIL_ADDRESS, to=TEST_EMAIL_ADDRESS
        )

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, TEST_EMAIL_FROM_ADDRESS)
        self.assertEqual(mail.outbox[0].to, [TEST_EMAIL_ADDRESS])
        self.assertEqual(mail.outbox[0].reply_to, [TEST_EMAIL_ADDRESS])

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, None)
        self.assertEqual(events[0].actor, self.test_user_mailer)
        self.assertEqual(events[0].target, self.test_user_mailer)
        self.assertEqual(events[0].verb, event_email_sent.id)


class DocumentMailingTestCase(MailerTestMixin, GenericDocumentTestCase):
    def test_send_link(self):
        self._create_test_user_mailer()

        self._clear_events()

        self.test_user_mailer.send_object(
            obj=self.test_document, to=TEST_EMAIL_ADDRESS
        )

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, TEST_EMAIL_FROM_ADDRESS)
        self.assertEqual(mail.outbox[0].to, [TEST_EMAIL_ADDRESS])

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_document)
        self.assertEqual(events[0].actor, self.test_user_mailer)
        self.assertEqual(events[0].target, self.test_user_mailer)
        self.assertEqual(events[0].verb, event_email_sent.id)


class DocumentFileMailingTestCase(MailerTestMixin, GenericDocumentTestCase):
    def test_send_document_file_attachment(self):
        self._create_test_user_mailer()

        self._clear_events()

        kwargs = {
            'as_attachment': True, 'obj': self.test_document_file,
            'to': TEST_EMAIL_ADDRESS
        }
        kwargs.update(
            MODEL_SEND_FUNCTION_DOTTED_PATH.get(
                self.test_document_file._meta.model, {}
            )
        )

        self.test_user_mailer.send_object(**kwargs)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, TEST_EMAIL_FROM_ADDRESS)
        self.assertEqual(mail.outbox[0].to, [TEST_EMAIL_ADDRESS])
        self.assertEqual(
            mail.outbox[0].attachments[0][0],
            self.test_document_file.filename
        )
        self.assertEqual(
            mail.outbox[0].attachments[0][2],
            self.test_document_file.mimetype
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_document_file)
        self.assertEqual(events[0].actor, self.test_user_mailer)
        self.assertEqual(events[0].target, self.test_user_mailer)
        self.assertEqual(events[0].verb, event_email_sent.id)

    def test_send_document_file_link(self):
        self._create_test_user_mailer()

        self._clear_events()

        self.test_user_mailer.send_object(
            obj=self.test_document_file, to=TEST_EMAIL_ADDRESS
        )

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, TEST_EMAIL_FROM_ADDRESS)
        self.assertEqual(mail.outbox[0].to, [TEST_EMAIL_ADDRESS])
        self.assertEqual(len(mail.outbox[0].attachments), 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_document_file)
        self.assertEqual(events[0].actor, self.test_user_mailer)
        self.assertEqual(events[0].target, self.test_user_mailer)
        self.assertEqual(events[0].verb, event_email_sent.id)


class DocumentVersionMailingTestCase(
    MailerTestMixin, GenericDocumentTestCase
):
    def test_send_document_version_attachment(self):
        self._create_test_user_mailer()

        self._clear_events()

        kwargs = {
            'as_attachment': True, 'obj': self.test_document_version,
            'to': TEST_EMAIL_ADDRESS
        }
        kwargs.update(
            MODEL_SEND_FUNCTION_DOTTED_PATH.get(
                self.test_document_version._meta.model, {}
            )
        )

        self.test_user_mailer.send_object(**kwargs)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, TEST_EMAIL_FROM_ADDRESS)
        self.assertEqual(mail.outbox[0].to, [TEST_EMAIL_ADDRESS])
        self.assertEqual(
            mail.outbox[0].attachments[0][0],
            str(self.test_document_version)
        )
        self.assertEqual(
            mail.outbox[0].attachments[0][2],
            DOCUMENT_VERSION_EXPORT_MIMETYPE
        )

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_document_version)
        self.assertEqual(events[0].actor, self.test_user_mailer)
        self.assertEqual(events[0].target, self.test_user_mailer)
        self.assertEqual(events[0].verb, event_email_sent.id)

    def test_send_document_version_link(self):
        self._create_test_user_mailer()

        self._clear_events()

        self.test_user_mailer.send_object(
            obj=self.test_document_version,
            to=TEST_EMAIL_ADDRESS
        )

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, TEST_EMAIL_FROM_ADDRESS)
        self.assertEqual(mail.outbox[0].to, [TEST_EMAIL_ADDRESS])
        self.assertEqual(len(mail.outbox[0].attachments), 0)

        events = self._get_test_events()
        self.assertEqual(events.count(), 1)

        self.assertEqual(events[0].action_object, self.test_document_version)
        self.assertEqual(events[0].actor, self.test_user_mailer)
        self.assertEqual(events[0].target, self.test_user_mailer)
        self.assertEqual(events[0].verb, event_email_sent.id)
