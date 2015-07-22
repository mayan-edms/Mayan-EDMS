from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from navigation import Link


def is_superuser(context):
    return context['request'].user.is_staff or context['request'].user.is_superuser


link_namespace_list = Link(
    condition=is_superuser, icon='fa fa-sliders', text=_('Settings'),
    view='settings:namespace_list'
)
link_namespace_detail = Link(
    condition=is_superuser, text=_('Settings'),
    view='settings:namespace_detail', args='resolved_object.name'
)
