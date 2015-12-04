from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from common.generics import SingleObjectListView

from .classes import PropertyNamespace
from .permissions import permission_installation_details


class NamespaceListView(SingleObjectListView):
    extra_context = {
        'title': _('Installation property namespaces'),
        'hide_object': True,
    }
    view_permission = permission_installation_details

    def get_queryset(self):
        return PropertyNamespace.get_all()


class NamespaceDetailView(SingleObjectListView):
    view_permission = permission_installation_details

    def get_extra_context(self):
        return {
            'title': _('Installation namespace details for: %s') % self.get_namespace().label,
            'hide_object': True,
            'object': self.get_namespace(),
        }

    def get_namespace(self):
        return PropertyNamespace.get(self.kwargs['namespace_id'])

    def get_queryset(self):
        return self.get_namespace().get_properties()
