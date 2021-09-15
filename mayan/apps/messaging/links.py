from django.apps import apps
from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link

from .icons import (
    icon_message_create, icon_message_delete, icon_message_list,
    icon_message_mark_read, icon_message_mark_read_all,
    icon_message_mark_unread
)
from .permissions import (
    permission_message_create, permission_message_delete,
    permission_message_view
)


def condition_is_read(context):
    return context['object'].read


def condition_is_unread(context):
    return not context['object'].read


def get_unread_message_count(context):
    Message = apps.get_model(
        app_label='messaging', model_name='Message'
    )
    if context.request.user.is_authenticated:
        return Message.objects.filter(
            user=context.request.user
        ).filter(read=False).count()


link_message_create = Link(
    icon=icon_message_create, permissions=(permission_message_create,),
    text=_('Create message'), view='messaging:message_create'
)
link_message_multiple_delete = Link(
    icon=icon_message_delete, tags='dangerous', text=_('Delete'),
    view='messaging:message_multiple_delete'
)
link_message_single_delete = Link(
    args='object.pk', icon=icon_message_delete,
    permissions=(permission_message_delete,),
    tags='dangerous', text=_('Delete'), view='messaging:message_single_delete'
)
link_message_list = Link(
    badge_text=get_unread_message_count, icon=icon_message_list,
    text='', view='messaging:message_list'
)
link_message_single_mark_read = Link(
    args='object.pk', conditional_disable=condition_is_read,
    icon=icon_message_mark_read, text=_('Mark as read'),
    permissions=(permission_message_view,),
    view='messaging:message_single_mark_read'
)
link_message_single_mark_unread = Link(
    args='object.pk', conditional_disable=condition_is_unread,
    icon=icon_message_mark_unread, text=_('Mark as unread'),
    permissions=(permission_message_view,),
    view='messaging:message_single_mark_unread'
)
link_message_multiple_mark_read = Link(
    icon=icon_message_mark_read, text=_('Mark as read'),
    view='messaging:message_multiple_mark_read'
)
link_message_multiple_mark_unread = Link(
    icon=icon_message_mark_unread, text=_('Mark as unread'),
    view='messaging:message_multiple_mark_unread'
)
link_message_all_mark_read = Link(
    icon=icon_message_mark_read_all, text=_('Mark all as read'),
    view='messaging:message_all_mark_read'
)
