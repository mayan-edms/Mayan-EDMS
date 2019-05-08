from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.menus import (
    menu_about, menu_list_facet, menu_secondary, menu_tools
)
from mayan.apps.common.html_widgets import TwoStateWidget
from mayan.apps.navigation.classes import SourceColumn

from .classes import Dependency, DependencyGroup, DependencyGroupEntry
from .dependencies import *  # NOQA
from .links import (
    link_check_version, link_dependency_group_entry_detail,
    link_dependency_group_entry_list, link_dependency_group_list,
    link_packages_licenses, link_dependency_tool
)


class DependenciesApp(MayanAppConfig):
    app_namespace = 'dependencies'
    app_url = 'dependencies'
    has_rest_api = False
    has_tests = False
    name = 'mayan.apps.dependencies'
    verbose_name = _('Dependencies')

    def ready(self):
        super(DependenciesApp, self).ready()

        SourceColumn(
            attribute='get_label', label=_('Label'), order=-1, source=Dependency
        )
        SourceColumn(
            attribute='name', label=_('Internal name'), order=0, source=Dependency
        )
        SourceColumn(
            attribute='get_help_text', label=_('Description'), order=1,
            source=Dependency
        )
        SourceColumn(
            attribute='class_name_verbose_name', label=_('Type'),
            order=2, source=Dependency
        )
        SourceColumn(
            attribute='get_other_data', label=_('Other data'), order=3,
            source=Dependency
        )
        SourceColumn(
            attribute='app_label_verbose_name', label=_('Declared by'),
            order=4, source=Dependency
        )
        SourceColumn(
            attribute='get_version_string', label=_('Version'),
            order=5, source=Dependency
        )
        SourceColumn(
            attribute='get_environment_verbose_name', label=_('Environment'),
            order=6, source=Dependency
        )
        SourceColumn(
            attribute='check', label=_('Check'), order=7, source=Dependency,
            widget=TwoStateWidget
        )

        SourceColumn(
            attribute='label', label=_('Label'), order=0, source=DependencyGroup
        )
        SourceColumn(
            attribute='help_text', label=_('Description'), order=1,
            source=DependencyGroup
        )

        SourceColumn(
            attribute='label', label=_('Label'), order=0,
            source=DependencyGroupEntry
        )
        SourceColumn(
            attribute='help_text', label=_('Description'), order=1,
            source=DependencyGroupEntry
        )

        menu_about.bind_links(
            links=(link_packages_licenses, link_check_version)
        )

        menu_list_facet.bind_links(
            links=(link_dependency_group_entry_list,),
            sources=(DependencyGroup,)
        )
        menu_list_facet.bind_links(
            links=(link_dependency_group_entry_detail,),
            sources=(DependencyGroupEntry,)
        )

        menu_secondary.bind_links(
            links=(link_dependency_group_list,),
            sources=(
                DependencyGroup,
                'dependencies:dependency_group_list',
            )
        )

        menu_tools.bind_links(links=(link_dependency_tool,))
