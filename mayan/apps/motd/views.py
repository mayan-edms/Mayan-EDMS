from __future__ import absolute_import, unicode_literals

import logging

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _, ungettext

from common.views import (
    SingleObjectCreateView, SingleObjectDeleteView, SingleObjectEditView,
    SingleObjectListView
)

from .models import MessageOfTheDay
from .permissions import (
    permission_message_create, permission_message_delete, permission_message_edit,
    permission_message_view,
)

logger = logging.getLogger(__name__)


class MessageCreateView(SingleObjectCreateView):
    fields = ('label',)
    model = Message
    view_permission = permission_message_create

    def get_extra_context(self):
        return {
            'object_name': _('Message'),
            'title': _('Create message'),
        }


class MessageDeleteView(SingleObjectDeleteView):
    model = Message
    object_permission = permission_message_delete
    post_action_redirect = reverse_lazy('messages:message_list')

    def get_extra_context(self):
        return {
            'object_name': _('Message'),
            'object': self.get_object(),
            'title': _('Delete the message: %s?') % self.get_object(),
        }


class MessageEditView(SingleObjectEditView):
    fields = ('label',)
    model = Message
    object_permission = permission_message_edit
    post_action_redirect = reverse_lazy('messages:message_list')

    def get_extra_context(self):
        return {
            'object': self.get_object(),
            'object_name': _('Message'),
            'title': _('Edit message: %s') % self.get_object(),
        }


class MessageListView(SingleObjectListView):
    model = Message
    object_permission = permission_message_view

    def get_extra_context(self):
        return {
            'hide_link': True,
            'title': _('Messages'),
