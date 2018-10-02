from __future__ import unicode_literals

from django.apps import apps
from django.utils.translation import ugettext_lazy as _

from navigation import Link
from navigation.classes import Separator, Text

from .icons import (
    icon_about, icon_check_version, icon_current_user_details,
    icon_current_user_edit, icon_current_user_locale_profile_details,
    icon_current_user_locale_profile_edit, icon_documentation,
    icon_forum, icon_license, icon_object_error_list_with_icon,
    icon_packages_licenses, icon_setup, icon_source_code, icon_support,
    icon_tools
)
from .permissions_runtime import permission_error_log_view
from .utils import get_user_label_text


def get_kwargs_factory(variable_name):
    def get_kwargs(context):
        ContentType = apps.get_model(
            app_label='contenttypes', model_name='ContentType'
        )

        content_type = ContentType.objects.get_for_model(
            context[variable_name]
        )
        return {
            'app_label': '"{}"'.format(content_type.app_label),
            'model': '"{}"'.format(content_type.model),
            'object_id': '{}.pk'.format(variable_name)
        }

    return get_kwargs


link_about = Link(
    icon_class=icon_about, text=_('About this'), view='common:about_view'
)
link_check_version = Link(
    icon_class=icon_check_version, text=_('Check for updates'),
    view='common:check_version_view'
)
link_current_user_details = Link(
    icon_class=icon_current_user_details, text=_('User details'),
    view='common:current_user_details'
)
link_current_user_edit = Link(
    icon_class=icon_current_user_edit, text=_('Edit details'),
    view='common:current_user_edit'
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
link_object_error_list = Link(
    kwargs=get_kwargs_factory('resolved_object'),
    permissions=(permission_error_log_view,), text=_('Errors'),
    view='common:object_error_list',
)
link_object_error_list_clear = Link(
    kwargs=get_kwargs_factory('resolved_object'),
    permissions=(permission_error_log_view,), text=_('Clear all'),
    view='common:object_error_list_clear',
)
link_object_error_list_with_icon = Link(
    kwargs=get_kwargs_factory('resolved_object'),
    icon_class=icon_object_error_list_with_icon,
    permissions=(permission_error_log_view,), text=_('Errors'),
    view='common:error_list',
)
link_forum = Link(
    icon_class=icon_forum, tags='new_window', text=_('Forum'),
    url='https://forum.mayan-edms.com'
)
link_license = Link(
    icon_class=icon_license, text=_('License'), view='common:license_view'
)
link_packages_licenses = Link(
    icon_class=icon_packages_licenses, text=_('Other packages licenses'),
    view='common:packages_licenses_view'
)
link_setup = Link(
    icon_class=icon_setup, text=_('Setup'), view='common:setup_list'
)
link_source_code = Link(
    icon_class=icon_source_code, tags='new_window', text=_('Source code'),
    url='https://gitlab.com/mayan-edms/mayan-edms'
)
link_support = Link(
    icon_class=icon_support, tags='new_window', text=_('Support'),
    url='http://www.mayan-edms.com/providers/'
)
link_tools = Link(
    icon_class=icon_tools, text=_('Tools'), view='common:tools_list'
)
separator_user_label = Separator()
text_user_label = Text(text=get_user_label_text)
