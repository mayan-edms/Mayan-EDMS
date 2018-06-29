from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from navigation import Link

from .icons import icon_logout, icon_password_change


def has_usable_password(context):
    return context['request'].user.has_usable_password


link_logout = Link(
    html_extra_classes='non-ajax', icon_class=icon_logout,
    text=_('Logout'), view='authentication:logout_view'
)
link_password_change = Link(
    condition=has_usable_password, icon_class=icon_password_change,
    text=_('Change password'), view='authentication:password_change_view'
)
