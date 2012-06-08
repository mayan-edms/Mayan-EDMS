from __future__ import absolute_import

import logging

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import PermissionDenied

from permissions.models import Permission
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


def tag_attach(request, document_id):
    document = get_object_or_404(Document, pk=document_id)

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_TAG_ATTACH])
    except PermissionDenied:
        AccessEntry.objects.check_access(PERMISSION_TAG_ATTACH, request.user, document)

    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', reverse('document_tags', args=[document.pk]))))

    if request.method == 'POST':
        form = TagListForm(request.POST, user=request.user)
        if form.is_valid():
            tag = form.cleaned_data['tag']
            if tag in document.tags.all():
                messages.warning(request, _(u'Document is already tagged as "%s"') % tag)
                return HttpResponseRedirect(next)

            document.tags.add(tag)
            document.mark_indexable()
            messages.success(request, _(u'Tag "%s" attached successfully.') % tag)
            return HttpResponseRedirect(next)
    else:
        form = TagListForm(user=request.user)

    return render_to_response('generic_form.html', {
        'title': _(u'attach tag to: %s') % document,
        'form': form,
        'object': document,
        'next': next,
    },
    context_instance=RequestContext(request))


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
                for document in Document.objects.filter(tags__in=[tag]):
                    document.mark_indexable()
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
            for document in Document.objects.filter(tags__in=[tag]):
                document.mark_indexable()
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


def tag_remove(request, document_id, tag_id=None, tag_id_list=None):
    document = get_object_or_404(Document, pk=document_id)

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_TAG_REMOVE])
    except PermissionDenied:
        AccessEntry.objects.check_access(PERMISSION_TAG_REMOVE, request.user, document)

    post_action_redirect = None

    if tag_id:
        tags = [get_object_or_404(Tag, pk=tag_id)]
    elif tag_id_list:
        tags = [get_object_or_404(Tag, pk=tag_id) for tag_id in tag_id_list.split(',')]
    else:
        messages.error(request, _(u'Must provide at least one tag.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', '/')))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', '/')))

    if request.method == 'POST':
        for tag in tags:
            try:
                document.tags.remove(tag)
                document.mark_indexable()
                messages.success(request, _(u'Tag "%s" removed successfully.') % tag)
            except Exception, e:
                messages.error(request, _(u'Error deleting tag "%(tag)s": %(error)s') % {
                    'tag': tag, 'error': e
                })

        return HttpResponseRedirect(next)

    context = {
        'previous': previous,
        'next': next,
        'form_icon': u'tag_blue_delete.png',
        'object': document,
    }

    if len(tags) == 1:
        context['title'] = _(u'Are you sure you wish to remove the tag: %s?') % ', '.join([unicode(d) for d in tags])
    elif len(tags) > 1:
        context['title'] = _(u'Are you sure you wish to remove the tags: %s?') % ', '.join([unicode(d) for d in tags])

    return render_to_response('generic_confirm.html', context,
        context_instance=RequestContext(request))


def tag_multiple_remove(request, document_id):
    return tag_remove(request, document_id=document_id, tag_id_list=request.GET.get('id_list', []))


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
