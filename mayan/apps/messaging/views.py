import logging

from django.contrib import messages
from django.template import RequestContext
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.models import AccessControlList
from mayan.apps.views.generics import (
    ConfirmView, MultipleObjectConfirmActionView, SingleObjectCreateView,
    SingleObjectDetailView, SingleObjectListView
)

from .forms import MessageDetailForm
from .icons import icon_form_button_send, icon_message_list
from .links import link_message_create
from .models import Message
from .permissions import (
    permission_message_create, permission_message_delete,
    permission_message_view
)

logger = logging.getLogger(name=__name__)


class MessageCreateView(SingleObjectCreateView):
    fields = ('user', 'subject', 'body')
    model = Message
    view_permission = permission_message_create

    def get_extra_context(self):
        return {
            'title': _('Create message'),
            'submit_label': _('Send'),
            'submit_icon': icon_form_button_send,
        }

    def get_instance_extra_data(self):
        return {
            'sender_object': self.request.user,
            '_event_actor': self.request.user
        }


class MessageDeleteView(MultipleObjectConfirmActionView):
    error_message = _('Error deleting message "%(instance)s"; %(exception)s')
    object_permission = permission_message_delete
    pk_url_kwarg = 'message_id'
    post_action_redirect = reverse_lazy(viewname='messaging:message_list')
    success_message_single = _('Message "%(object)s" deleted successfully.')
    success_message_singular = _('%(count)d message deleted successfully.')
    success_message_plural = _('%(count)d messages deleted successfully.')
    title_single = _('Delete message: %(object)s.')
    title_singular = _('Delete the %(count)d selected message.')
    title_plural = _('Delete the %(count)d selected messages.')

    def get_extra_context(self):
        context = {
            'delete_view': True,
        }

        if self.object_list.count() == 1:
            context.update(
                {
                    'object': self.object_list.first()
                }
            )

        return context

    def get_source_queryset(self):
        return self.request.user.messages.all()

    def object_action(self, instance, form=None):
        instance.delete()


class MessageDetailView(SingleObjectDetailView):
    form_class = MessageDetailForm
    object_permission = permission_message_view
    pk_url_kwarg = 'message_id'

    def dispatch(self, request, *args, **kwargs):
        result = super().dispatch(request=request, *args, **kwargs)
        self.object._event_actor = self.request.user
        self.object.mark_read()
        return result

    def get_extra_context(self):
        return {
            'form_hide_help_text': True,
            'hide_labels': True,
            'object': self.object,
            'title': _('Details of message: %s') % self.object,
        }

    def get_initial(self):
        return {
            'body': self.object.get_rendered_body()
        }

    def get_source_queryset(self):
        return self.request.user.messages.all()


class MessageListView(SingleObjectListView):
    object_permission = permission_message_view

    def get_extra_context(self):
        return {
            'hide_object': True,
            'no_results_icon': icon_message_list,
            'no_results_main_link': link_message_create.resolve(
                context=RequestContext(request=self.request)
            ),
            'no_results_text': _(
                'Here you will find text messages from other users or from '
                'the system.'
            ),
            'no_results_title': _('There are no messages'),
            'object': self.request.user,
            'title': _('Messages'),
        }

    def get_source_queryset(self):
        return self.request.user.messages.all()


class MessageMarkReadView(MultipleObjectConfirmActionView):
    error_message = _(
        'Error marking message "%(instance)s" as read; %(exception)s'
    )
    object_permission = permission_message_view
    pk_url_kwarg = 'message_id'
    post_action_redirect = reverse_lazy(viewname='messaging:message_list')
    success_message_single = _(
        'Message "%(object)s" marked as read successfully.'
    )
    success_message_singular = _(
        '%(count)d message marked as read successfully.'
    )
    success_message_plural = _(
        '%(count)d messages marked as read successfully.'
    )
    title_single = _('Mark the message "%(object)s" as read.')
    title_singular = _('Mark the %(count)d selected message as read.')
    title_plural = _('Mark the %(count)d selected messages as read.')

    def get_extra_context(self):
        context = {}

        if self.object_list.count() == 1:
            context.update(
                {
                    'object': self.object_list.first()
                }
            )

        return context

    def get_source_queryset(self):
        return self.request.user.messages.all()

    def object_action(self, instance, form=None):
        instance._event_actor = self.request.user
        instance.mark_read()


class MessageMarkReadAllView(ConfirmView):
    post_action_redirect = reverse_lazy(viewname='messaging:message_list')

    def get_extra_context(self):
        return {
            'title': _('Mark all message as read?')
        }

    def get_queryset(self):
        return self.request.user.messages.all()

    def view_action(self, form=None):
        queryset = AccessControlList.objects.restrict_queryset(
            permission=permission_message_view, queryset=self.get_queryset(),
            user=self.request.user
        )

        for message in queryset.all():
            message._event_actor = self.request.user
            message.mark_read()

        messages.success(
            message=_('All messages marked as read.'),
            request=self.request
        )


class MessageMarkUnReadView(MultipleObjectConfirmActionView):
    error_message = _(
        'Error marking message "%(instance)s" as unread; %(exception)s'
    )
    object_permission = permission_message_view
    pk_url_kwarg = 'message_id'
    post_action_redirect = reverse_lazy(viewname='messaging:message_list')
    success_message_single = _(
        'Message "%(object)s" marked as unread successfully.'
    )
    success_message_singular = _(
        '%(count)d message marked as unread successfully.'
    )
    success_message_plural = _(
        '%(count)d messages marked as unread successfully.'
    )
    title_single = _('Mark the message "%(object)s" as unread.')
    title_singular = _('Mark the %(count)d selected message as unread.')
    title_plural = _('Mark the %(count)d selected messages as unread.')

    def get_extra_context(self):
        context = {}

        if self.object_list.count() == 1:
            context.update(
                {
                    'object': self.object_list.first()
                }
            )

        return context

    def get_source_queryset(self):
        return self.request.user.messages.all()

    def object_action(self, instance, form=None):
        instance._event_actor = self.request.user
        instance.mark_unread()
