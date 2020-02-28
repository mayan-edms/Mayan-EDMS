from __future__ import unicode_literals

from ..models import Message

from .literals import (
    TEST_LABEL, TEST_LABEL_EDITED, TEST_MESSAGE, TEST_MESSAGE_EDITED
)


class MessageAPITestMixin(object):
    def _request_test_message_create_api_view(self):
        return self.post(
            viewname='rest_api:message-list', data={
                'label': TEST_LABEL, 'message': TEST_MESSAGE
            }
        )

    def _request_test_message_destroy_api_view(self):
        return self.delete(
            viewname='rest_api:message-detail', kwargs={
                'message_id': self.test_message.pk
            }
        )

    def _request_test_message_list_api_view(self):
        return self.get(viewname='rest_api:message-list')

    def _request_test_message_partial_update_api_view(self):
        return self.patch(
            viewname='rest_api:message-detail', kwargs={
                'message_id': self.test_message.pk
            }, data={
                'label': TEST_LABEL_EDITED,
                'message': TEST_MESSAGE_EDITED
            }
        )

    def _request_test_message_retrieve_api_view(self):
        return self.get(
            viewname='rest_api:message-detail', kwargs={
                'message_id': self.test_message.pk
            }
        )

    def _request_test_message_update_api_view(self):
        return self.put(
            viewname='rest_api:message-detail', kwargs={
                'message_id': self.test_message.pk
            }, data={
                'label': TEST_LABEL_EDITED,
                'message': TEST_MESSAGE_EDITED
            }
        )


class MessageTestMixin(object):
    def _create_test_message(self):
        self.test_message = Message.objects.create(
            label=TEST_LABEL, message=TEST_MESSAGE
        )


class MessageViewTestMixin(object):
    def _request_test_message_create_view(self):
        return self.post(
            viewname='motd:message_create', data={
                'label': TEST_LABEL,
                'message': TEST_MESSAGE
            }
        )

    def _request_test_message_delete_view(self):
        return self.post(
            viewname='motd:message_delete', kwargs={
                'message_id': self.test_message.pk
            }
        )

    def _request_test_message_edit_view(self):
        return self.post(
            viewname='motd:message_edit', kwargs={
                'message_id': self.test_message.pk
            }, data={
                'label': TEST_LABEL_EDITED,
                'message': TEST_MESSAGE_EDITED
            }
        )

    def _request_test_message_list_view(self):
        return self.get(viewname='motd:message_list')
