from __future__ import absolute_import

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import PermissionDenied

from permissions.models import Permission

from .classes import Property, PropertyNamespace
from .permissions import PERMISSION_INSTALLATION_DETAILS
from .models import Installation


def namespace_list(request):
    Permission.objects.check_permissions(request.user, [PERMISSION_INSTALLATION_DETAILS])

    Installation().get_properties()

    return render_to_response('generic_list.html', {
        'object_list':  PropertyNamespace.get_all(),
        'title': _(u'installation property namespaces'),
        'hide_object': True,
    }, context_instance=RequestContext(request))


def namespace_details(request, namespace_id):
    Permission.objects.check_permissions(request.user, [PERMISSION_INSTALLATION_DETAILS])

    Installation().get_properties()

    namespace = PropertyNamespace.get(namespace_id)
    object_list = namespace.get_properties()
    title = _(u'installation namespace details for: %s') % namespace.label

    return render_to_response('generic_list.html', {
        'object_list': object_list,
        'hide_object': True,
        'title': title,
        'object': namespace,
    }, context_instance=RequestContext(request))
