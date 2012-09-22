from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.core.urlresolvers import reverse

from permissions.models import Permission

from .models import BootstrapSetup
from .classes import Cleanup
from .permissions import PERMISSION_BOOTSTRAP_EXECUTE, PERMISSION_NUKE_DATABASE
from .icons import icon_bootstrap_execute, icon_nuke_database


def bootstrap_type_list(request):
    Permission.objects.check_permissions(request.user, [PERMISSION_BOOTSTRAP_EXECUTE])

    context = {
        'object_list': BootstrapSetup.objects.all(),
        'title': _(u'database bootstrap setups'),
        'hide_link': True,
        'extra_columns': [
            {'name': _(u'description'), 'attribute': 'description'},
        ],
    }

    return render_to_response('generic_list.html', context,
        context_instance=RequestContext(request))


def bootstrap_execute(request, bootstrap_setup_pk):
    Permission.objects.check_permissions(request.user, [PERMISSION_BOOTSTRAP_EXECUTE])
    bootstrap_setup = get_object_or_404(BootstrapSetup, pk=bootstrap_setup_pk)

    post_action_redirect = reverse('bootstrap_type_list')

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', '/')))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', '/')))

    if request.method == 'POST':
        try:
            bootstrap_setup.execute()
        except Exception, exc:
            messages.error(request, _(u'Error executing bootstrap setup; %s') % exc)
        else:
            messages.success(request, _(u'Bootstrap setup "%s" executed successfully.') % bootstrap_setup)
            return HttpResponseRedirect(next)

    context = {
        'object_name': _(u'bootstrap setup'),
        'delete_view': False,
        'previous': previous,
        'next': next,
        'form_icon': icon_bootstrap_execute,
        'object': bootstrap_setup,
    }

    context['title'] = _(u'Are you sure you wish to execute the database bootstrap named: %s?') % bootstrap_setup

    return render_to_response('generic_confirm.html', context,
        context_instance=RequestContext(request))


def erase_database_view(request):
    Permission.objects.check_permissions(request.user, [PERMISSION_NUKE_DATABASE])

    post_action_redirect = None

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', '/')))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', '/')))

    if request.method == 'POST':
        try:
            Cleanup.execute_all()
        except Exception, exc:
            messages.error(request, _(u'Error erasing database; %s') % exc)
        else:
            messages.success(request, _(u'Database erased successfully.'))
            return HttpResponseRedirect(next)

    context = {
        'delete_view': False,
        'previous': previous,
        'next': next,
        'form_icon': icon_nuke_database,
    }

    context['title'] = _(u'Are you sure you wish to erase the entire database and document storage?')
    context['message'] = _(u'All documents, sources, metadata, metadata types, set, tags, indexes and logs will be lost irreversibly!')

    return render_to_response('generic_confirm.html', context,
        context_instance=RequestContext(request))
