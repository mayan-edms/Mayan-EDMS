from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from .icons import icon_acl_app
from .links import acl_setup_valid_classes

name = 'acls'
label = _(u'ACL')
description = _(u'Handles object level access control.')
icon = icon_acl_app
setup_links = [acl_setup_valid_classes]
dependencies = ['app_registry', 'permissions', 'navigation']
