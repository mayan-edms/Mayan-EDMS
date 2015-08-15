from __future__ import unicode_literals

from django.http import Http404
from django.utils.translation import ugettext_lazy as _

from common.views import SingleObjectListView

from .classes import Statistic, StatisticNamespace
from .permissions import permission_statistics_view


class NamespaceListView(SingleObjectListView):
    extra_context = {
        'hide_link': True,
        'title': _('Statistics namespaces'),
    }
    template_name = 'appearance/generic_list.html'
    view_permission = permission_statistics_view

    def get_queryset(self):
        return StatisticNamespace.get_all()


class NamespaceDetailView(SingleObjectListView):
    template_name = 'appearance/generic_list.html'
    view_permission = permission_statistics_view

    def get_extra_context(self):
        return {
            'hide_link': True,
            'object': self.get_namespace(),
            'title': _('Namespace details for: %s') % self.get_namespace(),
        }

    def get_namespace(self):
        return StatisticNamespace.get(self.kwargs['namespace_id'])

    def get_queryset(self):
        return self.get_namespace().statistics


class StatisticExecute(SingleObjectListView):
    template_name = 'appearance/generic_list.html'
    view_permission = permission_statistics_view

    def get_extra_context(self):
        return {
            'hide_link': True,
            'namespace': self.get_statictic().namespace,
            'navigation_object_list': ('namespace', 'object'),
            'object': self.get_statictic(),
            'title': _('Results for: %s') % self.get_statictic(),
        }

    def get_queryset(self):
        return self.get_statictic().get_results()

    def get_statictic(self):
        try:
            return Statistic.get(self.kwargs['statistic_id'])
        except KeyError:
            raise Http404(_('Statistic "%s" not found.') % self.kwargs['statistic_id'])
