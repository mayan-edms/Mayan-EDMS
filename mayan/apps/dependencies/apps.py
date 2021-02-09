from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.menus import (
    menu_about, menu_list_facet, menu_secondary, menu_tools
)
from mayan.apps.navigation.classes import SourceColumn
from mayan.apps.views.html_widgets import TwoStateWidget

from .classes import Dependency, DependencyGroup, DependencyGroupEntry
from .links import (
    link_check_version, link_dependency_group_entry_detail,
    link_dependency_group_entry_list, link_dependency_group_list,
    link_packages_licenses, link_dependency_tool
)


class DependenciesApp(MayanAppConfig):
    app_namespace = 'dependencies'
    app_url = 'dependencies'
    has_rest_api = False
    has_tests = True
    name = 'mayan.apps.dependencies'
    verbose_name = _('Dependencies')

    def ready(self):
        super().ready()

        Dependency.load_modules()

        SourceColumn(
            attribute='get_label', is_identifier=True, label=_('Label'),
            order=-1, source=Dependency
        )
        SourceColumn(
            attribute='name', include_label=True, label=_('Internal name'),
            order=0, source=Dependency
        )
        SourceColumn(
            attribute='get_help_text', include_label=True,
            label=_('Description'), order=1, source=Dependency
        )
        SourceColumn(
            attribute='class_name_verbose_name', include_label=True,
            label=_('Type'), order=2, source=Dependency
        )
        SourceColumn(
            attribute='get_other_data', include_label=True,
            label=_('Other data'), order=3, source=Dependency
        )
        SourceColumn(
            attribute='app_label_verbose_name', include_label=True,
            label=_('Declared by'), order=4, source=Dependency
        )
        SourceColumn(
            attribute='get_version_string', include_label=True,
            label=_('Version'), order=5, source=Dependency
        )
        SourceColumn(
            attribute='get_environment_verbose_name', include_label=True,
            label=_('Environment'), order=6, source=Dependency
        )
        SourceColumn(
            attribute='check', include_label=True, label=_('Check'), order=7,
            source=Dependency, widget=TwoStateWidget
        )

        SourceColumn(
            attribute='label', is_identifier=True, label=_('Label'),
            order=0, source=DependencyGroup
        )
        SourceColumn(
            attribute='help_text', include_label=True,
            label=_('Description'), order=1, source=DependencyGroup
        )

        SourceColumn(
            attribute='label', is_identifier=True, label=_('Label'), order=0,
            source=DependencyGroupEntry
        )
        SourceColumn(
            attribute='help_text', include_label=True,
            label=_('Description'), order=1, source=DependencyGroupEntry
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
