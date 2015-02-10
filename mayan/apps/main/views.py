from __future__ import absolute_import, unicode_literals

from django.core.exceptions import PermissionDenied
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from dynamic_search.classes import SearchModel
from permissions.models import Permission

from .api import diagnostics, tools
from .classes import FrontPageButton


def home(request):
    document_search = SearchModel.get('documents.Document')

    context = {
        'object_navigation_links': FrontPageButton.get_all(),
        'query_string': request.GET,
        'hide_links': True,
        'search_results_limit': 100,
    }

    if request.GET:
        queryset, ids, timedelta = document_search.search(request.GET, request.user)

        # Update the context with the search results
        context.update({
            'object_list': queryset,
            'time_delta': timedelta,
            'title': _('Results'),
        })

    return render_to_response('main/home.html', context, context_instance=RequestContext(request))


def maintenance_menu(request):
    user_tools = {}
    for namespace, values in tools.items():
        user_tools[namespace] = {
            'title': values['title']
        }
        user_tools[namespace].setdefault('links', [])
        for link in values['links']:
            try:
                permissions = link.get('permissions', [])
                Permission.objects.check_permissions(request.user, permissions)
                user_tools[namespace]['links'].append(link)
            except PermissionDenied:
                pass

    return render_to_response('main/tools.html', {
        'blocks': user_tools,
        'title': _('Maintenance menu')
    }, context_instance=RequestContext(request))


def diagnostics_view(request):
    return render_to_response('main/diagnostics.html', {
        'blocks': diagnostics,
        'title': _('Diagnostics')
    }, context_instance=RequestContext(request))
