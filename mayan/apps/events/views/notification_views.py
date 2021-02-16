from django.contrib import messages
from django.template import RequestContext
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from mayan.apps.views.generics import ConfirmView, SingleObjectListView

from ..icons import icon_user_notifications_list
from ..links import link_event_types_subscriptions_list

__all__ = (
    'NotificationListView', 'NotificationMarkRead', 'NotificationMarkReadAll'
)


class NotificationListView(SingleObjectListView):
    def get_extra_context(self):
        return {
            'hide_object': True,
            'no_results_icon': icon_user_notifications_list,
            'no_results_main_link': link_event_types_subscriptions_list.resolve(
                context=RequestContext(request=self.request)
            ),
            'no_results_text': _(
                'Subscribe to global or object events to receive '
                'notifications.'
            ),
            'no_results_title': _('There are no notifications'),
            'object': self.request.user,
            'title': _('Notifications'),
        }

    def get_source_queryset(self):
        return self.request.user.notifications.all()


class NotificationMarkRead(ConfirmView):
    post_action_redirect = reverse_lazy(
        viewname='events:user_notifications_list'
    )

    def get_extra_context(self):
        return {
            'title': _('Mark the selected notification as read?')
        }

    def get_queryset(self):
        return self.request.user.notifications.all()

    def view_action(self, form=None):
        self.get_queryset().filter(
            pk=self.kwargs['notification_id']
        ).update(read=True)

        messages.success(
            message=_('Notification marked as read.'), request=self.request
        )


class NotificationMarkReadAll(ConfirmView):
    post_action_redirect = reverse_lazy(
        viewname='events:user_notifications_list'
    )

    def get_extra_context(self):
        return {
            'title': _('Mark all notification as read?')
        }

    def get_queryset(self):
        return self.request.user.notifications.all()

    def view_action(self, form=None):
        self.get_queryset().update(read=True)

        messages.success(
            message=_('All notifications marked as read.'),
            request=self.request
        )
