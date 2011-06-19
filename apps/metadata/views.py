from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.http import urlencode

from documents.models import Document, RecentDocument
from permissions.api import check_permissions
from document_indexing.api import update_indexes, delete_indexes

from metadata import PERMISSION_METADATA_DOCUMENT_EDIT, \
    PERMISSION_METADATA_DOCUMENT_ADD, PERMISSION_METADATA_DOCUMENT_REMOVE
from metadata.forms import MetadataFormSet, AddMetadataForm, \
    MetadataRemoveFormSet, MetadataTypeForm
from metadata.api import save_metadata_list
from metadata.models import DocumentMetadata, MetadataType


def metadata_edit(request, document_id=None, document_id_list=None):
    check_permissions(request.user, [PERMISSION_METADATA_DOCUMENT_EDIT])

    if document_id:
        documents = [get_object_or_404(Document, pk=document_id)]
        if documents[0].documentmetadata_set.count() == 0:
            messages.warning(request, _(u'The selected document doesn\'t have any metadata.'))
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    elif document_id_list:
        documents = [get_object_or_404(Document, pk=document_id) for document_id in document_id_list.split(',')]
    else:
        messages.error(request, _(u'Must provide at least one document.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    post_action_redirect = reverse('document_list_recent')

    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', post_action_redirect)))

    metadata = {}
    for document in documents:
        RecentDocument.objects.add_document_for_user(request.user, document)

        for item in document.documentmetadata_set.all():
            value = item.value
            if item.metadata_type in metadata:
                if value not in metadata[item.metadata_type]:
                    metadata[item.metadata_type].append(value)
            else:
                metadata[item.metadata_type] = [value] if value else []

    initial = []
    for key, value in metadata.items():
        initial.append({
            'metadata_type': key,
            'value': u', '.join(value)
        })

    formset = MetadataFormSet(initial=initial)
    if request.method == 'POST':
        formset = MetadataFormSet(request.POST)
        if formset.is_valid():
            for document in documents:

                warnings = delete_indexes(document)
                if request.user.is_staff or request.user.is_superuser:
                    for warning in warnings:
                        messages.warning(request, _(u'Error deleting document indexes; %s') % warning)

                errors = []
                for form in formset.forms:
                    if form.cleaned_data['update']:
                        try:
                            save_metadata_list([form.cleaned_data], document)
                        except Exception, e:
                            errors.append(e)

                if errors:
                    for error in errors:
                        messages.error(request, _(u'Error editing metadata for document %(document)s; %(error)s.') % {
                        'document': document, 'error': error})
                else:
                    messages.success(request, _(u'Metadata for document %s edited successfully.') % document)

                warnings = update_indexes(document)
                if warnings and (request.user.is_staff or request.user.is_superuser):
                    for warning in warnings:
                        messages.warning(request, _(u'Error updating document indexes; %s') % warning)
                else:
                    messages.success(request, _(u'Document indexes updated successfully.'))

            return HttpResponseRedirect(next)

    context = {
        'form_display_mode_table': True,
        'form': formset,
        'next': next,
    }
    if len(documents) == 1:
        context['object'] = documents[0]
        context['title'] = _(u'Edit metadata for document: %s') % ', '.join([unicode(d) for d in documents])
    elif len(documents) > 1:
        context['title'] = _(u'Edit metadata for documents: %s') % ', '.join([unicode(d) for d in documents])

    return render_to_response('generic_form.html', context,
        context_instance=RequestContext(request))


def metadata_multiple_edit(request):
    return metadata_edit(request, document_id_list=request.GET.get('id_list', []))


def metadata_add(request, document_id=None, document_id_list=None):
    check_permissions(request.user, [PERMISSION_METADATA_DOCUMENT_ADD])

    if document_id:
        documents = [get_object_or_404(Document, pk=document_id)]
    elif document_id_list:
        documents = [get_object_or_404(Document, pk=document_id) for document_id in document_id_list.split(',')]
    else:
        messages.error(request, _(u'Must provide at least one document.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    for document in documents:
        RecentDocument.objects.add_document_for_user(request.user, document)

    post_action_redirect = reverse('document_list_recent')

    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', post_action_redirect)))

    if request.method == 'POST':
        form = AddMetadataForm(request.POST)
        if form.is_valid():
            metadata_type = form.cleaned_data['metadata_type']
            for document in documents:
                document_metadata, created = DocumentMetadata.objects.get_or_create(document=document, metadata_type=metadata_type, defaults={'value': u''})
                if created:
                    messages.success(request, _(u'Metadata type: %(metadata_type)s successfully added to document %(document)s.') % {
                        'metadata_type': metadata_type, 'document': document})
                else:
                    messages.warning(request, _(u'Metadata type: %(metadata_type)s already present in document %(document)s.') % {
                        'metadata_type': metadata_type, 'document': document})

            if len(documents) == 1:
                return HttpResponseRedirect(u'%s?%s' % (
                    reverse(metadata_edit, args=[document.pk]),
                    urlencode({'next': next}))
                )
            elif len(documents) > 1:
                return HttpResponseRedirect(u'%s?%s' % (
                    reverse('metadata_multiple_edit'),
                    urlencode({'id_list': document_id_list, 'next': next}))
                )

    else:
        form = AddMetadataForm()

    context = {
        #'form_display_mode_table': True,
        'form': form,
        'next': next,
    }
    if len(documents) == 1:
        context['object'] = documents[0]
        context['title'] = _(u'Add metadata type to document: %s') % ', '.join([unicode(d) for d in documents])
    elif len(documents) > 1:
        context['title'] = _(u'Add metadata type to documents: %s') % ', '.join([unicode(d) for d in documents])

    return render_to_response('generic_form.html', context,
        context_instance=RequestContext(request))


def metadata_multiple_add(request):
    return metadata_add(request, document_id_list=request.GET.get('id_list', []))


def metadata_remove(request, document_id=None, document_id_list=None):
    check_permissions(request.user, [PERMISSION_METADATA_DOCUMENT_REMOVE])

    if document_id:
        documents = [get_object_or_404(Document, pk=document_id)]
        if documents[0].documentmetadata_set.count() == 0:
            messages.warning(request, _(u'The selected document doesn\'t have any metadata.'))
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    elif document_id_list:
        documents = [get_object_or_404(Document, pk=document_id) for document_id in document_id_list.split(',')]
    else:
        messages.error(request, _(u'Must provide at least one document.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    post_action_redirect = reverse('document_list_recent')

    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', post_action_redirect)))

    metadata = {}
    for document in documents:
        RecentDocument.objects.add_document_for_user(request.user, document)

        for item in document.documentmetadata_set.all():
            value = item.value
            if item.metadata_type in metadata:
                if value not in metadata[item.metadata_type]:
                    metadata[item.metadata_type].append(value)
            else:
                metadata[item.metadata_type] = [value] if value else u''

    initial = []
    for key, value in metadata.items():
        initial.append({
            'metadata_type': key,
            'value': u', '.join(value)
        })

    formset = MetadataRemoveFormSet(initial=initial)
    if request.method == 'POST':
        formset = MetadataRemoveFormSet(request.POST)
        if formset.is_valid():
            for document in documents:

                warnings = delete_indexes(document)
                if request.user.is_staff or request.user.is_superuser:
                    for warning in warnings:
                        messages.warning(request, _(u'Error deleting document indexes; %s') % warning)

                for form in formset.forms:
                    if form.cleaned_data['update']:
                        metadata_type = get_object_or_404(MetadataType, pk=form.cleaned_data['id'])
                        try:
                            document_metadata = DocumentMetadata.objects.get(document=document, metadata_type=metadata_type)
                            document_metadata.delete()
                            messages.success(request, _(u'Successfully remove metadata type: %(metadata_type)s from document: %(document)s.') % {
                                'metadata_type': metadata_type, 'document': document})
                        except:
                            messages.error(request, _(u'Error removing metadata type: %(metadata_type)s from document: %(document)s.') % {
                                'metadata_type': metadata_type, 'document': document})

                warnings = update_indexes(document)
                if warnings and (request.user.is_staff or request.user.is_superuser):
                    for warning in warnings:
                        messages.warning(request, _(u'Error updating document indexes; %s') % warning)
                else:
                    messages.success(request, _(u'Document indexes updated successfully.'))

            return HttpResponseRedirect(next)

    context = {
        'form_display_mode_table': True,
        'form': formset,
        'next': next,
    }
    if len(documents) == 1:
        context['object'] = documents[0]
        context['title'] = _(u'Remove metadata types to document: %s') % ', '.join([unicode(d) for d in documents])
    elif len(documents) > 1:
        context['title'] = _(u'Remove metadata types to documents: %s') % ', '.join([unicode(d) for d in documents])

    return render_to_response('generic_form.html', context,
        context_instance=RequestContext(request))


def metadata_multiple_remove(request):
    return metadata_remove(request, document_id_list=request.GET.get('id_list', []))


def setup_metadata_type_list(request):
    #check_permissions(request.user, [PERMISSION_DOCUMENT_VIEW])

    context = {
        'object_list': MetadataType.objects.all(),
        'title': _(u'metadata types'),
        'hide_link': True,
        'extra_columns': [
            {
                'name': _(u'internal name'),
                'attribute': 'name',
            },
        ]
    }

    return render_to_response('generic_list.html', context,
        context_instance=RequestContext(request))    


def setup_metadata_type_edit(request, metadatatype_id):
    #check_permissions(request.user, [PERMISSION_DOCUMENT_VIEW])
    metadata_type = get_object_or_404(MetadataType, pk=metadatatype_id)

    if request.method == 'POST':
        form = MetadataTypeForm(instance=metadata_type, data=request.POST)
        if form.is_valid():
            #folder.title = form.cleaned_data['title']
            try:
                form.save()
                messages.success(request, _(u'Metadata type edited successfully'))
                return HttpResponseRedirect(reverse('setup_metadata_type_list'))
            except Exception, e:
                messages.error(request, _(u'Error editing metadata type; %s') % e)
            pass
    else:
        form = MetadataTypeForm(instance=metadata_type)

    return render_to_response('generic_form.html', {
        'title': _(u'edit metadata type: %s') % metadata_type,
        'form': form,
        'object': metadata_type,
        'object_name': _(u'metadata type'),
    },
    context_instance=RequestContext(request))    
        
        
def setup_metadata_type_create(request):
    if request.method == 'POST':
        form = MetadataTypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _(u'Metadata type created successfully'))
            return HttpResponseRedirect(reverse('setup_metadata_type_list'))
    else:
        form = MetadataTypeForm()

    return render_to_response('generic_form.html', {
        'title': _(u'create metadata type'),
        'form': form,
    },
    context_instance=RequestContext(request))


def setup_metadata_type_delete(request, metadatatype_id):
    metadata_type = get_object_or_404(MetadataType, pk=metadatatype_id)

    post_action_redirect = reverse('setup_metadata_type_list')

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', post_action_redirect)))
    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', post_action_redirect)))

    if request.method == 'POST':
        try:
            metadata_type.delete()
            messages.success(request, _(u'Metadata type: %s deleted successfully.') % metadata_type)
        except Exception, e:
            messages.error(request, _(u'Folder: %(metadata_type)s delete error: %(error)s') % {
                'metadata_type': metadata_type, 'error': e})

        return HttpResponseRedirect(next)

    context = {
        'object_name': _(u'metadata type'),
        'delete_view': True,
        'next': next,
        'previous': previous,
        'object': metadata_type,
        'title': _(u'Are you sure you with to delete the metadata type: %s?') % metadata_type,
        'form_icon': u'xhtml_delete.png',
    }

    return render_to_response('generic_confirm.html', context,
        context_instance=RequestContext(request))
