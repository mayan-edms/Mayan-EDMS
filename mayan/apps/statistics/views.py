from __future__ import unicode_literals

from django.core.exceptions import PermissionDenied
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from .classes import Statistic, StatisticNamespace


def namespace_list(request):
    if not request.user.is_superuser or not request.user.is_staff:
        raise PermissionDenied

    return render_to_response('main/generic_list.html', {
        'object_list': StatisticNamespace.get_all(),
        'hide_link': True,
        'title': _('Statistics namespaces'),
        'list_object_variable_name': 'namespace',
    }, context_instance=RequestContext(request))


def namespace_details(request, namespace_id):
    if not request.user.is_superuser or not request.user.is_staff:
        raise PermissionDenied

    namespace = StatisticNamespace.get(namespace_id)

    return render_to_response('main/generic_list.html', {
        'object': namespace,
        'namespace': namespace,
        'object_list': namespace.statistics,
        'hide_link': True,
        'title': _('Namespace details for: %s') % namespace,
    }, context_instance=RequestContext(request))


def execute(request, statistic_id):
    if not request.user.is_superuser or not request.user.is_staff:
        raise PermissionDenied

    statictic = Statistic.get(statistic_id)

    return render_to_response('main/generic_list.html', {
        'object': statictic,
        'namespace': statictic.namespace,
        'navigation_object_list': [
            {'object': 'namespace', 'name': _('Namespace')},
            {'object': 'object', 'name': _('Statistic')},
        ],
        'object_list': statictic.get_results(),
        'hide_link': True,
        'title': _('Results for: %s') % statictic,
    }, context_instance=RequestContext(request))
