from __future__ import unicode_literals

from organizations.tests.test_organization_views import OrganizationViewTestCase

from ..models import Message

from .literals import (
    TEST_MESSAGE_LABEL, TEST_MESSAGE_LABEL_EDITED, TEST_MESSAGE_TEXT
)


class MessageOrganizationViewTestCase(OrganizationViewTestCase):
    def create_message(self):
        with self.settings(ORGANIZATION_ID=self.organization_a.pk):
            self.message = Message.on_organization.create(
                label=TEST_MESSAGE_LABEL, message=TEST_MESSAGE_TEXT
            )

    def test_message_create_view(self):
        # Create a message for organization A
        with self.settings(ORGANIZATION_ID=self.organization_a.pk):
            response = self.post(
                'motd:message_create', data={
                    'label': TEST_MESSAGE_LABEL, 'message': TEST_MESSAGE_TEXT
                }
            )
            self.assertNotContains(response, text='danger', status_code=302)
            self.assertEqual(Message.on_organization.count(), 1)

        with self.settings(ORGANIZATION_ID=self.organization_b.pk):
            self.assertEqual(Message.on_organization.count(), 0)

    def test_message_delete_view(self):
        # Create a message for organization A
        self.create_message()

        with self.settings(ORGANIZATION_ID=self.organization_b.pk):
            response = self.post(
                'motd:message_delete', args=(self.message.pk,)
            )
            self.assertEqual(response.status_code, 404)

    def test_message_edit_view(self):
        # Create a message for organization A
        self.create_message()

        with self.settings(ORGANIZATION_ID=self.organization_b.pk):
            # Make sure admin for organization B cannot edit the message
            response = self.post(
                'motd:message_edit', args=(self.message.pk,), data={
                    'label': TEST_MESSAGE_LABEL_EDITED
                }
            )

            self.assertEqual(response.status_code, 404)

    def test_message_messageged_item_list_view(self):
        # Create a message for organization A
        self.create_message()

        with self.settings(ORGANIZATION_ID=self.organization_b.pk):
            # Make sure admin for organization B cannot find the message for
            # organization A
            response = self.get('motd:message_list')
            self.assertNotContains(
                response, text=self.message.label, status_code=200
            )
