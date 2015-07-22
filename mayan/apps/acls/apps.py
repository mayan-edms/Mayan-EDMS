from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from common import MayanAppConfig, menu_object, menu_sidebar

from .links import link_acl_new, link_acl_delete, link_acl_permissions
from .models import AccessControlList


class ACLsApp(MayanAppConfig):
    name = 'acls'
    verbose_name = _('ACLs')

    def ready(self):
        super(ACLsApp, self).ready()

        menu_object.bind_links(
            links=[link_acl_permissions, link_acl_delete],
            sources=[AccessControlList]
        )
        menu_sidebar.bind_links(links=[link_acl_new], sources=['acls:acl_list'])
