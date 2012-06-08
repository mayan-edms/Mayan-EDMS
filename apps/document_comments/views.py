from __future__ import absolute_import

from django.shortcuts import render_to_response, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.contrib.comments.models import Comment
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.exceptions import PermissionDenied

from acls.models import AccessEntry
from permissions.models import Permission
from documents.models import Document

from .permissions import (PERMISSION_COMMENT_CREATE,
    PERMISSION_COMMENT_DELETE, PERMISSION_COMMENT_VIEW)
from .forms import CommentForm


def comment_delete(request, comment_id=None, comment_id_list=None):
    post_action_redirect = None

    if comment_id:
        comments = [get_object_or_404(Comment, pk=comment_id)]
    elif comment_id_list:
        comments = [get_object_or_404(Comment, pk=comment_id) for comment_id in comment_id_list.split(',')]

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_COMMENT_DELETE])
    except PermissionDenied:
        comments = AccessEntry.objects.filter_objects_by_access(PERMISSION_COMMENT_DELETE, request.user, comments, related='content_object')

    if not comments:
        messages.error(request, _(u'Must provide at least one comment.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', '/')))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', '/')))

    if request.method == 'POST':
        for comment in comments:
            try:
                comment.delete()
                comment.content_object.mark_indexable()
                messages.success(request, _(u'Comment "%s" deleted successfully.') % comment)
            except Exception, e:
                messages.error(request, _(u'Error deleting comment "%(comment)s": %(error)s') % {
                    'comment': comment, 'error': e
                })

        return HttpResponseRedirect(next)

    context = {
        #'object_name': _(u'comment'),
        'delete_view': True,
        'previous': previous,
        'next': next,
        'form_icon': u'comment_delete.png',
    }
    if len(comments) == 1:
        context['object'] = comments[0].content_object
        context['title'] = _(u'Are you sure you wish to delete the comment: %s?') % ', '.join([unicode(d) for d in comments])
    elif len(comments) > 1:
        context['title'] = _(u'Are you sure you wish to delete the comments: %s?') % ', '.join([unicode(d) for d in comments])

    return render_to_response('generic_confirm.html', context,
        context_instance=RequestContext(request))


def comment_multiple_delete(request):
    return comment_delete(
        request, comment_id_list=request.GET.get('id_list', [])
    )


def comment_add(request, document_id):
    document = get_object_or_404(Document, pk=document_id)

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_COMMENT_CREATE])
    except PermissionDenied:
        AccessEntry.objects.check_access(PERMISSION_COMMENT_CREATE, request.user, document)

    post_action_redirect = None

    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', '/')))

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.content_type = ContentType.objects.get_for_model(document)
            comment.object_pk = document.pk
            comment.site = Site.objects.get_current()
            comment.save()
            document.mark_indexable()

            messages.success(request, _(u'Comment added successfully.'))
            return HttpResponseRedirect(next)
    else:
        form = CommentForm()

    return render_to_response('generic_form.html', {
        'form': form,
        'title': _(u'Add comment to document: %s') % document,
        'next': next,
        'object': document,
    }, context_instance=RequestContext(request))


def comments_for_document(request, document_id):
    """
    Show a list of all the comments related to the passed object
    """
    document = get_object_or_404(Document, pk=document_id)

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_COMMENT_VIEW])
    except PermissionDenied:
        AccessEntry.objects.check_access(PERMISSION_COMMENT_VIEW, request.user, document)

    return render_to_response('generic_list.html', {
        'object': document,
        'access_object': document,
        'title': _(u'comments: %s') % document,
        'object_list': Comment.objects.for_model(document).order_by('-submit_date'),
        'hide_link': True,
        'hide_object': True,
    }, context_instance=RequestContext(request))
