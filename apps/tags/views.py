from __future__ import absolute_import

import logging

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import PermissionDenied

from permissions import Permission
from taggit.models import Tag
from documents.models import Document
from documents.views import document_list
from documents.permissions import PERMISSION_DOCUMENT_VIEW
from acls.models import AccessEntry
from acls.views import acl_list_for
from acls.utils import apply_default_acls

from .forms import TagListForm, TagForm
from .models import TagProperties
from .permissions import (PERMISSION_TAG_CREATE, PERMISSION_TAG_ATTACH,
    PERMISSION_TAG_REMOVE, PERMISSION_TAG_DELETE, PERMISSION_TAG_EDIT,
    PERMISSION_TAG_VIEW)

logger = logging.getLogger(__name__)


def tag_create(request):
    Permission.objects.check_permissions(request.user, [PERMISSION_TAG_CREATE])
    redirect_url = reverse('tag_list')
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', redirect_url)))

    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag_name = form.cleaned_data['name']

            if tag_name in Tag.objects.values_list('name', flat=True):
                messages.error(request, _(u'Tag already exists.'))
                return HttpResponseRedirect(previous)

            tag = Tag(name=tag_name)
            tag.save()
            TagProperties(tag=tag, color=form.cleaned_data['color']).save()
            apply_default_acls(tag, request.user)

            messages.success(request, _(u'Tag created succesfully.'))
            return HttpResponseRedirect(redirect_url)
    else:
        form = TagForm()

    return render_to_response('generic_form.html', {
        'title': _(u'create tag'),
        'form': form,
    },
    context_instance=RequestContext(request))


def tag_attach(request, document_id=None, document_id_list=None):
    if document_id:
        documents = [get_object_or_404(Document, pk=document_id)]
        post_action_redirect = reverse('tag_list')
    elif document_id_list:
        documents = [get_object_or_404(Document, pk=document_id) for document_id in document_id_list.split(',')]
    else:
        messages.error(request, _(u'Must provide at least one document.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_TAG_ATTACH])
    except PermissionDenied:
        documents = AccessEntry.objects.filter_objects_by_access(PERMISSION_TAG_ATTACH, request.user, documents)

    post_action_redirect = None
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', '/')))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', '/')))

    if request.method == 'POST':
        form = TagListForm(request.POST, user=request.user)
        if form.is_valid():
            tag = form.cleaned_data['tag']
            for document in documents:
                if tag in document.tags.all():
                    messages.warning(request, _(u'Document "%(document)s" is already tagged as "%(tag)s"') % {
                        'document': document, 'tag': tag}
                    )
                else:
                    document.tags.add(tag)
                    messages.success(request, _(u'Tag "%(tag)s" attached successfully to document "%(document)s".') % {
                        'document': document, 'tag': tag}
                    )
            return HttpResponseRedirect(next)
    else:
        form = TagListForm(user=request.user)

    context = {
        'object_name': _(u'document'),
        'form': form,
        'previous': previous,
        'next': next,
    }
    
    if len(documents) == 1:
        context['object'] = documents[0]
        context['title'] = _(u'Attach tag to document: %s.') % ', '.join([unicode(d) for d in documents])
    elif len(documents) > 1:
        context['title'] = _(u'Attach tag to documents: %s.') % ', '.join([unicode(d) for d in documents])

    return render_to_response('generic_form.html', context,
        context_instance=RequestContext(request))
        

def tag_multiple_attach(request):
    return tag_attach(
        request, document_id_list=request.GET.get('id_list', [])
    )


def tag_list(request, queryset=None, extra_context=None):
    context = {
        'title': _(u'tags'),
        'hide_link': True,
        'multi_select_as_buttons': True,
        'hide_object': True,
    }
    if extra_context:
        context.update(extra_context)

    queryset = queryset if not (queryset is None) else Tag.objects.all()

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_TAG_VIEW])
    except PermissionDenied:
        queryset = AccessEntry.objects.filter_objects_by_access(PERMISSION_TAG_VIEW, request.user, queryset)

    context['object_list'] = queryset

    return render_to_response('generic_list.html',
        context,
        context_instance=RequestContext(request)
    )


def tag_delete(request, tag_id=None, tag_id_list=None):
    post_action_redirect = None

    if tag_id:
        tags = [get_object_or_404(Tag, pk=tag_id)]
        post_action_redirect = reverse('tag_list')
    elif tag_id_list:
        tags = [get_object_or_404(Tag, pk=tag_id) for tag_id in tag_id_list.split(',')]
    else:
        messages.error(request, _(u'Must provide at least one tag.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_TAG_DELETE])
    except PermissionDenied:
        tags = AccessEntry.objects.filter_objects_by_access(PERMISSION_TAG_DELETE, request.user, tags)

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', '/')))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', '/')))

    if request.method == 'POST':
        for tag in tags:
            try:
                tag.delete()
                messages.success(request, _(u'Tag "%s" deleted successfully.') % tag)
            except Exception, e:
                messages.error(request, _(u'Error deleting tag "%(tag)s": %(error)s') % {
                    'tag': tag, 'error': e
                })

        return HttpResponseRedirect(next)

    context = {
        'object_name': _(u'tag'),
        'delete_view': True,
        'previous': previous,
        'next': next,
        'form_icon': u'tag_blue_delete.png',
    }
    if len(tags) == 1:
        context['object'] = tags[0]
        context['title'] = _(u'Are you sure you wish to delete the tag: %s?') % ', '.join([unicode(d) for d in tags])
        context['message'] = _('Will be removed from all documents.')
    elif len(tags) > 1:
        context['title'] = _(u'Are you sure you wish to delete the tags: %s?') % ', '.join([unicode(d) for d in tags])
        context['message'] = _('Will be removed from all documents.')

    return render_to_response('generic_confirm.html', context,
        context_instance=RequestContext(request))


def tag_multiple_delete(request):
    return tag_delete(
        request, tag_id_list=request.GET.get('id_list', [])
    )


def tag_edit(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_TAG_EDIT])
    except PermissionDenied:
        AccessEntry.objects.check_access(PERMISSION_TAG_EDIT, request.user, tag)

    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag.name = form.cleaned_data['name']
            tag.save()
            tag_properties = tag.tagproperties_set.get()
            tag_properties.color = form.cleaned_data['color']
            tag_properties.save()
            messages.success(request, _(u'Tag updated succesfully.'))
            return HttpResponseRedirect(reverse('tag_list'))
    else:
        form = TagForm(initial={
            'name': tag.name,
            'color': tag.tagproperties_set.get().color
        })

    return render_to_response('generic_form.html', {
        'title': _(u'edit tag: %s') % tag,
        'form': form,
        'object': tag,
        'object_name': _(u'tag'),
    },
    context_instance=RequestContext(request))


def tag_tagged_item_list(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)

    return document_list(
        request,
        object_list=Document.objects.filter(tags__in=[tag]),
        title=_('documents with the tag "%s"') % tag,
        extra_context={
            'object': tag,
            'object_name': _(u'tag'),
        }
    )


def document_tags(request, document_id):
    document = get_object_or_404(Document, pk=document_id)

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_DOCUMENT_VIEW])
    except PermissionDenied:
        AccessEntry.objects.check_access(PERMISSION_DOCUMENT_VIEW, request.user, document)

    context = {
        'object': document,
        'document': document,
        'title': _(u'tags for: %s') % document,
    }

    return tag_list(request, queryset=document.tags.all(), extra_context=context)


def tag_remove(request, document_id=None, document_id_list=None, tag_id=None, tag_id_list=None):
    if document_id:
        documents = [get_object_or_404(Document, pk=document_id)]
    elif document_id_list:
        documents = [get_object_or_404(Document, pk=document_id) for document_id in document_id_list.split(',')]
    else:
        messages.error(request, _(u'Must provide at least one tagged document.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_TAG_REMOVE])
    except PermissionDenied:
        documents = AccessEntry.objects.filter_objects_by_access(PERMISSION_TAG_REMOVE, request.user, documents, exception_on_empty=True)

    post_action_redirect = None

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', '/')))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', '/')))

    context = {
        'previous': previous,
        'next': next,
        'form_icon': u'tag_blue_delete.png',
    }

    template = 'generic_confirm.html'
    if tag_id:
        tags = [get_object_or_404(Tag, pk=tag_id)]
    elif tag_id_list:
        tags = [get_object_or_404(Tag, pk=tag_id) for tag_id in tag_id_list.split(',')]
    else:
        template = 'generic_form.html'

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
            context['title'] = _(u'Remove tag from document: %s.') % ', '.join([unicode(d) for d in documents])
        elif len(documents) > 1:
            context['title'] = _(u'Remove tag from documents: %s.') % ', '.join([unicode(d) for d in documents])

    if tags:
        if len(tags) == 1:
            if len(documents) == 1:
                context['object'] = documents[0]
                context['title'] = _(u'Are you sure you wish to remove the tag "%(tag)s" from the document: %(document)s?') % {
                    'tag': ', '.join([unicode(d) for d in tags]), 'document': ', '.join([unicode(d) for d in documents])}
            else:
                context['title'] = _(u'Are you sure you wish to remove the tag "%(tag)s" from the documents: %(documents)s?') % {
                    'tag': ', '.join([unicode(d) for d in tags]), 'documents': ', '.join([unicode(d) for d in documents])}
        elif len(tags) > 1:
            if len(documents) == 1:
                context['object'] = documents[0]
                context['title'] = _(u'Are you sure you wish to remove the tags: %(tags)s from the document: %(document)s?') % {
                    'tags': ', '.join([unicode(d) for d in tags]), 'document': ', '.join([unicode(d) for d in documents])}
            else:
                context['title'] = _(u'Are you sure you wish to remove the tags %(tags)s from the documents: %(documents)s?') % {
                    'tags': ', '.join([unicode(d) for d in tags]), 'documents': ', '.join([unicode(d) for d in documents])}

    if request.method == 'POST':
        for document in documents:
            for tag in tags:
                if tag not in document.tags.all():
                    messages.warning(request, _(u'Document "%(document)s" wasn\'t tagged as "%(tag)s"') % {
                        'document': document, 'tag': tag}
                    )
                else:
                    document.tags.remove(tag)
                    messages.success(request, _(u'Tag "%(tag)s" removed successfully from document "%(document)s".') % {
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


def tag_acl_list(request, tag_pk):
    tag = get_object_or_404(Tag, pk=tag_pk)
    logger.debug('tag: %s' % tag)

    return acl_list_for(
        request,
        tag,
        extra_context={
            'object': tag,
        }
    )
