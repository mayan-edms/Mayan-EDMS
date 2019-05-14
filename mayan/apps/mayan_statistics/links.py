from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link

from .permissions import permission_statistics_view

# Translators: 'Queue' here is the verb, to queue a statistic to update
link_execute = Link(
    icon_class_path='mayan.apps.mayan_statistics.icons.icon_execute',
    permissions=(permission_statistics_view,), text=_('Queue'),
    view='statistics:statistic_queue', args='resolved_object.slug'
)
link_view = Link(
    icon_class_path='mayan.apps.mayan_statistics.icons.icon_view',
    permissions=(permission_statistics_view,), text=_('View'),
    view='statistics:statistic_detail', args='resolved_object.slug'
)
link_namespace_details = Link(
    icon_class_path='mayan.apps.mayan_statistics.icons.icon_namespace_details',
    permissions=(permission_statistics_view,), text=_('Namespace details'),
    view='statistics:namespace_details', args='resolved_object.slug'
)
link_namespace_list = Link(
    icon_class_path='mayan.apps.mayan_statistics.icons.icon_namespace_list',
    permissions=(permission_statistics_view,), text=_('Namespace list'),
    view='statistics:namespace_list'
)
link_statistics = Link(
    icon_class_path='mayan.apps.mayan_statistics.icons.icon_statistics',
    permissions=(permission_statistics_view,),
    text=_('Statistics'), view='statistics:namespace_list'
)
