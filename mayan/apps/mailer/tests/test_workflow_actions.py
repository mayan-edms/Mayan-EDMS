import json

from django.core import mail

from mayan.apps.documents.tests.base import GenericDocumentTestCase
from mayan.apps.documents.tests.mixins.document_mixins import DocumentTestMixin
from mayan.apps.document_states.literals import WORKFLOW_ACTION_ON_ENTRY
from mayan.apps.document_states.permissions import permission_workflow_template_edit
from mayan.apps.document_states.tests.base import ActionTestCase
from mayan.apps.document_states.tests.mixins.workflow_template_mixins import WorkflowTemplateTestMixin
from mayan.apps.document_states.tests.mixins.workflow_template_state_mixins import WorkflowTemplateStateActionViewTestMixin
from mayan.apps.metadata.tests.mixins import MetadataTypeTestMixin
from mayan.apps.testing.tests.base import GenericViewTestCase

from ..permissions import permission_user_mailer_use
from ..workflow_actions import EmailAction

from .literals import (
    TEST_EMAIL_ADDRESS, TEST_EMAIL_BODY, TEST_EMAIL_FROM_ADDRESS,
    TEST_EMAIL_SUBJECT
)
from .mixins import MailerTestMixin


class EmailActionTestCase(
    MailerTestMixin, WorkflowTemplateTestMixin, GenericDocumentTestCase
):
    auto_upload_test_document = False

    def test_email_action_literal_text(self):
        self._create_test_document_stub()
        self._create_test_user_mailer()

        action = EmailAction(
            form_data={
                'mailing_profile': self.test_user_mailer.pk,
                'recipient': TEST_EMAIL_ADDRESS,
                'subject': TEST_EMAIL_SUBJECT,
                'body': TEST_EMAIL_BODY,
            }
        )
        action.execute(context={'document': self.test_document})
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, TEST_EMAIL_FROM_ADDRESS)
        self.assertEqual(mail.outbox[0].to, [TEST_EMAIL_ADDRESS])

    def test_email_action_literal_text_cc_field(self):
        self._create_test_document_stub()
        self._create_test_user_mailer()

        action = EmailAction(
            form_data={
                'mailing_profile': self.test_user_mailer.pk,
                'recipient': TEST_EMAIL_ADDRESS,
                'cc': TEST_EMAIL_ADDRESS,
                'subject': TEST_EMAIL_SUBJECT,
                'body': TEST_EMAIL_BODY,
            }
        )
        action.execute(context={'document': self.test_document})
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, TEST_EMAIL_FROM_ADDRESS)
        self.assertEqual(mail.outbox[0].to, [TEST_EMAIL_ADDRESS])
        self.assertEqual(mail.outbox[0].cc, [TEST_EMAIL_ADDRESS])

    def test_email_action_literal_text_bcc_field(self):
        self._create_test_document_stub()
        self._create_test_user_mailer()

        action = EmailAction(
            form_data={
                'mailing_profile': self.test_user_mailer.pk,
                'recipient': TEST_EMAIL_ADDRESS,
                'bcc': TEST_EMAIL_ADDRESS,
                'subject': TEST_EMAIL_SUBJECT,
                'body': TEST_EMAIL_BODY,
            }
        )
        action.execute(context={'document': self.test_document})
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, TEST_EMAIL_FROM_ADDRESS)
        self.assertEqual(mail.outbox[0].to, [TEST_EMAIL_ADDRESS])
        self.assertEqual(mail.outbox[0].bcc, [TEST_EMAIL_ADDRESS])

    def test_email_action_workflow_execute(self):
        self._create_test_workflow_template()
        self._create_test_workflow_template_state()
        self._create_test_user_mailer()

        self.test_workflow_template_state.actions.create(
            action_data=json.dumps(
                obj={
                    'mailing_profile': self.test_user_mailer.pk,
                    'recipient': TEST_EMAIL_ADDRESS,
                    'subject': TEST_EMAIL_SUBJECT,
                    'body': TEST_EMAIL_BODY,
                }
            ),
            action_path='mayan.apps.mailer.workflow_actions.EmailAction',
            label='test email action', when=WORKFLOW_ACTION_ON_ENTRY,
        )

        self.test_workflow_template_state.initial = True
        self.test_workflow_template_state.save()
        self.test_workflow_template.document_types.add(self.test_document_type)

        self._create_test_document_stub()

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, TEST_EMAIL_FROM_ADDRESS)
        self.assertEqual(mail.outbox[0].to, [TEST_EMAIL_ADDRESS])


class EmailActionTemplateTestCase(
    MetadataTypeTestMixin, MailerTestMixin, WorkflowTemplateTestMixin, ActionTestCase
):
    def test_email_action_recipient_template(self):
        self._create_test_metadata_type()
        self.test_document_type.metadata.create(
            metadata_type=self.test_metadata_type
        )
        self.test_document.metadata.create(
            metadata_type=self.test_metadata_type, value=TEST_EMAIL_ADDRESS
        )

        self._create_test_user_mailer()

        action = EmailAction(
            form_data={
                'mailing_profile': self.test_user_mailer.pk,
                'recipient': '{{{{ document.metadata_value_of.{} }}}}'.format(
                    self.test_metadata_type.name
                ),
                'subject': TEST_EMAIL_SUBJECT,
                'body': '',
            }
        )
        action.execute(context={'document': self.test_document})
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, TEST_EMAIL_FROM_ADDRESS)
        self.assertEqual(
            mail.outbox[0].to, [self.test_document.metadata.first().value]
        )

    def test_email_action_subject_template(self):
        self._create_test_metadata_type()
        self.test_document_type.metadata.create(
            metadata_type=self.test_metadata_type
        )
        self.test_document.metadata.create(
            metadata_type=self.test_metadata_type, value=TEST_EMAIL_SUBJECT
        )

        self._create_test_user_mailer()

        action = EmailAction(
            form_data={
                'mailing_profile': self.test_user_mailer.pk,
                'recipient': TEST_EMAIL_ADDRESS,
                'subject': '{{{{ document.metadata_value_of.{} }}}}'.format(
                    self.test_metadata_type.name
                ),
                'body': '',
            }
        )
        action.execute(context={'document': self.test_document})
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, TEST_EMAIL_FROM_ADDRESS)
        self.assertEqual(mail.outbox[0].to, [TEST_EMAIL_ADDRESS])
        self.assertEqual(
            mail.outbox[0].subject, self.test_document.metadata.first().value
        )

    def test_email_action_body_template(self):
        self._create_test_metadata_type()
        self.test_document_type.metadata.create(
            metadata_type=self.test_metadata_type
        )
        self.test_document.metadata.create(
            metadata_type=self.test_metadata_type, value=TEST_EMAIL_BODY
        )

        self._create_test_user_mailer()

        action = EmailAction(
            form_data={
                'mailing_profile': self.test_user_mailer.pk,
                'recipient': TEST_EMAIL_ADDRESS,
                'subject': TEST_EMAIL_SUBJECT,
                'body': '{{{{ document.metadata_value_of.{} }}}}'.format(
                    self.test_metadata_type.name
                ),
            }
        )
        action.execute(context={'document': self.test_document})
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, TEST_EMAIL_FROM_ADDRESS)
        self.assertEqual(mail.outbox[0].to, [TEST_EMAIL_ADDRESS])
        self.assertEqual(mail.outbox[0].body, TEST_EMAIL_BODY)

    def test_email_action_attachment(self):
        self._create_test_metadata_type()
        self.test_document_type.metadata.create(
            metadata_type=self.test_metadata_type
        )
        self.test_document.metadata.create(
            metadata_type=self.test_metadata_type, value=TEST_EMAIL_SUBJECT
        )

        self._create_test_user_mailer()

        action = EmailAction(
            form_data={
                'mailing_profile': self.test_user_mailer.pk,
                'recipient': TEST_EMAIL_ADDRESS,
                'subject': '{{{{ document.metadata_value_of.{} }}}}'.format(
                    self.test_metadata_type.name
                ),
                'body': '',
                'attachment': True
            }
        )
        action.execute(context={'document': self.test_document})
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, TEST_EMAIL_FROM_ADDRESS)
        self.assertEqual(mail.outbox[0].to, [TEST_EMAIL_ADDRESS])
        self.assertEqual(
            mail.outbox[0].subject, self.test_document.metadata.first().value
        )
        self.assertEqual(len(mail.outbox[0].attachments), 1)


class EmailActionViewTestCase(
    DocumentTestMixin, MailerTestMixin, WorkflowTemplateStateActionViewTestMixin,
    WorkflowTemplateTestMixin, GenericViewTestCase
):
    auto_upload_test_document = False

    def test_email_action_create_get_view(self):
        self._create_test_workflow_template()
        self._create_test_workflow_template_state()
        self._create_test_user_mailer()
        self.grant_access(
            obj=self.test_workflow_template, permission=permission_workflow_template_edit
        )

        response = self._request_test_workflow_template_state_action_create_get_view(
            class_path='mayan.apps.mailer.workflow_actions.EmailAction'
        )
        self.assertEqual(response.status_code, 200)

        self.assertEqual(self.test_workflow_template_state.actions.count(), 0)

    def test_email_action_create_post_view(self):
        self._create_test_workflow_template()
        self._create_test_workflow_template_state()
        self._create_test_user_mailer()
        self.grant_access(
            obj=self.test_user_mailer, permission=permission_user_mailer_use
        )
        self.grant_access(
            obj=self.test_workflow_template, permission=permission_workflow_template_edit
        )

        response = self._request_test_workflow_template_state_action_create_post_view(
            class_path='mayan.apps.mailer.workflow_actions.EmailAction',
            extra_data={
                'mailing_profile': self.test_user_mailer.pk,
                'recipient': TEST_EMAIL_ADDRESS,
                'subject': TEST_EMAIL_SUBJECT,
                'body': TEST_EMAIL_BODY,
            }
        )
        self.assertEqual(response.status_code, 302)

        self.assertEqual(self.test_workflow_template_state.actions.count(), 1)
