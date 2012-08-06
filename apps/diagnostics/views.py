from __future__ import absolute_import

from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.utils.text import capfirst

from common.utils import encapsulate
from permissions.models import Permission

from .api import DiagnosticNamespace


def diagnostic_list(request):
    tool_list = []
    
    for tool in DiagnosticNamespace.tool_all():
        try:
            Permission.objects.check_permissions(request.user, tool.link.permissions)
        except PermissionDenied:
            pass
        else:
            tool_list.append(tool)
    
    return render_to_response('generic_list.html', {
        'title': _(u'diagnostic tools'),
        'object_list': tool_list,
        'extra_columns': [
            {'name': _(u'namespace'), 'attribute': encapsulate(lambda x: capfirst(x.namespace))},
            {'name': _(u'label'), 'attribute': encapsulate(lambda x: capfirst(x.link.text))},
            {'name': _(u'description'), 'attribute': 'link.description'},
        ],
        'hide_object': True,
    }, context_instance=RequestContext(request))


def diagnostic_execute(request, diagnostic_tool_id):
    tool = DiagnosticNamespace.tool_get(int(diagnostic_tool_id))
    context = RequestContext(request)
    resolve_link = tool.link.resolve(context)
    return HttpResponseRedirect(resolve_link.url)
