from __future__ import absolute_import

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.http import Http404

from permissions.models import Permission
from common.utils import encapsulate

from .permissions import PERMISSION_VIEW_SCHEDULER_LIST, PERMISSION_VIEW_JOB_LIST
from .api import LocalScheduler


def scheduler_list(request):
    Permission.objects.check_permissions(request.user, [PERMISSION_VIEW_SCHEDULER_LIST])

    context = {
        'object_list': LocalScheduler.get_all(),
        'title': _(u'local schedulers'),
        'extra_columns': [
            {
                'name': _(u'name'),
                'attribute': 'name'
            },
            {
                'name': _(u'label'),
                'attribute': 'label'
            },
            {
                'name': _(u'running'),
                'attribute': 'running'
            },
            {
                'name': _(u'jobs'),
                'attribute': encapsulate(lambda x: len(x.get_job_list()))
            },
        ],
        'hide_object': True,
    }

    return render_to_response('generic_list.html', context,
        context_instance=RequestContext(request))


def job_list(request, scheduler_name):
    Permission.objects.check_permissions(request.user, [PERMISSION_VIEW_JOB_LIST])
    try:
        scheduler = LocalScheduler.get(scheduler_name)
    except:
        raise Http404

    context = {
        'object_list': scheduler.get_job_list(),
        'title': _(u'local jobs in scheduler: %s') % scheduler,
        'extra_columns': [
            {
                'name': _(u'name'),
                'attribute': 'name'
            },
            {
                'name': _(u'label'),
                'attribute': 'label'
            },
            {
                'name': _(u'start date time'),
                'attribute': 'start_date'
            },
            {
                'name': _(u'type'),
                'attribute': 'job_type'
            },
        ],
        'hide_object': True,
        'hide_links': True,
    }

    return render_to_response('generic_list.html', context,
        context_instance=RequestContext(request))
