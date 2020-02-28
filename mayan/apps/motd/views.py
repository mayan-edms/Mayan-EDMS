from __future__ import absolute_import, unicode_literals

import logging

from django.template import RequestContext
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.generics import (
    SingleObjectCreateView, SingleObjectDeleteView, SingleObjectEditView,
    SingleObjectListView
)

from .icons import icon_message_list
from .links import link_message_create
from .models import Message
from .permissions import (
    permission_message_create, permission_message_delete,
    permission_message_edit, permission_message_view
)

logger = logging.getLogger(__name__)


class MessageCreateView(SingleObjectCreateView):
    fields = ('label', 'message', 'enabled', 'start_datetime', 'end_datetime')
    model = Message
    view_permission = permission_message_create

    def get_extra_context(self):
        return {
            'title': _('Create message'),
        }


class MessageDeleteView(SingleObjectDeleteView):
    model = Message
    object_permission = permission_message_delete
    pk_url_kwarg = 'message_id'
    post_action_redirect = reverse_lazy(viewname='motd:message_list')

    def get_extra_context(self):
        return {
            'message': None,
            'object': self.get_object(),
            'title': _('Delete the message: %s?') % self.get_object(),
        }


class MessageEditView(SingleObjectEditView):
    fields = ('label', 'message', 'enabled', 'start_datetime', 'end_datetime')
    model = Message
    object_permission = permission_message_edit
    pk_url_kwarg = 'message_id'
    post_action_redirect = reverse_lazy(viewname='motd:message_list')

    def get_extra_context(self):
        return {
            'object': self.get_object(),
            'title': _('Edit message: %s') % self.get_object(),
        }


class MessageListView(SingleObjectListView):
    model = Message
    object_permission = permission_message_view

    def get_extra_context(self):
        return {
            'hide_link': True,
            'hide_object': True,
            'no_results_icon': icon_message_list,
            'no_results_main_link': link_message_create.resolve(
                context=RequestContext(request=self.request)
            ),
            'no_results_text': _(
                'Messages are displayed in the login view. You can use '
                'messages to convery information about your organzation, '
                'announcements or usage guidelines for your users.'
            ),
            'no_results_title': _('No messages available'),
            'title': _('Messages'),
        }
