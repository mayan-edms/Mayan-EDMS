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
from .models import JobQueue, JobQueueItem, Worker
from .permissions import (PERMISSION_JOB_QUEUE_VIEW,
    PERMISSION_JOB_PROCESSING_CONFIGURATION, PERMISSION_JOB_QUEUE_START_STOP,
    PERMISSION_JOB_REQUEUE)


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
            {
                'name': _(u'priority'),
                'attribute': 'priority',
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


def job_requeue(request, job_item_pk):
    job = get_object_or_404(JobQueueItem, pk=job_item_pk)

    #try:
    #    Permission.objects.check_permissions(request.user, [PERMISSION_JOB_REQUEUE])
    #except PermissionDenied:
    #    AccessEntry.objects.check_access(PERMISSION_JOB_REQUEUE, request.user, job_queue)

    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', None)))
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', None)))

    if request.method == 'POST':
        #try:
        job.requeue()
        #except JobQueueAlreadyStarted:
        #    messages.warning(request, _(u'job ueue already started.'))
        #    return HttpResponseRedirect(previous)            
        #else:
        messages.success(request, _(u'Job requeue successfully.'))
        return HttpResponseRedirect(next)

    return render_to_response('generic_confirm.html', {
        'object': job,
        'object_name': _(u'job'),
        'title': _(u'Are you sure you wish to requeue job: %s?') % job,
        'next': next,
        'previous': previous,
        'form_icon': u'cog_add.png',
    }, context_instance=RequestContext(request))


def job_delete(request, job_item_pk):
    job = get_object_or_404(JobQueueItem, pk=job_item_pk)

    #try:
    #    Permission.objects.check_permissions(request.user, [PERMISSION_JOB_REQUEUE])
    #except PermissionDenied:
    #    AccessEntry.objects.check_access(PERMISSION_JOB_REQUEUE, request.user, job_queue)

    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', None)))
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', None)))

    if request.method == 'POST':
        try:
            job.delete()
        except Exception, exc:
            messages.warning(request, _(u'Error deleting job; %s.') % exc)
            return HttpResponseRedirect(previous)            
        else:
            messages.success(request, _(u'Job deleted successfully.'))
            return HttpResponseRedirect(next)

    return render_to_response('generic_confirm.html', {
        'object': job,
        'object_name': _(u'job'),
        'title': _(u'Are you sure you wish to delete job: %s?') % job,
        'next': next,
        'previous': previous,
        'form_icon': u'cog_delete.png',
    }, context_instance=RequestContext(request))


def worker_terminate(request, worker_pk):
    worker = get_object_or_404(Worker, pk=worker_pk)

    #try:
    #    Permission.objects.check_permissions(request.user, [PERMISSION_JOB_REQUEUE])
    #except PermissionDenied:
    #    AccessEntry.objects.check_access(PERMISSION_JOB_REQUEUE, request.user, job_queue)

    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', None)))
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', None)))

    if request.method == 'POST':
        try:
            worker.terminate()
        except Exception, exc:
            messages.warning(request, _(u'Error terminating worker; %s.') % exc)
            return HttpResponseRedirect(previous)            
        else:
            messages.success(request, _(u'Worker terminated successfully.'))
            return HttpResponseRedirect(next)

    return render_to_response('generic_confirm.html', {
        'object': worker,
        'object_name': _(u'worker'),
        'title': _(u'Are you sure you wish to terminate worker: %s?') % worker,
        'next': next,
        'previous': previous,
        'form_icon': u'lorry_delete.png',
    }, context_instance=RequestContext(request))

'''
def re_queue_document(request, queue_document_id=None, queue_document_id_list=None):
    Permission.objects.check_permissions(request.user, [PERMISSION_OCR_DOCUMENT])

    if queue_document_id:
        queue_documents = [get_object_or_404(QueueDocument, pk=queue_document_id)]
    elif queue_document_id_list:
        queue_documents = [get_object_or_404(QueueDocument, pk=queue_document_id) for queue_document_id in queue_document_id_list.split(',')]
    else:
        messages.error(request, _(u'Must provide at least one queue document.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', None)))
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', None)))

    if request.method == 'POST':
        for queue_document in queue_documents:
            try:
                queue_document.requeue()
                messages.success(
                    request,
                    _(u'Document: %(document)s was re-queued to the OCR queue: %(queue)s') % {
                        'document': queue_document.document_version.document,
                        'queue': queue_document.document_queue.label
                    }
                )
            except Document.DoesNotExist:
                messages.error(request, _(u'Document no longer in queue.'))
            except ReQueueError:
                messages.warning(
                    request,
                    _(u'Document: %s is already being processed and can\'t be re-queded.') % queue_document
                )
        return HttpResponseRedirect(next)

    context = {
        'next': next,
        'previous': previous,
        'form_icon': u'hourglass_add.png',
    }

    if len(queue_documents) == 1:
        context['object'] = queue_documents[0]
        context['title'] = _(u'Are you sure you wish to re-queue document: %s?') % ', '.join([unicode(d) for d in queue_documents])
    elif len(queue_documents) > 1:
        context['title'] = _(u'Are you sure you wish to re-queue documents: %s?') % ', '.join([unicode(d) for d in queue_documents])

    return render_to_response('generic_confirm.html', context,
        context_instance=RequestContext(request))


def re_queue_multiple_document(request):
    return re_queue_document(request, queue_document_id_list=request.GET.get('id_list', []))
'''
