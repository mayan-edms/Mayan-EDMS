import logging

from django.contrib import messages
from django.template import RequestContext
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _, ungettext

from mayan.apps.views.generics import (
    MultipleObjectConfirmActionView, SingleObjectCreateView,
    SingleObjectEditView, SingleObjectListView
)

from .icons import icon_message_list
from .links import link_message_create
from .models import Message
from .permissions import (
    permission_message_create, permission_message_delete,
    permission_message_edit, permission_message_view
)

logger = logging.getLogger(name=__name__)


class MessageCreateView(SingleObjectCreateView):
    fields = ('label', 'message', 'enabled', 'start_datetime', 'end_datetime')
    model = Message
    view_permission = permission_message_create

    def get_extra_context(self):
        return {
            'title': _('Create message'),
        }


class MessageDeleteView(MultipleObjectConfirmActionView):
    model = Message
    object_permission = permission_message_delete
    pk_url_kwarg = 'message_id'
    post_action_redirect = reverse_lazy(viewname='motd:message_list')
    success_message = _('Delete request performed on %(count)d message')
    success_message_plural = _(
        'Delete request performed on %(count)d messages'
    )

    def get_extra_context(self):
        result = {
            'delete_view': True,
            'title': ungettext(
                singular='Delete the selected message?',
                plural='Delete the selected messages?',
                number=self.object_list.count()
            )
        }

        if self.object_list.count() == 1:
            result.update(
                {
                    'object': self.object_list.first(),
                    'title': _('Delete message: %s?') % self.object_list.first()
                }
            )

        return result

    def object_action(self, instance, form=None):
        try:
            instance.delete()
            messages.success(
                message=_(
                    'Message "%s" deleted successfully.'
                ) % instance, request=self.request
            )
        except Exception as exception:
            messages.error(
                message=_('Error deleting message "%(message)s": %(error)s') % {
                    'message': instance, 'error': exception
                }, request=self.request
            )


class MessageEditView(SingleObjectEditView):
    fields = ('label', 'message', 'enabled', 'start_datetime', 'end_datetime')
    model = Message
    object_permission = permission_message_edit
    pk_url_kwarg = 'message_id'
    post_action_redirect = reverse_lazy(viewname='motd:message_list')

    def get_extra_context(self):
        return {
            'object': self.object,
            'title': _('Edit message: %s') % self.object,
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
