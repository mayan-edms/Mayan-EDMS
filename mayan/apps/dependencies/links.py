from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link

from .icons import (
    icon_check_version, icon_dependency_group_entry_list,
    icon_dependency_group_entry_detail,
    icon_dependency_licenses, icon_dependency_group_list
)
from .permissions import permission_dependencies_view

link_check_version = Link(
    icon=icon_check_version, text=_('Check for updates'),
    view='dependencies:check_version_view'
)
link_dependency_group_list = Link(
    icon=icon_dependency_group_list,
    permissions=(permission_dependencies_view,), text=_('Groups'),
    view='dependencies:dependency_group_list'
)
link_dependency_group_entry_list = Link(
    args='resolved_object.name', icon=icon_dependency_group_entry_list,
    permissions=(permission_dependencies_view,), text=_('Entries'),
    view='dependencies:dependency_group_entry_list'
)
link_dependency_group_entry_detail = Link(
    args=('resolved_object.dependency_group.name', 'resolved_object.name'),
    icon=icon_dependency_group_entry_detail,
    permissions=(permission_dependencies_view,), text=_('Details'),
    view='dependencies:dependency_group_entry_detail'
)
link_packages_licenses = Link(
    icon=icon_dependency_licenses, text=_('Dependencies licenses'),
    view='dependencies:dependency_licenses_view'
)
link_dependency_tool = Link(
    icon=icon_dependency_group_list,
    permissions=(permission_dependencies_view,), text=_('Dependencies'),
    view='dependencies:dependency_group_list'
)
