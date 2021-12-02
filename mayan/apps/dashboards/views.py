from django.utils.translation import ugettext_lazy as _

from mayan.apps.views.generics import SingleObjectListView, SimpleView

from .classes import Dashboard


class DashboardListView(SingleObjectListView):
    extra_context = {
        'hide_object': True,
        'title': _('Dashboards'),
    }

    def get_source_queryset(self):
        return Dashboard.get_all()


class DashboardDetailView(SimpleView):
    template_name = 'appearance/generic_template.html'

    def get_extra_context(self):
        dashboard = Dashboard.get(name=self.kwargs['dashboard_name'])

        return {
            'content': dashboard.render(request=self.request),
            'object': dashboard,
            'title': _('Dashboard detail')
        }
