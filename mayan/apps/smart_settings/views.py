from __future__ import unicode_literals

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe

from common.utils import encapsulate
from common.widgets import exists_widget
from common.views import SimpleView

from .classes import Namespace


class NamespaceListView(SimpleView):
    template_name = 'appearance/generic_list.html'

    def get_context_data(self, **kwargs):
        context = super(NamespaceListView, self).get_context_data(**kwargs)

        context.update(
            {
                'hide_link': True,
                'object_list': Namespace.get_all(),
                'title': _('Setting namespaces'),
            }
        )

        return context


class NamespaceDetailView(SimpleView):
    template_name = 'appearance/generic_list.html'

    def get_context_data(self, **kwargs):
        context = super(NamespaceDetailView, self).get_context_data(**kwargs)

        namespace = Namespace.get(self.kwargs['namespace_name'])

        context.update(
            {
                'hide_object': True,
                'object_list': namespace.settings,
                'title': _('Settings in namespace: %s') % namespace,
            }
        )

        return context
