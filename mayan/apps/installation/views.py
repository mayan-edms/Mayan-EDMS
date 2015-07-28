from __future__ import absolute_import, unicode_literals

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from permissions import Permission

from .classes import PropertyNamespace
from .permissions import permission_installation_details


def namespace_list(request):
    Permission.check_permissions(
        request.user, [permission_installation_details]
    )

    return render_to_response('appearance/generic_list.html', {
        'object_list': PropertyNamespace.get_all(),
        'title': _('Installation property namespaces'),
        'hide_object': True,
    }, context_instance=RequestContext(request))


def namespace_details(request, namespace_id):
    Permission.check_permissions(
        request.user, [permission_installation_details]
    )

    namespace = PropertyNamespace.get(namespace_id)
    object_list = namespace.get_properties()
    title = _('Installation namespace details for: %s') % namespace.label

    return render_to_response('appearance/generic_list.html', {
        'object_list': object_list,
        'hide_object': True,
        'title': title,
        'object': namespace,
    }, context_instance=RequestContext(request))
