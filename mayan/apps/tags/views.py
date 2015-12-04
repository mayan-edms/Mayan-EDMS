from __future__ import absolute_import, unicode_literals

import logging

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse, reverse_lazy
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _, ungettext

from acls.models import AccessControlList
from common.views import (
    SingleObjectCreateView, SingleObjectEditView, SingleObjectListView
)
from documents.models import Document
from documents.views import DocumentListView
from documents.permissions import permission_document_view
from permissions import Permission

from .forms import TagListForm
from .models import Tag
from .permissions import (
    permission_tag_attach, permission_tag_create, permission_tag_delete,
    permission_tag_edit, permission_tag_remove, permission_tag_view
)

logger = logging.getLogger(__name__)


class TagCreateView(SingleObjectCreateView):
    extra_context = {'title': _('Create tag')}
    fields = ('label', 'color')
    model = Tag
    post_action_redirect = reverse_lazy('tags:tag_list')
    view_permission = permission_tag_create


def tag_attach(request, document_id=None, document_id_list=None):
    if document_id:
        queryset = Document.objects.filter(pk=document_id)
        post_action_redirect = reverse('tags:tag_list')
    elif document_id_list:
        queryset = Document.objects.filter(pk__in=document_id_list)

    try:
        Permission.check_permissions(request.user, (permission_tag_attach,))
    except PermissionDenied:
        queryset = AccessControlList.objects.filter_by_access(
            permission_tag_attach, request.user, queryset
        )

    if not queryset:
        if document_id:
            raise PermissionDenied
        else:
            messages.error(request, _('Must provide at least one document.'))
            return HttpResponseRedirect(
                request.META.get(
                    'HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL)
                )
            )

    post_action_redirect = None
    previous = request.POST.get(
        'previous', request.GET.get(
            'previous', request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))
        )
    )
    next = request.POST.get(
        'next', request.GET.get(
            'next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))
        )
    )

    if request.method == 'POST':
        form = TagListForm(request.POST, user=request.user)
        if form.is_valid():
            tag = form.cleaned_data['tag']
            for document in queryset:
                if tag in document.attached_tags().all():
                    messages.warning(
                        request, _(
                            'Document "%(document)s" is already tagged as "%(tag)s"'
                        ) % {
                            'document': document, 'tag': tag
                        }
                    )
                else:
                    tag.documents.add(document)
                    messages.success(
                        request,
                        _(
                            'Tag "%(tag)s" attached successfully to document "%(document)s".'
                        ) % {
                            'document': document, 'tag': tag
                        }
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
            queryset.count()
        )
    }

    if queryset.count() == 1:
        context['object'] = queryset.first()

    return render_to_response(
        'appearance/generic_form.html', context,
        context_instance=RequestContext(request)
    )


def tag_multiple_attach(request):
    return tag_attach(
        request, document_id_list=request.GET.get(
            'id_list', request.POST.get('id_list', '')
        ).split(',')
    )


class TagListView(SingleObjectListView):
    object_permission = permission_tag_view

    def get_extra_context(self):
        return {
            'hide_link': True,
            'title': _('Tags'),
        }

    def get_queryset(self):
        self.queryset = self.get_tag_queryset()
        return super(TagListView, self).get_queryset()

    def get_tag_queryset(self):
        return Tag.objects.all()


def tag_delete(request, tag_id=None, tag_id_list=None):
    post_action_redirect = None

    if tag_id:
        queryset = Tag.objects.filter(pk=tag_id)
        post_action_redirect = reverse('tags:tag_list')
    elif tag_id_list:
        queryset = Tag.objects.filter(pk__in=tag_id_list)

    if not queryset:
        messages.error(request, _('Must provide at least one tag.'))
        return HttpResponseRedirect(
            request.META.get(
                'HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL)
            )
        )

    try:
        Permission.check_permissions(request.user, (permission_tag_delete,))
    except PermissionDenied:
        queryset = AccessControlList.objects.filter_by_access(
            permission_tag_delete, request.user, queryset
        )

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))))

    if request.method == 'POST':
        for tag in queryset:
            try:
                tag.delete()
                messages.success(
                    request, _('Tag "%s" deleted successfully.') % tag
                )
            except Exception as exception:
                messages.error(
                    request, _('Error deleting tag "%(tag)s": %(error)s') % {
                        'tag': tag, 'error': exception
                    }
                )

        return HttpResponseRedirect(next)

    context = {
        'delete_view': True,
        'previous': previous,
        'message': _('Will be removed from all documents.'),
        'next': next,
        'title': ungettext(
            'Delete the selected tag?',
            'Delete the selected tags?',
            queryset.count()
        )
    }

    if queryset.count() == 1:
        context['object'] = queryset.first()

    return render_to_response(
        'appearance/generic_confirm.html', context,
        context_instance=RequestContext(request)
    )


def tag_multiple_delete(request):
    return tag_delete(
        request, tag_id_list=request.GET.get(
            'id_list', request.POST.get('id_list', '')
        ).split(',')
    )


class TagEditView(SingleObjectEditView):
    fields = ('label', 'color')
    model = Tag
    object_permission = permission_tag_edit
    post_action_redirect = reverse_lazy('tags:tag_list')

    def get_extra_context(self):
        return {
            'object': self.get_object(),
            'title': _('Edit tag: %s') % self.get_object(),
        }


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
            Permission.check_permissions(
                request.user, (permission_document_view,)
            )
        except PermissionDenied:
            AccessControlList.objects.check_access(
                permission_document_view, request.user, self.document
            )

        return super(
            DocumentTagListView, self
        ).dispatch(request, *args, **kwargs)

    def get_extra_context(self):
        return {
            'hide_link': True,
            'object': self.document,
            'title': _('Tags for document: %s') % self.document,
        }

    def get_tag_queryset(self):
        return self.document.attached_tags().all()


def tag_remove(request, document_id=None, document_id_list=None, tag_id=None, tag_id_list=None):
    if document_id:
        documents = Document.objects.filter(pk=document_id)
    elif document_id_list:
        documents = Document.objects.filter(pk__in=document_id_list)

    if not documents:
        messages.error(
            request, _('Must provide at least one tagged document.')
        )
        return HttpResponseRedirect(
            request.META.get(
                'HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL)
            )
        )

    try:
        Permission.check_permissions(request.user, (permission_tag_remove,))
    except PermissionDenied:
        documents = AccessControlList.objects.filter_by_access(
            permission_tag_remove, request.user, documents
        )

    post_action_redirect = None

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL))))

    context = {
        'previous': previous,
        'next': next,
    }

    template = 'appearance/generic_confirm.html'
    if tag_id:
        tags = Tag.objects.filter(pk=tag_id)
    elif tag_id_list:
        tags = Tag.objects.filter(pk__in=tag_id_list)
    else:
        template = 'appearance/generic_form.html'

        if request.method == 'POST':
            form = TagListForm(request.POST, user=request.user)
            if form.is_valid():
                tags = Tag.objects.filter(pk=form.cleaned_data['tag'].pk)
        else:
            if not tag_id and not tag_id_list:
                form = TagListForm(user=request.user)
                tags = Tag.objects.none()

        context['form'] = form
        if len(documents) == 1:
            context['object'] = documents.first()
            context['title'] = _(
                'Remove tag from document: %s.'
            ) % ', '.join([unicode(d) for d in documents])
        elif len(documents) > 1:
            context['title'] = _(
                'Remove tag from documents: %s.'
            ) % ', '.join([unicode(d) for d in documents])

    if tags:
        if tags.count() == 1:
            if documents.count() == 1:
                context['object'] = documents.first()
                context['title'] = _(
                    'Remove the tag "%(tag)s" from the document: %(document)s?'
                ) % {
                    'tag': ', '.join([unicode(d) for d in tags]),
                    'document': ', '.join([unicode(d) for d in documents])
                }
            else:
                context['title'] = _(
                    'Remove the tag "%(tag)s" from the documents: %(documents)s?'
                ) % {
                    'tag': ', '.join([unicode(d) for d in tags]),
                    'documents': ', '.join([unicode(d) for d in documents])
                }
        elif tags.count() > 1:
            if documents.count() == 1:
                context['object'] = documents.first()
                context['title'] = _(
                    'Remove the tags: %(tags)s from the document: %(document)s?'
                ) % {
                    'tags': ', '.join([unicode(d) for d in tags]),
                    'document': ', '.join([unicode(d) for d in documents])
                }
            else:
                context['title'] = _(
                    'Remove the tags %(tags)s from the documents: %(documents)s?'
                ) % {
                    'tags': ', '.join([unicode(d) for d in tags]),
                    'documents': ', '.join([unicode(d) for d in documents])
                }

    if request.method == 'POST':
        for document in documents:
            for tag in tags:
                if tag not in document.attached_tags().all():
                    messages.warning(
                        request, _(
                            'Document "%(document)s" wasn\'t tagged as "%(tag)s"'
                        ) % {
                            'document': document, 'tag': tag
                        }
                    )
                else:
                    tag.documents.remove(document)
                    messages.success(
                        request, _(
                            'Tag "%(tag)s" removed successfully from document "%(document)s".'
                        ) % {
                            'document': document, 'tag': tag
                        }
                    )

        return HttpResponseRedirect(next)
    else:
        return render_to_response(
            template, context, context_instance=RequestContext(request)
        )


def single_document_multiple_tag_remove(request, document_id):
    return tag_remove(
        request, document_id=document_id,
        tag_id_list=request.GET.get(
            'id_list', request.POST.get('id_list', '')
        ).split(',')
    )


def multiple_documents_selection_tag_remove(request):
    return tag_remove(
        request, document_id_list=request.GET.get(
            'id_list', request.POST.get('id_list', '')
        ).split(',')
    )
