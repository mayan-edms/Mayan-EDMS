from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link

from .icons import (
    icon_statistic_detail, icon_statistic_queue,
    icon_statistic_namespace_detail, icon_statistic_namespace_list,
    icon_statistics
)
from .permissions import permission_statistics_view

# Translators: 'Queue' here is the verb, to queue a statistic to update.
link_statistic_queue = Link(
    args='resolved_object.slug', icon=icon_statistic_queue,
    permissions=(permission_statistics_view,), text=_('Queue'),
    view='statistics:statistic_queue'
)
link_statistic_detail = Link(
    args='resolved_object.slug', icon=icon_statistic_detail,
    permissions=(permission_statistics_view,), text=_('View'),
    view='statistics:statistic_detail'
)
link_statistic_namespace_detail = Link(
    args='resolved_object.slug', icon=icon_statistic_namespace_detail,
    permissions=(permission_statistics_view,), text=_('Namespace details'),
    view='statistics:statistic_namespace_detail'
)
link_statistic_namespace_list = Link(
    icon=icon_statistic_namespace_list,
    permissions=(permission_statistics_view,), text=_('Namespace list'),
    view='statistics:statistic_namespace_list'
)
link_statistics = Link(
    icon=icon_statistics, permissions=(permission_statistics_view,),
    text=_('Statistics'), view='statistics:statistic_namespace_list'
)
