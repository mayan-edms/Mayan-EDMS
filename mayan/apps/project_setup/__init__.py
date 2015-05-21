from __future__ import unicode_literals

from navigation.api import register_links

from .links import link_setup

register_links(['common:current_user_details', 'common:current_user_edit', 'common:current_user_locale_profile_details', 'common:current_user_locale_profile_edit', 'common:password_change_view'], [link_setup], menu_name='secondary_menu')
