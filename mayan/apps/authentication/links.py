from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link
from mayan.apps.user_management.links import condition_user_is_not_admin
from mayan.apps.user_management.permissions import permission_user_edit

from .icons import icon_impersonate_start, icon_logout, icon_password_change
from .permissions import permission_users_impersonate


def _condition_user_has_usable_password_and_can_change_password(user):
    if user.is_authenticated:
        return user.has_usable_password() and not user.user_options.block_password_change
    else:
        return False


def condition_user_has_usable_password_and_can_change_password(context, resolved_object):
    user = context['request'].user

    return _condition_user_has_usable_password_and_can_change_password(
        user=user
    )


def condition_user_has_usable_password_and_can_change_password_and_is_not_admin(context, resolved_object):
    return _condition_user_has_usable_password_and_can_change_password(
        user=resolved_object
    ) and condition_user_is_not_admin(
        context=context, resolved_object=resolved_object
    )


link_logout = Link(
    html_extra_classes='non-ajax', icon=icon_logout, text=_('Logout'),
    view='authentication:logout_view'
)
link_password_change = Link(
    condition=condition_user_has_usable_password_and_can_change_password,
    icon=icon_password_change, text=_('Change password'),
    view='authentication:password_change_view'
)
link_user_impersonate_form_start = Link(
    icon=icon_impersonate_start,
    permissions=(permission_users_impersonate,), text=_('Impersonate user'),
    view='authentication:user_impersonate_form_start'
)
link_user_impersonate_start = Link(
    args='object.id', condition=condition_user_is_not_admin, icon=icon_impersonate_start,
    permissions=(permission_users_impersonate,), text=_('Impersonate'),
    view='authentication:user_impersonate_start'
)
link_user_multiple_set_password = Link(
    icon=icon_password_change, permissions=(permission_user_edit,),
    text=_('Set password'), view='authentication:user_multiple_set_password'
)
link_user_set_password = Link(
    args='object.id', condition=condition_user_has_usable_password_and_can_change_password_and_is_not_admin,
    icon=icon_password_change, permissions=(permission_user_edit,),
    text=_('Set password'), view='authentication:user_set_password'
)
