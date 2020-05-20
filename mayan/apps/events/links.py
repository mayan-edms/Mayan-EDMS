from django.apps import apps
from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link

from .icons import (
    icon_events_list, icon_events_for_object,
    icon_event_types_subscriptions_list,
    icon_object_event_types_user_subcriptions_list,
    icon_user_notifications_list
)
from .permissions import permission_events_view


def get_kwargs_factory(variable_name):
    def get_kwargs(context):
        ContentType = apps.get_model(
            app_label='contenttypes', model_name='ContentType'
        )

        content_type = ContentType.objects.get_for_model(
            model=context[variable_name]
        )
        return {
            'app_label': '"{}"'.format(content_type.app_label),
            'model': '"{}"'.format(content_type.model),
            'object_id': '{}.pk'.format(variable_name)
        }

    return get_kwargs


def get_unread_notification_count(context):
    Notification = apps.get_model(
        app_label='events', model_name='Notification'
    )
    return Notification.objects.filter(
        user=context.request.user
    ).filter(read=False).count()


link_current_user_events = Link(
    icon_class=icon_events_list, text=_('My events'),
    view='events:current_user_events'
)
link_events_details = Link(
    text=_('Events'), view='events:events_list'
)
link_events_for_object = Link(
    icon_class=icon_events_for_object,
    kwargs=get_kwargs_factory('resolved_object'),
    permissions=(permission_events_view,), text=_('Events'),
    view='events:events_for_object',
)
link_events_list = Link(
    icon_class=icon_events_list, permissions=(permission_events_view,),
    text=_('Events'), view='events:events_list'
)
link_event_types_subscriptions_list = Link(
    icon_class=icon_event_types_subscriptions_list,
    text=_('Event subscriptions'),
    view='events:event_types_user_subcriptions_list'
)
link_notification_mark_read = Link(
    args='object.pk', text=_('Mark as seen'),
    view='events:notification_mark_read'
)
link_notification_mark_read_all = Link(
    text=_('Mark all as seen'), view='events:notification_mark_read_all'
)
link_object_event_types_user_subcriptions_list = Link(
    icon_class=icon_object_event_types_user_subcriptions_list,
    kwargs=get_kwargs_factory('resolved_object'),
    permissions=(permission_events_view,), text=_('Subscriptions'),
    view='events:object_event_types_user_subcriptions_list',
)
link_user_notifications_list = Link(
    badge_text=get_unread_notification_count,
    icon_class=icon_user_notifications_list, text='',
    view='events:user_notifications_list'
)
