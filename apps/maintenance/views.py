from __future__ import absolute_import

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import PermissionDenied

from permissions.models import Permission

from .api import tools


def maintenance_menu(request):
    user_tools = {}
    for namespace, values in tools.items():
        user_tools[namespace] = {
            'title': values['title']
            }
        user_tools[namespace].setdefault('links', [])
        for link in values['links']:
            try:
                permissions = link.permissions
                Permission.objects.check_permissions(request.user, permissions)
                user_tools[namespace]['links'].append(link)
            except PermissionDenied:
                pass

    return render_to_response('tools.html', {
        'blocks': user_tools,
        'title': _(u'maintenance menu')
    },
    context_instance=RequestContext(request))
