from __future__ import unicode_literals

from django.db.utils import OperationalError
from django.utils.translation import ugettext_lazy as _

from acls import ModelPermission
from acls.links import link_acl_list
from acls.permissions import permission_acl_edit, permission_acl_view
from common import MayanAppConfig, menu_object, menu_secondary, menu_setup
from common.widgets import two_state_template
from navigation import SourceColumn

from .classes import QuotaBackend
from .links import (
    link_quota_create, link_quota_delete, link_quota_edit, link_quota_list,
    link_quota_setup
)
from .permissions import (
    permission_quota_delete, permission_quota_edit, permission_quota_view
)


class QuotasApp(MayanAppConfig):
    name = 'quotas'
    verbose_name = _('Quotas')

    def ready(self, *args, **kwargs):
        super(QuotasApp, self).ready(*args, **kwargs)
        Quota = self.get_model('Quota')

        QuotaBackend.initialize()

        try:
            for quota in Quota.objects.all():
                quota.update_receiver()
        except OperationalError:
            # Ignore errors during migration
            pass

        ModelPermission.register(
            model=Quota, permissions=(
                permission_acl_edit, permission_acl_view,
                permission_quota_delete, permission_quota_edit,
                permission_quota_view
            )
        )

        SourceColumn(
            source=Quota, label=_('Backend'), attribute='backend_label'
        )
        SourceColumn(
            source=Quota, label=_('Display'), attribute='backend_display'
        )
        SourceColumn(
            source=Quota, label=_('Usage'), attribute='backend_usage'
        )
        SourceColumn(
            source=Quota, label=_('Enabled?'),
            func=lambda context: two_state_template(
                context['object'].enabled
            )
        )
        SourceColumn(
            source=Quota, label=_('Editable?'),
            func=lambda context: two_state_template(
                context['object'].editable
            )
        )

        menu_object.bind_links(
            links=(
                link_quota_edit, link_acl_list, link_quota_delete,
            ), sources=(Quota,)
        )

        menu_secondary.bind_links(
            links=(
                link_quota_list, link_quota_create,
            ), sources=(
                Quota, 'quotas:quota_backend_selection', 'quotas:quota_create',
                'quotas:quota_list',
            )
        )

        menu_setup.bind_links(links=(link_quota_setup,))
