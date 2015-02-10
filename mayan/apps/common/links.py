from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _


def has_usable_password(context):
    return context['request'].user.has_usable_password


link_password_change = {'text': _('Change password'), 'view': 'common:password_change_view', 'famfam': 'computer_key', 'condition': has_usable_password}
link_current_user_details = {'text': _('User details'), 'view': 'common:current_user_details', 'famfam': 'vcard'}
link_current_user_edit = {'text': _('Edit details'), 'view': 'common:current_user_edit', 'famfam': 'vcard_edit'}

link_about = {'text': _('About'), 'view': 'common:about_view', 'famfam': 'information'}
link_license = {'text': _('License'), 'view': 'common:license_view', 'famfam': 'script'}

link_current_user_locale_profile_details = {'text': _('Locale profile'), 'view': 'common:current_user_locale_profile_details', 'famfam': 'world'}
link_current_user_locale_profile_edit = {'text': _('Edit locale profile'), 'view': 'common:current_user_locale_profile_edit', 'famfam': 'world_edit'}

link_logout = {'text': _('Logout'), 'view': 'common:logout_view', 'famfam': 'door_out'}
