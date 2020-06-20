from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link

from .icons import (
    icon_about, icon_book, icon_current_user_locale_profile_details,
    icon_current_user_locale_profile_edit, icon_documentation,
    icon_forum, icon_license, icon_setup, icon_source_code, icon_support,
    icon_tools
)

link_about = Link(
    icon_class=icon_about, text=_('About this'), view='common:about_view'
)
link_book = Link(
    icon_class=icon_book, tags='new_window', text=_('Get the book'),
    url='https://mayan-edms.com/book/'
)
link_current_user_locale_profile_details = Link(
    icon_class=icon_current_user_locale_profile_details,
    text=_('Locale profile'),
    view='common:current_user_locale_profile_details'
)
link_current_user_locale_profile_edit = Link(
    icon_class=icon_current_user_locale_profile_edit,
    text=_('Edit locale profile'),
    view='common:current_user_locale_profile_edit'
)
link_documentation = Link(
    icon_class=icon_documentation, tags='new_window',
    text=_('Documentation'), url='https://docs.mayan-edms.com'
)
link_forum = Link(
    icon_class=icon_forum, tags='new_window', text=_('Forum'),
    url='https://forum.mayan-edms.com'
)
link_license = Link(
    icon_class=icon_license, text=_('License'), view='common:license_view'
)
link_setup = Link(
    icon_class=icon_setup, text=_('Setup'), view='common:setup_list'
)
link_source_code = Link(
    icon_class=icon_source_code, tags='new_window', text=_('Source code'),
    url='https://gitlab.com/mayan-edms/mayan-edms'
)
link_support = Link(
    icon_class=icon_support, tags='new_window', text=_('Get support'),
    url='http://www.mayan-edms.com/providers/'
)
link_tools = Link(
    icon_class=icon_tools, text=_('Tools'), view='common:tools_list'
)
