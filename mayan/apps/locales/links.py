from django.utils.translation import ugettext_lazy as _

from mayan.apps.authentication.link_conditions import (
    condition_user_is_authenticated
)
from mayan.apps.navigation.classes import Link

from .icons import (
    icon_user_locale_profile_detail,
    icon_user_locale_profile_edit,
)


link_user_locale_profile_detail = Link(
    args='object.id',
    condition=condition_user_is_authenticated,
    icon=icon_user_locale_profile_detail,
    text=_('Locale profile'),
    view='locales:user_locale_profile_detail'
)
link_user_locale_profile_edit = Link(
    args='object.id',
    condition=condition_user_is_authenticated,
    icon=icon_user_locale_profile_edit,
    text=_('Edit locale profile'),
    view='locales:user_locale_profile_edit'
)
