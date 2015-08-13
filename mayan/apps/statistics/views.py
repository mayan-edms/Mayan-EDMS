from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from common.views import SimpleView

from .classes import Statistic, StatisticNamespace
from .permissions import permission_statistics_view


class NamespaceListView(SimpleView):
    template_name = 'appearance/generic_list.html'
    view_permission = permission_statistics_view

    def get_extra_context(self):
        return {
            'hide_link': True,
            'object_list': StatisticNamespace.get_all(),
            'title': _('Statistics namespaces'),
        }


class NamespaceDetailView(SimpleView):
    template_name = 'appearance/generic_list.html'
    view_permission = permission_statistics_view

    def get_extra_context(self):
        namespace = StatisticNamespace.get(self.kwargs['namespace_id'])

        return {
            'hide_link': True,
            'object': namespace,
            'object_list': namespace.statistics,
            'title': _('Namespace details for: %s') % namespace,
        }


class StatisticExecute(SimpleView):
    template_name = 'appearance/generic_list.html'
    view_permission = permission_statistics_view

    def get_extra_context(self):
        statictic = Statistic.get(self.kwargs['statistic_id'])

        return {
            'hide_link': True,
            'namespace': statictic.namespace,
            'navigation_object_list': ('namespace', 'object'),
            'object': statictic,
            'object_list': statictic.get_results(),
            'title': _('Results for: %s') % statictic,
        }
