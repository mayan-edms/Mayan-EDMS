from __future__ import unicode_literals

from django.http import Http404
from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.generics import SimpleView, SingleObjectListView

from .classes import DependencyGroup
from .forms import DependenciesLicensesForm
from .permissions import permission_dependencies_view
from .utils import PyPIClient


class CheckVersionView(SimpleView):
    template_name = 'appearance/generic_template.html'

    def get_extra_context(self):
        return {
            'title': _('Check for updates'),
            'content': PyPIClient().check_version_verbose()
        }


class DependencyGroupEntryListView(SingleObjectListView):
    view_permission = permission_dependencies_view

    def get_extra_context(self):
        return {
            'hide_link': True,
            'hide_object': True,
            'object': self.get_object(),
            'subtitle': self.get_object().help_text,
            'title': _('Entries for dependency group: %s') % self.get_object(),
        }

    def get_source_queryset(self):
        return self.get_object().get_entries()

    def get_object(self):
        try:
            return DependencyGroup.get(
                name=self.kwargs['dependency_group_name']
            )
        except KeyError:
            raise Http404(
                _('Group %s not found.') % self.kwargs[
                    'dependency_group_name'
                ]
            )


class DependencyGroupListView(SingleObjectListView):
    view_permission = permission_dependencies_view

    def get_extra_context(self):
        return {
            'hide_link': True,
            'hide_object': True,
            'title': _('Dependency groups'),
        }

    def get_source_queryset(self):
        return DependencyGroup.get_all()


class DependencyGroupEntryDetailView(SingleObjectListView):
    view_permission = permission_dependencies_view

    def get_extra_context(self):
        group = self.get_dependency_group()
        entry = self.get_dependency_group_entry()

        return {
            'entry': entry,
            'group': group,
            'hide_link': True,
            'hide_object': True,
            'navigation_object_list': ('group', 'entry'),
            'title': _('Dependency group and entry: %(group)s, %(entry)s') % {
                'group': group, 'entry': entry
            }
        }

    def get_dependency_group(self):
        try:
            return DependencyGroup.get(
                name=self.kwargs['dependency_group_name']
            )
        except KeyError:
            raise Http404(
                _('Group %s not found.') % self.kwargs[
                    'dependency_group_name'
                ]
            )

    def get_dependency_group_entry(self):
        try:
            return self.get_dependency_group().get_entry(
                entry_name=self.kwargs['dependency_group_entry_name']
            )
        except KeyError:
            raise Http404(
                _('Entry %s not found.') % self.kwargs[
                    'dependency_group_entry_name'
                ]
            )

    def get_source_queryset(self):
        return self.get_dependency_group_entry().get_dependencies()


class DependencyLicensesView(SimpleView):
    template_name = 'appearance/generic_form.html'

    def get_extra_context(self):
        # Use a function so that DependenciesLicensesForm get initialized
        # at every request
        return {
            'form': DependenciesLicensesForm(),
            'read_only': True,
            'title': _('Other packages licenses'),
        }
