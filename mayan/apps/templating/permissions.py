from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.permissions import PermissionNamespace

namespace = PermissionNamespace(label=_('Templating'), name='templating')

permission_template_sandbox = namespace.add_permission(
    label=_('Use the template sandbox'), name='template_sandbox'
)
