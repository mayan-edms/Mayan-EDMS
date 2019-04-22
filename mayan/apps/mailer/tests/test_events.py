from __future__ import unicode_literals

from django.core import mail

from actstream.models import Action

from mayan.apps.common.tests import GenericViewTestCase
from mayan.apps.documents.tests import DocumentTestMixin

from ..permissions import (
    permission_mailing_send_document, permission_user_mailer_use
)

from ..events import event_email_sent

from .mixins import MailerTestMixin, MailerViewTestMixin


class MailerEventsTestCase(DocumentTestMixin, MailerTestMixin, MailerViewTestMixin, GenericViewTestCase):
    auto_upload_document = False

    def setUp(self):
        super(MailerEventsTestCase, self).setUp()
        self._create_test_user_mailer()

    def test_email_send_event(self):
        Action.objects.all().delete()

        self.grant_access(
            obj=self.test_user_mailer, permission=permission_user_mailer_use
        )

        response = self._request_test_user_mailer_test_view()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)

        self.assertEqual(Action.objects.last().target, self.test_user_mailer)
        self.assertEqual(Action.objects.last().verb, event_email_sent.id)
        self.assertEqual(Action.objects.last().action_object, None)

    def test_document_email_send_event(self):
        self.upload_document()
        Action.objects.all().delete()

        self.grant_access(
            obj=self.test_user_mailer, permission=permission_user_mailer_use
        )
        self.grant_access(
            obj=self.test_document, permission=permission_mailing_send_document
        )

        response = self._request_test_document_send_view()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)

        self.assertEqual(Action.objects.last().target, self.test_user_mailer)
        self.assertEqual(Action.objects.last().verb, event_email_sent.id)
        self.assertEqual(Action.objects.last().action_object, self.test_document)
