from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from smart_settings import Namespace

namespace = Namespace(name='permissions', label=_('Permissions'))
setting_default_roles = namespace.add_setting(global_name='ROLES_DEFAULT_ROLES', default=[], help_text=_('A list of existing roles that are automatically assigned to newly created users.'))
