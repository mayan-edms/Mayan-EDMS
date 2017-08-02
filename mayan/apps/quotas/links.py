from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from navigation import Link

from .permissions import (
    permission_quota_create, permission_quota_delete,
    permission_quota_edit, permission_quota_view,
)


def is_not_editable(context):
    return not context['object'].editable


link_quota_create = Link(
    icon='fa fa-envelope', permissions=(permission_quota_create,),
    text=_('Quota create'), view='quotas:quota_backend_selection',
)
link_quota_delete = Link(
    args='resolved_object.pk', conditional_disable=is_not_editable,
    permissions=(permission_quota_delete,), tags='dangerous', text=_('Delete'),
    view='quotas:quota_delete',
)
link_quota_edit = Link(
    args='object.pk', conditional_disable=is_not_editable,
    permissions=(permission_quota_edit,), text=_('Edit'),
    view='quotas:quota_edit',
)
link_quota_list = Link(
    icon='fa fa-envelope', permissions=(permission_quota_view,),
    text=_('Quotas list'), view='quotas:quota_list',
)
link_quota_setup = Link(
    icon='fa fa-dashboard', permissions=(permission_quota_view,),
    text=_('Quotas'), view='quotas:quota_list',
)
