from __future__ import absolute_import

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404, HttpResponseRedirect
from django.db.models.loading import get_model
from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.contrib import messages

from permissions.models import Permission
from common.utils import encapsulate
from acls.models import AccessEntry

from .forms import ClusteringConfigForm
from .models import Node, ClusteringConfig
from .permissions import PERMISSION_NODES_VIEW, PERMISSION_EDIT_CLUSTER_CONFIGURATION


def node_list(request):
    Permission.objects.check_permissions(request.user, [PERMISSION_NODES_VIEW])

    context = {
        'object_list': Node.objects.all(),
        'title': _(u'nodes'),
        'extra_columns_preffixed': [
            {
                'name': _(u'hostname'),
                'attribute': 'hostname',
            },
            {
                'name': _(u'cpu load'),
                'attribute': 'cpuload',
            },
            {
                'name': _(u'heartbeat'),
                'attribute': 'heartbeat',
            },
            {
                'name': _(u'memory usage'),
                'attribute': 'memory_usage',
            },

        ],
        'hide_object': True,
    }

    return render_to_response('generic_list.html', context,
        context_instance=RequestContext(request))


def node_workers(request, node_pk):
    node = get_object_or_404(Node, pk=node_pk)

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_NODES_VIEW])
    except PermissionDenied:
        AccessEntry.objects.check_access(PERMISSION_NODES_VIEW, request.user, node)

    context = {
        'object_list': node.workers.all(),
        'title': _(u'workers for node: %s') % node,
        'object': node,
        'hide_object': True,
    }

    return render_to_response('generic_list.html', context,
        context_instance=RequestContext(request))


def clustering_config_edit(request):
    Permission.objects.check_permissions(request.user, [PERMISSION_EDIT_CLUSTER_CONFIGURATION])

    cluster_config = ClusteringConfig.get()
    
    post_action_redirect = None

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', '/')))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', '/')))
    

    if request.method == 'POST':
        form = ClusteringConfigForm(data=request.POST)
        if form.is_valid():
            try:
                form.save()
            except Exception, exc:
                messages.error(request, _(u'Error trying to edit cluster configuration; %s') % exc)
            else:
                messages.success(request, _(u'Cluster configuration edited successfully.'))
                return HttpResponseRedirect(next)
    else:
        form = ClusteringConfigForm(instance=cluster_config)

    return render_to_response('generic_form.html', {
        'form': form,
        'object': cluster_config,
        'title': _(u'Edit cluster configuration')
    }, context_instance=RequestContext(request))
