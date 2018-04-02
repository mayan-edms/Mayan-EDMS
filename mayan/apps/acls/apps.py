from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from common import MayanAppConfig, menu_object, menu_sidebar
from navigation import SourceColumn

from .links import link_acl_create, link_acl_delete, link_acl_permissions


class ACLsApp(MayanAppConfig):
    has_rest_api = True
    has_tests = True
    name = 'acls'
    verbose_name = _('ACLs')

    def ready(self):
        super(ACLsApp, self).ready()

        AccessControlList = self.get_model('AccessControlList')

        SourceColumn(
            source=AccessControlList, label=_('Role'), attribute='role'
        )
        SourceColumn(
            source=AccessControlList, label=_('Permissions'),
            attribute='get_permission_titles'
        )

        menu_object.bind_links(
            links=(link_acl_permissions, link_acl_delete),
            sources=(AccessControlList,)
        )
        menu_sidebar.bind_links(
            links=(link_acl_create,), sources=('acls:acl_list',)
        )
