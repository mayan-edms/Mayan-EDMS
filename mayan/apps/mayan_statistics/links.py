from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link

from .icons import (
    icon_execute, icon_view, icon_namespace_details, icon_namespace_list,
    icon_statistics
)
from .permissions import permission_statistics_view

# Translators: 'Queue' here is the verb, to queue a statistic to update
link_execute = Link(
    args='resolved_object.slug', icon=icon_execute,
    permissions=(permission_statistics_view,), text=_('Queue'),
    view='statistics:statistic_queue'
)
link_view = Link(
    args='resolved_object.slug', icon=icon_view,
    permissions=(permission_statistics_view,), text=_('View'),
    view='statistics:statistic_detail'
)
link_namespace_details = Link(
    args='resolved_object.slug', icon=icon_namespace_details,
    permissions=(permission_statistics_view,), text=_('Namespace details'),
    view='statistics:namespace_details'
)
link_namespace_list = Link(
    icon=icon_namespace_list,
    permissions=(permission_statistics_view,), text=_('Namespace list'),
    view='statistics:namespace_list'
)
link_statistics = Link(
    icon=icon_statistics, permissions=(permission_statistics_view,),
    text=_('Statistics'), view='statistics:namespace_list'
)
