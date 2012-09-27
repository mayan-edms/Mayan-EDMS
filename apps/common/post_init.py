from __future__ import absolute_import

import tempfile

from django.utils.translation import ugettext_lazy as _

from navigation.api import bind_links, register_top_menu

from .utils import validate_path
from .links import (link_password_change, link_current_user_details,
    link_current_user_edit, link_about, link_license, link_admin_site)
from .settings import TEMPORARY_DIRECTORY
import common.settings as common_settings

if (validate_path(getattr(common_settings, 'TEMPORARY_DIRECTORY')) == False) or (not getattr(common_settings, 'TEMPORARY_DIRECTORY')):
    setattr(common_settings, 'TEMPORARY_DIRECTORY', tempfile.mkdtemp())


bind_links(['about_view', 'license_view'], [link_about, link_license], menu_name='secondary_menu')
bind_links(['current_user_details', 'current_user_edit', 'password_change_view'], [link_current_user_details, link_current_user_edit, link_password_change], menu_name='secondary_menu')

register_top_menu('about', link=link_about, position=-1)
