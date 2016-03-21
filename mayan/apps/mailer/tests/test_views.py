# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.core import mail
from django.test import override_settings
from django.utils.six import BytesIO

from common.tests.test_views import GenericViewTestCase
from documents.tests.test_views import GenericDocumentViewTestCase
from user_management.tests.literals import (
    TEST_USER_PASSWORD, TEST_USER_USERNAME
)

from ..models import LogEntry
from ..permissions import (
    permission_mailing_link, permission_mailing_send_document,
    permission_view_error_log
)

TEST_EMAIL_ADDRESS = 'test@example.com'


class MailerViewsTestCase(GenericDocumentViewTestCase):
    def test_mail_link_view_no_permissions(self):
        self.login(
            username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD
        )

        response = self.post(
            'mailer:send_document_link', args=(self.document.pk,),
            data={'email': TEST_EMAIL_ADDRESS},
        )

        self.assertEqual(response.status_code, 302)

    def test_mail_link_view_with_permission(self):
        self.login(
            username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD
        )

        self.role.permissions.add(
            permission_mailing_link.stored_permission
        )
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
