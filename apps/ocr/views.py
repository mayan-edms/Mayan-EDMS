import datetime
import socket

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.views.generic.list_detail import object_list
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.conf import settings

from celery.task.control import inspect
from permissions.api import check_permissions
from documents.models import Document

from ocr import PERMISSION_OCR_DOCUMENT, PERMISSION_OCR_DOCUMENT_DELETE, \
    PERMISSION_OCR_QUEUE_ENABLE_DISABLE, PERMISSION_OCR_CLEAN_ALL_PAGES

from ocr.models import DocumentQueue, QueueDocument
from ocr.literals import QUEUEDOCUMENT_STATE_PENDING, \
    QUEUEDOCUMENT_STATE_PROCESSING, DOCUMENTQUEUE_STATE_STOPPED, \
    DOCUMENTQUEUE_STATE_ACTIVE
from ocr.exceptions import AlreadyQueued
from ocr.api import clean_pages


def _display_thumbnail(ocr_document):
    try:
        return u'<a class="fancybox" href="%(url)s"><img class="lazy-load" data-href="%(thumbnail_url)s" src="%(media_url)s/images/ajax-loader.gif" /><noscript><img src="%(thumbnail_url)s" /></noscript></a>' % {
            'url': reverse('document_preview', args=[ocr_document.document.pk]),
            'thumbnail_url': reverse('document_thumbnail', args=[ocr_document.document.pk]),
            'media_url': settings.MEDIA_URL
        }
    except:
        return u''


def queue_document_list(request, queue_name='default'):
    check_permissions(request.user, 'ocr', [PERMISSION_OCR_DOCUMENT])

    document_queue = get_object_or_404(DocumentQueue, name=queue_name)

    return object_list(
        request,
        queryset=document_queue.queuedocument_set.all(),
        template_name='generic_list.html',
        extra_context={
            'title': _(u'documents in queue: %s') % document_queue,
            'hide_object': True,
            'object': document_queue,
            'object_name': _(u'document queue'),
            'extra_columns': [
                {'name': 'document', 'attribute': lambda x: '<a href="%s">%s</a>' % (x.document.get_absolute_url(), x.document) if hasattr(x, 'document') else _(u'Missing document.')},
                {'name': _(u'thumbnail'), 'attribute': lambda x: _display_thumbnail(x)},
                {'name': 'submitted', 'attribute': lambda x: unicode(x.datetime_submitted).split('.')[0], 'keep_together':True},
                {'name': 'delay', 'attribute': 'delay'},
                {'name': 'state', 'attribute': lambda x: x.get_state_display()},
                {'name': 'node', 'attribute': 'node_name'},
                {'name': 'result', 'attribute': 'result'},
            ],
            'multi_select_as_buttons': True,
            'sidebar_subtemplates_list': [
                {
                    'title': _(u'document queue properties'),
                    'name': 'generic_subtemplate.html',
                    'content': _(u'Current state: %s') % document_queue.get_state_display(),
                }],
        },
    )


def queue_document_delete(request, queue_document_id=None, queue_document_id_list=None):
    check_permissions(request.user, 'ocr', [PERMISSION_OCR_DOCUMENT_DELETE])

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
                if queue_document.state == QUEUEDOCUMENT_STATE_PROCESSING:
                    messages.error(request, _(u'Document: %s is being processed and can\'t be deleted.') % queue_document)
                else:
                    queue_document.delete()
                    messages.success(request, _(u'Queue document: %(document)s deleted successfully.') % {
                        'document': queue_document.document})

            except Exception, e:
                messages.error(request, _(u'Error deleting document: %(document)s; %(error)s') % {
                    'document': queue_document, 'error': e})
        return HttpResponseRedirect(next)

    context = {
        'next': next,
        'previous': previous,
        'delete_view': True
    }

    if len(queue_documents) == 1:
        context['object'] = queue_documents[0]
        context['title'] = _(u'Are you sure you wish to delete queue document: %s?') % ', '.join([unicode(d) for d in queue_documents])
    elif len(queue_documents) > 1:
        context['title'] = _(u'Are you sure you wish to delete queue documents: %s?') % ', '.join([unicode(d) for d in queue_documents])

    return render_to_response('generic_confirm.html', context,
        context_instance=RequestContext(request))


def queue_document_multiple_delete(request):
    return queue_document_delete(request, queue_document_id_list=request.GET.get('id_list', []))


def submit_document(request, document_id):
    check_permissions(request.user, 'ocr', [PERMISSION_OCR_DOCUMENT])

    document = get_object_or_404(Document, pk=document_id)
    return submit_document_to_queue(request, document=document,
        post_submit_redirect=request.META['HTTP_REFERER'])


def submit_document_to_queue(request, document, post_submit_redirect=None):
    """This view is meant to be reusable"""

    try:
        document_queue = DocumentQueue.objects.queue_document(document)
        messages.success(request, _(u'Document: %(document)s was added to the OCR queue: %(queue)s.') % {
            'document': document, 'queue': document_queue.label})
    except AlreadyQueued:
        messages.warning(request, _(u'Document: %(document)s is already queued.') % {
        'document': document})
    except Exception, e:
        messages.error(request, e)

    if post_submit_redirect:
        return HttpResponseRedirect(post_submit_redirect)


def re_queue_document(request, queue_document_id=None, queue_document_id_list=None):
    check_permissions(request.user, 'ocr', [PERMISSION_OCR_DOCUMENT])

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
                queue_document.document
                if queue_document.state == QUEUEDOCUMENT_STATE_PROCESSING:
                    messages.warning(request, _(u'Document: %s is already being processed and can\'t be re-queded.') % queue_document)
                else:
                    queue_document.datetime_submitted = datetime.datetime.now()
                    queue_document.state = QUEUEDOCUMENT_STATE_PENDING
                    queue_document.delay = False
                    queue_document.result = None
                    queue_document.node_name = None
                    queue_document.save()
                    messages.success(request, _(u'Document: %(document)s was re-queued to the OCR queue: %(queue)s') % {
                        'document': queue_document.document, 'queue': queue_document.document_queue.label})
            except Document.DoesNotExist:
                messages.error(request, _(u'Document id#: %d, no longer exists.') % queue_document.document_id)
            except Exception, e:
                messages.error(request, e)
        return HttpResponseRedirect(next)

    context = {
        'next': next,
        'previous': previous,
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


def document_queue_disable(request, document_queue_id):
    check_permissions(request.user, 'ocr', [PERMISSION_OCR_QUEUE_ENABLE_DISABLE])

    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', None)))
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', None)))
    document_queue = get_object_or_404(DocumentQueue, pk=document_queue_id)

    if document_queue.state == DOCUMENTQUEUE_STATE_STOPPED:
        messages.warning(request, _(u'Document queue: %s, already stopped.') % document_queue)
        return HttpResponseRedirect(previous)

    if request.method == 'POST':
        document_queue.state = DOCUMENTQUEUE_STATE_STOPPED
        document_queue.save()
        messages.success(request, _(u'Document queue: %s, stopped successfully.') % document_queue)
        return HttpResponseRedirect(next)

    return render_to_response('generic_confirm.html', {
        'object': document_queue,
        'title': _(u'Are you sure you wish to disable document queue: %s') % document_queue,
        'next': next,
        'previous': previous,
    }, context_instance=RequestContext(request))


def document_queue_enable(request, document_queue_id):
    check_permissions(request.user, 'ocr', [PERMISSION_OCR_QUEUE_ENABLE_DISABLE])

    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', None)))
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', None)))
    document_queue = get_object_or_404(DocumentQueue, pk=document_queue_id)

    if document_queue.state == DOCUMENTQUEUE_STATE_ACTIVE:
        messages.warning(request, _(u'Document queue: %s, already active.') % document_queue)
        return HttpResponseRedirect(previous)

    if request.method == 'POST':
        document_queue.state = DOCUMENTQUEUE_STATE_ACTIVE
        document_queue.save()
        messages.success(request, _(u'Document queue: %s, activated successfully.') % document_queue)
        return HttpResponseRedirect(next)

    return render_to_response('generic_confirm.html', {
        'object': document_queue,
        'title': _(u'Are you sure you wish to activate document queue: %s') % document_queue,
        'next': next,
        'previous': previous,
    }, context_instance=RequestContext(request))


def all_document_ocr_cleanup(request):
    check_permissions(request.user, 'ocr', [PERMISSION_OCR_CLEAN_ALL_PAGES])

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', None)))
    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', None)))

    if request.method != 'POST':
        return render_to_response('generic_confirm.html', {
            'previous': previous,
            'next': next,
            'message': _(u'On large databases this operation may take some time to execute.'),
        }, context_instance=RequestContext(request))
    else:
        try:
            clean_pages()
            messages.success(request, _(u'Document pages content clean up complete.'))
        except Exception, e:
            messages.error(request, _(u'Document pages content clean up error: %s') % e)

        return HttpResponseRedirect(next)


def display_link(obj):
    output = []
    if hasattr(obj, 'get_absolute_url'):
        output.append(u'<a href="%(url)s">%(obj)s</a>'% {
            'url': obj.get_absolute_url(),
            'obj': obj
        })
    if output:
        return u''.join(output)
    else:
        return obj


def node_active_list(request):
    check_permissions(request.user, 'ocr', [PERMISSION_OCR_DOCUMENT])

    i = inspect()
    active_tasks = []
    try:
        active_nodes = i.active()
        if active_nodes:
            for node, tasks in active_nodes.items():
                for task in tasks:
                    task_info = {
                        'node': node,
                        'task_name': task['name'],
                        'task_id': task['id'],
                        'related_object': None,
                    }
                    if task['name'] == u'ocr.tasks.task_process_queue_document':
                        task_info['related_object'] = QueueDocument.objects.get(pk=eval(task['args'])[0]).document
                    active_tasks.append(task_info)
    except socket.error:
        active_tasks = []

    return render_to_response('generic_list.html', {
        'object_list': active_tasks,
        'title': _(u'active tasks'),
        'hide_links': True,
        'hide_object': True,
        'extra_columns': [
            {'name': _(u'node'), 'attribute': 'node'},
            {'name': _(u'task id'), 'attribute': 'task_id'},
            {'name': _(u'task name'), 'attribute': 'task_name'},
            {'name': _(u'related object'), 'attribute': lambda x: display_link(x['related_object']) if x['related_object'] else u''}
        ],
    }, context_instance=RequestContext(request))
