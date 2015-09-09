from __future__ import unicode_literals

import json

from django.http import Http404
from django.utils.translation import ugettext_lazy as _

from common.views import SingleObjectDetailView, SingleObjectListView

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


class StatisticDetailView(SingleObjectDetailView):
    view_permission = permission_statistics_view

    def get_extra_context(self):
        return {
            'chart_data': self.get_object().get_chart_data(),
            'namespace': self.get_object().namespace,
            'navigation_object_list': ('namespace', 'object'),
            'no_data': not self.get_object().get_results()['series'],
            'object': self.get_object(),
            'title': _('Results for: %s') % self.get_object(),
        }

    def get_object(self):
        try:
            return Statistic.get(self.kwargs['slug'])
        except KeyError:
            raise Http404(_('Statistic "%s" not found.') % self.kwargs['slug'])

    def get_template_names(self):
        return (self.get_object().renderer.template_name,)
