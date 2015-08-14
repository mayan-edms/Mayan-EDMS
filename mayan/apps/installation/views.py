from __future__ import absolute_import, unicode_literals

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from common.generics import SingleObjectListView
from permissions import Permission

from .classes import PropertyNamespace
from .permissions import permission_installation_details


def namespace_list(request):
    Permission.check_permissions(
        request.user, (permission_installation_details,)
    )

    return render_to_response('appearance/generic_list.html', {
        'object_list': PropertyNamespace.get_all(),
        'title': _('Installation property namespaces'),
        'hide_object': True,
    }, context_instance=RequestContext(request))


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

