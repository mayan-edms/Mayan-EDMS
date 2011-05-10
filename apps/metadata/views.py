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
from filesystem_serving.api import document_create_fs_links, document_delete_fs_links

from metadata import PERMISSION_METADATA_DOCUMENT_EDIT, \
    PERMISSION_METADATA_DOCUMENT_ADD, PERMISSION_METADATA_DOCUMENT_REMOVE
from metadata.forms import MetadataFormSet, AddMetadataForm, MetadataRemoveFormSet
from metadata.api import save_metadata_list
from metadata.models import DocumentMetadata, MetadataType


def metadata_edit(request, document_id=None, document_id_list=None):
    check_permissions(request.user, 'metadata', [PERMISSION_METADATA_DOCUMENT_EDIT])

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

    formset = MetadataFormSet(initial=initial)
    if request.method == 'POST':
        formset = MetadataFormSet(request.POST)
        if formset.is_valid():
            for document in documents:
                try:
                    document_delete_fs_links(document)
                except Exception, e:
                    messages.error(request, _(u'Error deleting filesystem links for document: %(document)s; %(error)s') % {
                        'document': document, 'error': e})
                
                for form in formset.forms:
                    if form.cleaned_data['update']:
                        try:
                            save_metadata_list([form.cleaned_data], document)
                            messages.success(request, _(u'Metadata for document %s edited successfully.') % document)
                        except Exception, e:
                            messages.error(request, _(u'Error editing metadata for document %(document)s; %(error)s.') % {
                                'document': document, 'error': e})

                try:
                    warnings = document_create_fs_links(document)

                    if request.user.is_staff or request.user.is_superuser:
                        for warning in warnings:
                            messages.warning(request, warning)

                    messages.success(request, _(u'Filesystem links updated successfully for document: %s.') % document)
                except Exception, e:
                    messages.error(request, _('Error creating filesystem links for document: %(document)s; %(error)s') % {
                        'document': document, 'error': e})

            if len(documents) == 1:
                return HttpResponseRedirect(document.get_absolute_url())
            elif len(documents) > 1:
                return HttpResponseRedirect(reverse('document_list_recent'))

    context = {
        'form_display_mode_table': True,
        'form': formset,
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
    check_permissions(request.user, 'metadata', [PERMISSION_METADATA_DOCUMENT_ADD])

    if document_id:
        documents = [get_object_or_404(Document, pk=document_id)]
    elif document_id_list:
        documents = [get_object_or_404(Document, pk=document_id) for document_id in document_id_list.split(',')]
    else:
        messages.error(request, _(u'Must provide at least one document.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    metadata = {}
    for document in documents:
        RecentDocument.objects.add_document_for_user(request.user, document)

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
                return HttpResponseRedirect(reverse(metadata_edit, args=[document.pk]))
            elif len(documents) > 1:
                return HttpResponseRedirect(u'%s?%s' % (reverse('metadata_multiple_edit'), urlencode({'id_list': document_id_list})))

    else:
        form = AddMetadataForm()
        
    context = {
        #'form_display_mode_table': True,
        'form': form,
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


def metadata_remove(request, document_id):
    check_permissions(request.user, 'metadata', [PERMISSION_METADATA_DOCUMENT_REMOVE])

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
                try:
                    document_delete_fs_links(document)
                except Exception, e:
                    messages.error(request, _(u'Error deleting filesystem links for document: %(document)s; %(error)s') % {
                        'document': document, 'error': e})
                
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

                try:
                    warnings = document_create_fs_links(document)

                    if request.user.is_staff or request.user.is_superuser:
                        for warning in warnings:
                            messages.warning(request, warning)

                    messages.success(request, _(u'Filesystem links updated successfully for document: %s.') % document)
                except Exception, e:
                    messages.error(request, _('Error creating filesystem links for document: %(document)s; %(error)s') % {
                        'document': document, 'error': e})

            if len(documents) == 1:
                return HttpResponseRedirect(document.get_absolute_url())
            elif len(documents) > 1:
                return HttpResponseRedirect(reverse('document_list_recent'))
        
    context = {
        'form_display_mode_table': True,
        'form': formset,
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
