from django.utils.translation import ugettext_lazy as _

from navigation import Link

from .icons import (icon_password_change, icon_current_user_details, icon_current_user_edit,
    icon_about, icon_license, icon_admin_site)

def has_usable_password(context):
    return context['request'].user.has_usable_password


def is_superuser(context):
    return context['request'].user.is_staff or context['request'].user.is_superuser


link_password_change = Link(text=_(u'change password'), view='password_change_view', icon=icon_password_change, condition=has_usable_password)
link_current_user_details = Link(text=_(u'user details'), view='current_user_details', icon=icon_current_user_details)
link_current_user_edit = Link(text=_(u'edit details'), view='current_user_edit', icon=icon_current_user_edit)
link_about = Link(text=_('about'), view='about_view', icon=icon_about)
link_license = Link(text=_('license'), view='license_view', icon=icon_license)
link_admin_site = Link(text=_(u'admin site'), view='admin:index', icon=icon_admin_site, condition=is_superuser)
