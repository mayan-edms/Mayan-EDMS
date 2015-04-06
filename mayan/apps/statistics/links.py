from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from navigation import Link


def is_superuser(context):
    return context['request'].user.is_staff or context['request'].user.is_superuser


link_execute = Link(condition=is_superuser, text=_('Execute'), view='statistics:execute', args='object.id')
link_namespace_details = Link(text=_('Namespace details'), view='statistics:namespace_details', args='resolved_object.id', condition=is_superuser)
link_namespace_list = Link(condition=is_superuser, text=_('Namespace list'), view='statistics:namespace_list')
link_statistics = Link(condition=is_superuser, icon='fa fa-sort-numeric-desc', text=_('Statistics'), view='statistics:namespace_list')
