from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.views.generic.list_detail import object_list
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied

from documents import PERMISSION_DOCUMENT_VIEW
from documents.models import Document
from permissions.api import check_permissions

from folders.models import Folder, FolderDocument
from folders.forms import FolderForm, AddDocumentForm


def folder_list(request):
    return object_list(
        request,
        queryset=Folder.objects.filter(user=request.user),
        template_name='generic_list.html',
        extra_context={
            'title': _(u'folders'),
            'multi_select_as_buttons': True,
            'extra_columns': [
                {'name': _(u'created'), 'attribute': 'datetime_created'},
                {'name': _(u'documents'), 'attribute': lambda x: x.folderdocument_set.count()}
            ]
        },
    )


def folder_create(request):
    if request.method == 'POST':
        form = FolderForm(request.POST)
        if form.is_valid():
            folder, created = Folder.objects.get_or_create(user=request.user, title=form.cleaned_data['title'])
            if created:
                messages.success(request, _(u'Folder created successfully'))
                return HttpResponseRedirect(reverse('folder_list'))
            else:
                messages.error(request, _(u'A folder named: %s, already exists.') % form.cleaned_data['title'])
    else:
        form = FolderForm()

    return render_to_response('generic_form.html', {
        'title': _(u'create folder'),
        'form': form,
    },
    context_instance=RequestContext(request))


def folder_edit(request, folder_id):
    folder = get_object_or_404(Folder, pk=folder_id)

    if not request.user.is_staff and not request.user.is_superuser and not request.user == folder.user:
        raise PermissionDenied

    if request.method == 'POST':
        form = FolderForm(request.POST)
        if form.is_valid():
            folder.title = form.cleaned_data['title']
            try:
                folder.save()
                messages.success(request, _(u'Folder edited successfully'))
                return HttpResponseRedirect(reverse('folder_list'))
            except Exception, e:
                messages.error(request, _(u'Error editing folder; %s') % e)
    else:
        form = FolderForm(instance=folder)

    return render_to_response('generic_form.html', {
        'title': _(u'edit folder: %s') % folder,
        'form': form,
        'object': folder,
    },
    context_instance=RequestContext(request))


def folder_delete(request, folder_id):
    folder = get_object_or_404(Folder, pk=folder_id)

    if not request.user.is_staff and not request.user.is_superuser and not request.user == folder.user:
        raise PermissionDenied

    post_action_redirect = reverse('folder_list')

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', '/')))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', '/')))

    if request.method == 'POST':
        try:
            folder.delete()
            messages.success(request, _(u'Folder: %s deleted successfully.') % folder)
        except Exception, e:
            messages.error(request, _(u'Folder: %(folder)s delete error: %(error)s') % {
                'folder': folder, 'error': e})

        return HttpResponseRedirect(next)

    context = {
        'object_name': _(u'folder'),
        'delete_view': True,
        'previous': previous,
        'next': next,
        'object': folder,
        'title': _(u'Are you sure you with to delete the folder: %s?') % folder
    }

    return render_to_response('generic_confirm.html', context,
        context_instance=RequestContext(request))


def folder_view(request, folder_id):
    folder = get_object_or_404(Folder, pk=folder_id)

    if not request.user.is_staff and not request.user.is_superuser and not request.user == folder.user:
        raise PermissionDenied

    return render_to_response('generic_list.html', {
        'object_list': folder.folderdocument_set.all(),
        'extra_columns': [
            {'name': _(u'document'), 'attribute':
                lambda x: '<a href="%s">%s</a>' % (reverse('document_view_simple', args=[x.document.pk]), x.document)
            },
            {'name': _(u'thumbnail'), 'attribute':
                lambda x: '<a class="fancybox" href="%s"><img src="%s" /></a>' % (reverse('document_preview', args=[x.document.pk]),
                    reverse('document_thumbnail', args=[x.document.pk]))
            },
        ],
        'hide_link': True,
        'hide_object': True,
        'title': _(u'documents in folder: %s') % folder,
        'multi_select_as_buttons': True,
        'object': folder,
        'object_name': _(u'folder'),
    }, context_instance=RequestContext(request))


def folder_add_document(request, document_id):
    check_permissions(request.user, 'documents', [PERMISSION_DOCUMENT_VIEW])
    document = get_object_or_404(Document, pk=document_id)

    if request.method == 'POST':
        previous = request.META.get('HTTP_REFERER', '/')
        form = AddDocumentForm(request.POST, user=request.user)
        if form.is_valid():
            if form.cleaned_data['existing_folder']:
                folder = form.cleaned_data['existing_folder']
            elif form.cleaned_data['title']:
                folder, created = Folder.objects.get_or_create(user=request.user, title=form.cleaned_data['title'])
                if created:
                    messages.success(request, _(u'Folder created successfully'))
                else:
                    messages.error(request, _(u'A folder named: %s, already exists.') % form.cleaned_data['title'])
                    return HttpResponseRedirect(previous)
            else:
                messages.error(request, _(u'Must specify a new folder or an existing one.'))
                return HttpResponseRedirect(previous)

            folder_document, created = FolderDocument.objects.get_or_create(folder=folder, document=document)
            if created:
                messages.success(request, _(u'Document: %(document)s added to folder: %(folder)s successfully.') % {
                    'document': document, 'folder': folder})
            else:
                messages.warning(request, _(u'Document: %(document)s is already in folder: %(folder)s.') % {
                    'document': document, 'folder': folder})

    return HttpResponseRedirect(previous)


def folder_document_remove(request, folder_document_id=None, folder_document_id_list=None):
    post_action_redirect = None

    if folder_document_id:
        folder_documents = [get_object_or_404(FolderDocument, pk=folder_document_id)]
    elif folder_document_id_list:
        folder_documents = [get_object_or_404(FolderDocument, pk=folder_document_id) for folder_document_id in folder_document_id_list.split(',')]
    else:
        messages.error(request, _(u'Must provide at least one folder document.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', '/')))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', '/')))

    if request.method == 'POST':
        for folder_document in folder_documents:
            try:
                folder_document.delete()
                messages.success(request, _(u'Document: %s removed successfully.') % folder_document)
            except Exception, e:
                messages.error(request, _(u'Document: %(document)s delete error: %(error)s') % {
                    'document': folder_document, 'error': e})

        return HttpResponseRedirect(next)

    context = {
        'object_name': _(u'folder document'),
        'previous': previous,
        'next': next,
    }
    if len(folder_documents) == 1:
        context['object'] = folder_documents[0]
        context['title'] = _(u'Are you sure you wish to remove the document: %s?') % ', '.join([unicode(d) for d in folder_documents])
    elif len(folder_documents) > 1:
        context['title'] = _(u'Are you sure you wish to remove the documents: %s?') % ', '.join([unicode(d) for d in folder_documents])

    return render_to_response('generic_confirm.html', context,
        context_instance=RequestContext(request))


def folder_document_multiple_remove(request):
    return folder_document_remove(request, folder_document_id_list=request.GET.get('id_list', []))
