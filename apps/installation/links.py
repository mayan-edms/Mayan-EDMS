from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from .permissions import PERMISSION_INSTALLATION_DETAILS

link_menu_link = {'text': _(u'installation details'), 'view': 'namespace_list', 'icon': 'interface_preferences.png', 'permissions': [PERMISSION_INSTALLATION_DETAILS]}
link_namespace_list = {'text': _(u'installation property namespaces'), 'view': 'namespace_list', 'famfam': 'layout', 'permissions': [PERMISSION_INSTALLATION_DETAILS]}
link_namespace_details = {'text': _(u'details'), 'view': 'namespace_details', 'args': 'object.id', 'famfam': 'layout_link', 'permissions': [PERMISSION_INSTALLATION_DETAILS]}
