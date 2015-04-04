from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from navigation import Link


def has_usable_password(context):
    return context['request'].user.has_usable_password


link_about = Link(icon='fa fa-question', text=_('About'), view='common:about_view')
link_current_user_details = Link(icon='fa fa-user', text=_('User details'), view='common:current_user_details')
link_current_user_edit = Link(icon='fa fa-user', text=_('Edit details'), view='common:current_user_edit')
link_current_user_locale_profile_details = Link(icon='fa fa-globe', text=_('Locale profile'), view='common:current_user_locale_profile_details')
link_current_user_locale_profile_edit = Link(icon='fa fa-globe', text=_('Edit locale profile'), view='common:current_user_locale_profile_edit')
link_license = Link(icon='fa fa-book', text=_('License'), view='common:license_view')
link_logout = Link(icon='fa fa-sign-out', text=_('Logout'), view='common:logout_view')
link_password_change = Link(condition=has_usable_password, icon='fa fa-key', text=_('Change password'), view='common:password_change_view')
