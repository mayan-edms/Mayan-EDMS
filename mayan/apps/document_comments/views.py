from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from acls.models import AccessControlList
from common.generics import SingleObjectListView
from documents.models import Document
from permissions import Permission

from .forms import CommentForm
from .models import Comment
from .permissions import (
    permission_comment_create, permission_comment_delete,
    permission_comment_view
)


def comment_delete(request, comment_id=None, comment_id_list=None):
    post_action_redirect = None

    if comment_id:
        comments = [get_object_or_404(Comment, pk=comment_id)]
    elif comment_id_list:
        comments = [
            get_object_or_404(
                Comment, pk=comment_id
            ) for comment_id in comment_id_list.split(',')
        ]

    try:
        Permission.check_permissions(request.user, (
            permission_comment_delete,))
    except PermissionDenied:
        comments = AccessControlList.objects.filter_by_access(
            permission_comment_delete, request.user, comments,
        )

    if not comments:
        messages.error(request, _('Must provide at least one comment.'))
        return HttpResponseRedirect(
            request.META.get(
                'HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL)
            )
        )

    previous = request.POST.get(
        'previous', request.GET.get('previous', request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL)))
    )
    next = request.POST.get(
        'next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL)))
    )

    if request.method == 'POST':
        for comment in comments:
            try:
                comment.delete()
                messages.success(
                    request, _('Comment "%s" deleted successfully.') % comment
                )
            except Exception as exception:
                messages.error(
                    request, _(
                        'Error deleting comment "%(comment)s": %(error)s'
                    ) % {
                        'comment': comment, 'error': exception
                    }
                )

        return HttpResponseRedirect(next)

    context = {
        'delete_view': True,
        'previous': previous,
        'next': next,
    }
    if len(comments) == 1:
        context['object'] = comments[0].document
        context['title'] = _('Delete comment?')
    elif len(comments) > 1:
        context['title'] = _('Delete comments?')

    return render_to_response('appearance/generic_confirm.html', context,
                              context_instance=RequestContext(request))


def comment_multiple_delete(request):
    return comment_delete(
        request, comment_id_list=request.GET.get('id_list', [])
    )


def comment_add(request, document_id):
    document = get_object_or_404(Document, pk=document_id)

    try:
        Permission.check_permissions(
            request.user, (permission_comment_create,)
        )
    except PermissionDenied:
        AccessControlList.objects.check_access(
            permission_comment_create, request.user, document
        )

    post_action_redirect = None

    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))))

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.document = document
            comment.save()

            messages.success(request, _('Comment added successfully.'))
            return HttpResponseRedirect(next)
    else:
        form = CommentForm()

    return render_to_response('appearance/generic_form.html', {
        'form': form,
        'title': _('Add comment to document: %s') % document,
        'next': next,
        'object': document,
    }, context_instance=RequestContext(request))


class DocumentCommentListView(SingleObjectListView):
    def get_document(self):
        return get_object_or_404(Document, pk=self.kwargs['pk'])

    def get_queryset(self):
        try:
            Permission.check_permissions(
                self.request.user, (permission_comment_view,)
            )
        except PermissionDenied:
            AccessControlList.objects.check_access(
                permission_comment_view, self.request.user, self.get_document()
            )

        return self.get_document().comments.all()

    def get_extra_context(self):
        return {
            'hide_link': True,
            'hide_object': True,
            'object': self.get_document(),
            'title': _('Comments for document: %s') % self.get_document(),
        }
