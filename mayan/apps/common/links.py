from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from navigation import Link


link_about = Link(
    icon='fa fa-info', text=_('About this'), view='common:about_view'
)
link_current_user_details = Link(
    icon='fa fa-user', text=_('User details'),
    view='common:current_user_details'
)
link_current_user_edit = Link(
    icon='fa fa-user', text=_('Edit details'), view='common:current_user_edit'
)
link_current_user_locale_profile_details = Link(
    icon='fa fa-globe', text=_('Locale profile'),
    view='common:current_user_locale_profile_details'
)
link_current_user_locale_profile_edit = Link(
    icon='fa fa-globe', text=_('Edit locale profile'),
    view='common:current_user_locale_profile_edit'
)
link_code = Link(
    icon='fa fa-code-fork', tags='new_window', text=_('Source code'),
    url='https://gitlab.com/mayan-edms/mayan-edms'
)
link_documentation = Link(
    icon='fa fa-book', tags='new_window', text=_('Documentation'),
    url='https://mayan.readthedocs.io/en/stable/'
)
link_filters = Link(
    icon='fa fa-filter', text=_('Data filters'),
    view='common:filter_selection'
)
link_forum = Link(
    icon='fa fa-life-ring', tags='new_window', text=_('Forum'),
    url='https://groups.google.com/forum/#!forum/mayan-edms'
)
link_license = Link(
    icon='fa fa-certificate', text=_('License'), view='common:license_view'
)
link_packages_licenses = Link(
    icon='fa fa-certificate', text=_('Other packages licenses'),
    view='common:packages_licenses_view'
)
link_setup = Link(
    icon='fa fa-gear', text=_('Setup'), view='common:setup_list'
)
link_support = Link(
    icon='fa fa-phone', tags='new_window', text=_('Support'),
    url='http://www.mayan-edms.com/providers/'
)
link_tools = Link(
    icon='fa fa-wrench', text=_('Tools'), view='common:tools_list'
)
