from __future__ import absolute_import

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.db.models.loading import get_model
from django.http import Http404
from django.core.exceptions import PermissionDenied

from permissions.models import Permission
from common.utils import encapsulate
from acls.models import AccessEntry
from clustering.permissions import PERMISSION_NODES_VIEW
from clustering.models import Node


def node_workers(request, node_pk):
    node = get_object_or_404(Node, pk=node_pk)

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_NODES_VIEW])
    except PermissionDenied:
        AccessEntry.objects.check_access(PERMISSION_NODES_VIEW, request.user, node)

    context = {
        'object_list': node.workers().all(),
        'title': _(u'workers for node: %s') % node,
        'object': node,
        'hide_links': True,
        'extra_columns': [
            {
                'name': _(u'created'),
                'attribute': 'creation_datetime',
            },
            {
                'name': _(u'heartbeat'),
                'attribute': 'heartbeat',
            },
            {
                'name': _(u'state'),
                'attribute': 'get_state_display',
            },
            {
                'name': _(u'job queue item'),
                'attribute': 'job_queue_item',
            },
            {
                'name': _(u'job type'),
                'attribute': 'job_queue_item.job_type',
            },
        ],
    }

    return render_to_response('generic_list.html', context,
        context_instance=RequestContext(request))


    node = models.ForeignKey(Node, verbose_name=_(u'node'))
    name = models.CharField(max_length=255, verbose_name=_(u'name'))
    creation_datetime = models.DateTimeField(verbose_name=_(u'creation datetime'), default=lambda: datetime.datetime.now(), editable=False)
    heartbeat = models.DateTimeField(blank=True, default=datetime.datetime.now(), verbose_name=_(u'heartbeat check'))
    stat#e = models.CharField(max_length=4,
        #choices=WORKER_STATE_CHOICES,
        #default=WORKER_STATE_RUNNING,
        #verbose_name=_(u'state'))
