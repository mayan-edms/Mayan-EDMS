from __future__ import unicode_literals

from django.db.models.signals import post_migrate
from django.utils.translation import ugettext_lazy as _

from common import (
    MayanAppConfig, menu_multi_item, menu_object, menu_secondary, menu_setup,
    menu_sidebar
)

from .classes import (
    AccessHolder, AccessObject, AccessObjectClass
)
from .links import (
    link_acl_detail, link_acl_grant, link_acl_holder_new, link_acl_revoke
)

class ACLsApp(MayanAppConfig):
    name = 'acls'
    verbose_name = _('ACLs')

    def ready(self):
        super(ACLsApp, self).ready()

        menu_multi_item.bind_links(links=[link_acl_grant, link_acl_revoke], sources=['acls:acl_detail'])
        menu_object.bind_links(links=[link_acl_detail], sources=[AccessHolder])
        menu_sidebar.bind_links(links=[link_acl_holder_new], sources=[AccessObject])
