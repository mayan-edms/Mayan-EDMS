from __future__ import unicode_literals

from django.http import Http404
from django.utils.translation import ugettext_lazy as _

from common.views import SimpleView

from .classes import Namespace


class NamespaceListView(SimpleView):
    template_name = 'appearance/generic_list.html'

    def get_extra_context(self):
        return {
            'hide_link': True,
            'object_list': Namespace.get_all(),
            'title': _('Setting namespaces'),
        }


class NamespaceDetailView(SimpleView):
    template_name = 'appearance/generic_list.html'

    def get_extra_context(self):
        try:
            namespace = Namespace.get(self.kwargs['namespace_name'])
        except KeyError:
            raise Http404(_('Namespace: %s, not found') % self.kwargs['namespace_name'])

        return {
            'hide_object': True,
            'object_list': namespace.settings,
            'title': _('Settings in namespace: %s') % namespace,
        }
