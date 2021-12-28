from django.utils.translation import ugettext_lazy as _

from mayan.apps.authentication.link_conditions import condition_user_is_authenticated

from mayan.apps.navigation.classes import Link

from .icons import (
    icon_current_user_locale_profile_details,
    icon_current_user_locale_profile_edit,
)


link_current_user_locale_profile_details = Link(
    condition=condition_user_is_authenticated,
    icon=icon_current_user_locale_profile_details,
    text=_('Locale profile'),
    view='locales:current_user_locale_profile_details'
)
link_current_user_locale_profile_edit = Link(
    condition=condition_user_is_authenticated,
    icon=icon_current_user_locale_profile_edit,
    text=_('Edit locale profile'),
    view='locales:current_user_locale_profile_edit'
)
