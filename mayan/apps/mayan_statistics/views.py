from __future__ import unicode_literals

from django.contrib import messages
from django.http import Http404
from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.generics import ConfirmView, SimpleView, SingleObjectListView

from .classes import Statistic, StatisticNamespace
from .permissions import permission_statistics_view
from .tasks import task_execute_statistic


class NamespaceListView(SingleObjectListView):
    extra_context = {
        'hide_link': True,
        'title': _('Statistics namespaces'),
    }
    template_name = 'appearance/generic_list.html'
    view_permission = permission_statistics_view

    def get_source_queryset(self):
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
        return StatisticNamespace.get(slug=self.kwargs['slug'])

    def get_source_queryset(self):
        return self.get_namespace().statistics


class StatisticDetailView(SimpleView):
    view_permission = permission_statistics_view

    def get_extra_context(self):
        obj = self.get_object()

        return {
            'chart_data': obj.get_chart_data(),
            'namespace': obj.namespace,
            'navigation_object_list': ('namespace', 'object'),
            'no_data': not obj.get_results_data()['series'],
            'object': obj,
            'title': _('Results for: %s') % obj,
        }

    def get_object(self):
        try:
            return Statistic.get(self.kwargs['slug'])
        except KeyError:
            raise Http404(_('Statistic "%s" not found.') % self.kwargs['slug'])

    def get_template_names(self):
        return (self.get_object().renderer.template_name,)


class StatisticQueueView(ConfirmView):
    view_permission = permission_statistics_view

    def get_extra_context(self):
        obj = self.get_object()
        return {
            'namespace': obj.namespace,
            'object': obj,
            # Translators: This text is asking users if they want to queue
            # (to send to the queue) a statistic for it to be update ahead
            # of schedule
            'title': _(
                'Queue statistic "%s" to be updated?'
            ) % obj,
        }

    def get_object(self):
        try:
            return Statistic.get(slug=self.kwargs['slug'])
        except KeyError:
            raise Http404(_('Statistic "%s" not found.') % self.kwargs['slug'])

    def view_action(self):
        task_execute_statistic.delay(slug=self.get_object().slug)
        messages.success(
            message=_(
                'Statistic "%s" queued successfully for update.'
            ) % self.get_object().label, request=self.request
        )
