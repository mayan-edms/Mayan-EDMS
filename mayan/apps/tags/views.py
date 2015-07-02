from __future__ import absolute_import, unicode_literals

import logging

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _, ungettext

from acls.models import AccessControlList
from common.views import SingleObjectListView
from documents.models import Document
from documents.views import DocumentListView
from documents.permissions import permission_document_view
from permissions import Permission

from .forms import TagForm, TagListForm
from .models import Tag
from .permissions import (
    permission_tag_attach, permission_tag_create, permission_tag_delete,
    permission_tag_edit, permission_tag_remove, permission_tag_view
)

logger = logging.getLogger(__name__)


def tag_create(request):
    Permission.check_permissions(request.user, [permission_tag_create])
    redirect_url = reverse('tags:tag_list')

    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, _('Tag created succesfully.'))
            return HttpResponseRedirect(redirect_url)
    else:
        form = TagForm()

    return render_to_response('appearance/generic_form.html', {
        'title': _('Create tag'),
        'form': form,
    }, context_instance=RequestContext(request))


def tag_attach(request, document_id=None, document_id_list=None):
    if document_id:
        documents = [get_object_or_404(Document, pk=document_id)]
        post_action_redirect = reverse('tags:tag_list')
    elif document_id_list:
        documents = [get_object_or_404(Document, pk=document_id) for document_id in document_id_list.split(',')]
    else:
        messages.error(request, _('Must provide at least one document.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL)))

    try:
        Permission.check_permissions(request.user, [permission_tag_attach])
    except PermissionDenied:
        documents = AccessControlList.objects.filter_by_access(permission_tag_attach, request.user, documents)

    post_action_redirect = None
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))))

    if request.method == 'POST':
        form = TagListForm(request.POST, user=request.user)
        if form.is_valid():
            tag = form.cleaned_data['tag']
            for document in documents:
                if tag in document.tags.all():
                    messages.warning(request, _('Document "%(document)s" is already tagged as "%(tag)s"') % {
                        'document': document, 'tag': tag}
                    )
                else:
                    tag.documents.add(document)
                    messages.success(request, _('Tag "%(tag)s" attached successfully to document "%(document)s".') % {
                        'document': document, 'tag': tag}
                    )
            return HttpResponseRedirect(next)
    else:
        form = TagListForm(user=request.user)

    context = {
        'form': form,
        'previous': previous,
        'next': next,
        'title': ungettext(
            'Attach tag to document',
            'Attach tag to documents',
            len(documents)
        )
    }

    if len(documents) == 1:
        context['object'] = documents[0]

    return render_to_response('appearance/generic_form.html', context,
                              context_instance=RequestContext(request))


def tag_multiple_attach(request):
    return tag_attach(
        request, document_id_list=request.GET.get('id_list', [])
    )


class TagListView(SingleObjectListView):
    object_permission = permission_tag_view

    def get_tag_queryset(self):
        return Tag.objects.all()

    def get_queryset(self):
        self.queryset = self.get_tag_queryset()
        return super(TagListView, self).get_queryset()

    def get_extra_context(self, **kwargs):
        return {
            'title': _('Tags'),
            'hide_link': True,
            'hide_object': True,
        }


def tag_delete(request, tag_id=None, tag_id_list=None):
    post_action_redirect = None

    if tag_id:
        tags = [get_object_or_404(Tag, pk=tag_id)]
        post_action_redirect = reverse('tags:tag_list')
    elif tag_id_list:
        tags = [get_object_or_404(Tag, pk=tag_id) for tag_id in tag_id_list.split(',')]
    else:
        messages.error(request, _('Must provide at least one tag.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL)))

    try:
        Permission.check_permissions(request.user, [permission_tag_delete])
    except PermissionDenied:
        tags = AccessControlList.objects.filter_by_access(permission_tag_delete, request.user, tags)

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))))

    if request.method == 'POST':
        for tag in tags:
            try:
                tag.delete()
                messages.success(request, _('Tag "%s" deleted successfully.') % tag)
            except Exception as exception:
                messages.error(request, _('Error deleting tag "%(tag)s": %(error)s') % {
                    'tag': tag, 'error': exception
                })

        return HttpResponseRedirect(next)

    context = {
        'delete_view': True,
        'previous': previous,
        'message': _('Will be removed from all documents.'),
        'next': next,
        'title': ungettext(
            'Are you sure you wish to delete the selected tag?',
            'Are you sure you wish to delete the selected tags?',
            len(tags)
        )
    }

    if len(tags) == 1:
        context['object'] = tags[0]

    return render_to_response('appearance/generic_confirm.html', context,
                              context_instance=RequestContext(request))


def tag_multiple_delete(request):
    return tag_delete(
        request, tag_id_list=request.GET.get('id_list', [])
    )


def tag_edit(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)

    try:
        Permission.check_permissions(request.user, [permission_tag_edit])
    except PermissionDenied:
        AccessControlList.objects.check_access(permission_tag_edit, request.user, tag)

    if request.method == 'POST':
        form = TagForm(data=request.POST, instance=tag)
        if form.is_valid():
            form.save()
            messages.success(request, _('Tag updated succesfully.'))
            return HttpResponseRedirect(reverse('tags:tag_list'))
    else:
        form = TagForm(instance=tag)

    return render_to_response('appearance/generic_form.html', {
        'title': _('Edit tag: %s') % tag,
        'form': form,
        'object': tag,
    }, context_instance=RequestContext(request))


class TagTaggedItemListView(DocumentListView):
    def get_tag(self):
        return get_object_or_404(Tag, pk=self.kwargs['pk'])

    def get_document_queryset(self):
        return self.get_tag().documents.all()

    def get_extra_context(self):
        return {
            'title': _('Documents with the tag: %s') % self.get_tag(),
            'hide_links': True,
            'object': self.get_tag(),
        }


class DocumentTagListView(TagListView):
    def dispatch(self, request, *args, **kwargs):
        self.document = get_object_or_404(Document, pk=self.kwargs['pk'])

        try:
            Permission.check_permissions(request.user, [permission_document_view])
        except PermissionDenied:
            AccessControlList.objects.check_access(permission_document_view, request.user, self.document)

        return super(DocumentTagListView, self).dispatch(request, *args, **kwargs)

    def get_extra_context(self):
        return {
            'object': self.document,
            'title': _('Tags for document: %s') % self.document,
        }

    def get_tag_queryset(self):
        return self.document.tags.all()


def tag_remove(request, document_id=None, document_id_list=None, tag_id=None, tag_id_list=None):
    if document_id:
        documents = [get_object_or_404(Document, pk=document_id)]
    elif document_id_list:
        documents = [get_object_or_404(Document, pk=document_id) for document_id in document_id_list.split(',')]
    else:
        messages.error(request, _('Must provide at least one tagged document.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL)))

    try:
        Permission.check_permissions(request.user, [permission_tag_remove])
    except PermissionDenied:
        documents = AccessControlList.objects.filter_by_access(permission_tag_remove, request.user, documents, exception_on_empty=True)

    post_action_redirect = None

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))))

    context = {
        'previous': previous,
        'next': next,
    }

    template = 'appearance/generic_confirm.html'
    if tag_id:
        tags = [get_object_or_404(Tag, pk=tag_id)]
    elif tag_id_list:
        tags = [get_object_or_404(Tag, pk=tag_id) for tag_id in tag_id_list.split(',')]
    else:
        template = 'appearance/generic_form.html'

        if request.method == 'POST':
            form = TagListForm(request.POST, user=request.user)
            if form.is_valid():
                tags = [form.cleaned_data['tag']]
        else:
            if not tag_id and not tag_id_list:
                form = TagListForm(user=request.user)
                tags = None

        context['form'] = form
        if len(documents) == 1:
            context['object'] = documents[0]
            context['title'] = _('Remove tag from document: %s.') % ', '.join([unicode(d) for d in documents])
        elif len(documents) > 1:
            context['title'] = _('Remove tag from documents: %s.') % ', '.join([unicode(d) for d in documents])

    if tags:
        if len(tags) == 1:
            if len(documents) == 1:
                context['object'] = documents[0]
                context['title'] = _('Are you sure you wish to remove the tag "%(tag)s" from the document: %(document)s?') % {
                    'tag': ', '.join([unicode(d) for d in tags]), 'document': ', '.join([unicode(d) for d in documents])}
            else:
                context['title'] = _('Are you sure you wish to remove the tag "%(tag)s" from the documents: %(documents)s?') % {
                    'tag': ', '.join([unicode(d) for d in tags]), 'documents': ', '.join([unicode(d) for d in documents])}
        elif len(tags) > 1:
            if len(documents) == 1:
                context['object'] = documents[0]
                context['title'] = _('Are you sure you wish to remove the tags: %(tags)s from the document: %(document)s?') % {
                    'tags': ', '.join([unicode(d) for d in tags]), 'document': ', '.join([unicode(d) for d in documents])}
            else:
                context['title'] = _('Are you sure you wish to remove the tags %(tags)s from the documents: %(documents)s?') % {
                    'tags': ', '.join([unicode(d) for d in tags]), 'documents': ', '.join([unicode(d) for d in documents])}

    if request.method == 'POST':
        for document in documents:
            for tag in tags:
                if tag not in document.tags.all():
                    messages.warning(request, _('Document "%(document)s" wasn\'t tagged as "%(tag)s"') % {
                        'document': document, 'tag': tag}
                    )
                else:
                    tag.documents.remove(document)
                    messages.success(request, _('Tag "%(tag)s" removed successfully from document "%(document)s".') % {
                        'document': document, 'tag': tag}
                    )

        return HttpResponseRedirect(next)
    else:
        return render_to_response(template, context,
                                  context_instance=RequestContext(request))


def single_document_multiple_tag_remove(request, document_id):
    return tag_remove(request, document_id=document_id, tag_id_list=request.GET.get('id_list', []))


def multiple_documents_selection_tag_remove(request):
    return tag_remove(request, document_id_list=request.GET.get('id_list', []))
