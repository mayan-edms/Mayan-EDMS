from __future__ import absolute_import

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from acls.models import AccessEntry
from common.utils import encapsulate
from clustering.permissions import PERMISSION_NODES_VIEW
from clustering.models import Node
from permissions.models import Permission

from .exceptions import JobQueueAlreadyStopped, JobQueueAlreadyStarted
from .forms import JobProcessingConfigForm
from .models import JobQueue, JobProcessingConfig
from .permissions import (PERMISSION_JOB_QUEUE_VIEW,
    PERMISSION_JOB_PROCESSING_CONFIGURATION, PERMISSION_JOB_QUEUE_START_STOP)


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
        'hide_link': True,
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
                'attribute': 'job_queue_item.get_job_type',
            },
            {
                'name': _(u'job queue'),
                'attribute': 'job_queue_item.job_queue',
            },
        ],
    }

    return render_to_response('generic_list.html', context,
        context_instance=RequestContext(request))


def job_queues(request):
    # TODO: permissiong list filtering
    Permission.objects.check_permissions(request.user, [PERMISSION_JOB_QUEUE_VIEW])

    context = {
        'object_list': JobQueue.objects.all(),
        'title': _(u'job queue'),
        'hide_link': True,
        'extra_columns': [
            {
                'name': _(u'state'),
                'attribute': 'get_state_display',
            },
            {
                'name': _(u'pending jobs'),
                'attribute': 'pending_jobs.count',
            },
            {
                'name': _(u'active jobs'),
                'attribute': 'active_jobs.count',
            },
            {
                'name': _(u'error jobs'),
                'attribute': 'error_jobs.count',
            },
        ],
    }

    return render_to_response('generic_list.html', context,
        context_instance=RequestContext(request))


def job_queue_items(request, job_queue_pk, pending_jobs=False, error_jobs=False, active_jobs=False):
    job_queue = get_object_or_404(JobQueue, pk=job_queue_pk)

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_JOB_QUEUE_VIEW])
    except PermissionDenied:
        AccessEntry.objects.check_access(PERMISSION_JOB_QUEUE_VIEW, request.user, job_queue)

    jobs = set()
    if pending_jobs:
        jobs = job_queue.pending_jobs.all()
        title = _(u'pending jobs for queue: %s') % job_queue
        
    if error_jobs:
        jobs = job_queue.error_jobs.all()
        title = _(u'error jobs for queue: %s') % job_queue

    if active_jobs:
        jobs = job_queue.active_jobs.all()
        title = _(u'active jobs for queue: %s') % job_queue

    context = {
        'object_list': jobs,
        'title': title,
        'object': job_queue,
        'hide_link': True,
        'extra_columns': [
            {
                'name': _(u'created'),
                'attribute': 'creation_datetime',
            },
            {
                'name': _(u'job type'),
                'attribute': 'get_job_type',
            },
            {
                'name': _(u'arguments'),
                'attribute': 'kwargs',
            },
        ],
    }

    if active_jobs:
        context['extra_columns'].append(
            {
                'name': _(u'worker'),
                'attribute': encapsulate(lambda x: x.worker or _(u'Unknown')),
            }
        )
    
    if error_jobs:
        context['extra_columns'].append(
            {
                'name': _(u'result'),
                'attribute': 'result',
            }
        )

    return render_to_response('generic_list.html', context,
        context_instance=RequestContext(request))


def job_queue_config_edit(request):
    Permission.objects.check_permissions(request.user, [PERMISSION_JOB_PROCESSING_CONFIGURATION])

    job_processing_config = JobProcessingConfig.get()
    
    post_action_redirect = None

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', '/')))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', '/')))
    

    if request.method == 'POST':
        form = JobProcessingConfigForm(data=request.POST)
        if form.is_valid():
            try:
                form.save()
            except Exception, exc:
                messages.error(request, _(u'Error trying to edit job processing configuration; %s') % exc)
            else:
                messages.success(request, _(u'Job processing configuration edited successfully.'))
                return HttpResponseRedirect(next)
    else:
        form = JobProcessingConfigForm(instance=job_processing_config)

    return render_to_response('generic_form.html', {
        'form': form,
        'object': job_processing_config,
        'title': _(u'Edit job processing configuration')
    }, context_instance=RequestContext(request))
    
    
def job_queue_stop(request, job_queue_pk):
    job_queue = get_object_or_404(JobQueue, pk=job_queue_pk)

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_JOB_QUEUE_START_STOP])
    except PermissionDenied:
        AccessEntry.objects.check_access(PERMISSION_JOB_QUEUE_START_STOP, request.user, job_queue)

    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', None)))
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', None)))

    if request.method == 'POST':
        try:
            job_queue.stop()
        except JobQueueAlreadyStopped:
            messages.warning(request, _(u'job queue already stopped.'))
            return HttpResponseRedirect(previous)            
        else:
            messages.success(request, _(u'Job queue stopped successfully.'))
            return HttpResponseRedirect(next)

    return render_to_response('generic_confirm.html', {
        'object': job_queue,
        'object_name': _(u'job queue'),
        'title': _(u'Are you sure you wish to stop job queue: %s?') % job_queue,
        'next': next,
        'previous': previous,
        'form_icon': u'control_stop_blue.png',
    }, context_instance=RequestContext(request))


def job_queue_start(request, job_queue_pk):
    job_queue = get_object_or_404(JobQueue, pk=job_queue_pk)

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_JOB_QUEUE_VIEW])
    except PermissionDenied:
        AccessEntry.objects.check_access(PERMISSION_JOB_QUEUE_VIEW, request.user, job_queue)

    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', None)))
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', None)))

    if request.method == 'POST':
        try:
            job_queue.start()
        except JobQueueAlreadyStarted:
            messages.warning(request, _(u'job queue already started.'))
            return HttpResponseRedirect(previous)            
        else:
            messages.success(request, _(u'Job queue started successfully.'))
            return HttpResponseRedirect(next)

    return render_to_response('generic_confirm.html', {
        'object': job_queue,
        'object_name': _(u'job queue'),
        'title': _(u'Are you sure you wish to start job queue: %s?') % job_queue,
        'next': next,
        'previous': previous,
        'form_icon': u'control_play_blue.png',
    }, context_instance=RequestContext(request))
