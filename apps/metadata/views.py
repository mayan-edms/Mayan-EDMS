from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.http import urlencode

from documents.literals import PERMISSION_DOCUMENT_TYPE_EDIT
from documents.models import Document, RecentDocument, DocumentType
from permissions.api import check_permissions
from document_indexing.api import update_indexes, delete_indexes

from common.utils import generate_choices_w_labels#, two_state_template
from common.views import assign_remove

from metadata import PERMISSION_METADATA_DOCUMENT_VIEW, \
    PERMISSION_METADATA_DOCUMENT_EDIT, \
    PERMISSION_METADATA_DOCUMENT_ADD, PERMISSION_METADATA_DOCUMENT_REMOVE, \
    PERMISSION_METADATA_TYPE_EDIT, PERMISSION_METADATA_TYPE_CREATE, \
    PERMISSION_METADATA_TYPE_DELETE, PERMISSION_METADATA_TYPE_VIEW, \
    PERMISSION_METADATA_SET_EDIT, PERMISSION_METADATA_SET_CREATE, \
    PERMISSION_METADATA_SET_DELETE, PERMISSION_METADATA_SET_VIEW
from metadata.forms import MetadataFormSet, AddMetadataForm, \
    MetadataRemoveFormSet, MetadataTypeForm, MetadataSetForm
from metadata.api import save_metadata_list
from metadata.models import DocumentMetadata, MetadataType, MetadataSet, \
    MetadataSetItem, DocumentTypeDefaults


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
        context['title'] = _(u'Remove metadata types from document: %s') % ', '.join([unicode(d) for d in documents])
    elif len(documents) > 1:
        context['title'] = _(u'Remove metadata types from documents: %s') % ', '.join([unicode(d) for d in documents])

    return render_to_response('generic_form.html', context,
        context_instance=RequestContext(request))


def metadata_multiple_remove(request):
    return metadata_remove(request, document_id_list=request.GET.get('id_list', []))


def metadata_view(request, document_id):
    check_permissions(request.user, [PERMISSION_METADATA_DOCUMENT_VIEW])    
    document = get_object_or_404(Document, pk=document_id)

    return render_to_response('generic_list.html', {
        'title': _(u'metadata for: %s') % document,
        'object_list': document.documentmetadata_set.all(),
        'extra_columns': [{'name': _(u'value'), 'attribute': 'value'}],
        'hide_link': True,
        'object': document,
    }, context_instance=RequestContext(request))
            

def setup_metadata_type_list(request):
    check_permissions(request.user, [PERMISSION_METADATA_TYPE_VIEW])

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
    check_permissions(request.user, [PERMISSION_METADATA_TYPE_EDIT])
    
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
    check_permissions(request.user, [PERMISSION_METADATA_TYPE_CREATE])
    
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
    check_permissions(request.user, [PERMISSION_METADATA_TYPE_DELETE])
    
    metadata_type = get_object_or_404(MetadataType, pk=metadatatype_id)

    post_action_redirect = reverse('setup_metadata_type_list')

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', post_action_redirect)))
    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', post_action_redirect)))

    if request.method == 'POST':
        try:
            metadata_type.delete()
            messages.success(request, _(u'Metadata type: %s deleted successfully.') % metadata_type)
        except Exception, e:
            messages.error(request, _(u'Metadata type: %(metadata_type)s delete error: %(error)s') % {
                'metadata_type': metadata_type, 'error': e})

        return HttpResponseRedirect(next)

    context = {
        'object_name': _(u'metadata type'),
        'delete_view': True,
        'next': next,
        'previous': previous,
        'object': metadata_type,
        'title': _(u'Are you sure you wish to delete the metadata type: %s?') % metadata_type,
        'form_icon': u'xhtml_delete.png',
    }

    return render_to_response('generic_confirm.html', context,
        context_instance=RequestContext(request))


def setup_metadata_set_list(request):
    check_permissions(request.user, [PERMISSION_METADATA_SET_VIEW])

    context = {
        'object_list': MetadataSet.objects.all(),
        'title': _(u'metadata sets'),
        'hide_link': True,
        'extra_columns': [
            {
                'name': _(u'members'),
                'attribute': lambda x: x.metadatasetitem_set.count(),
            },
        ]
    }

    return render_to_response('generic_list.html', context,
        context_instance=RequestContext(request))    


def get_set_members(metadata_set):
    return [item.metadata_type for item in metadata_set.metadatasetitem_set.all()]


def get_non_set_members(metadata_set):
    return MetadataType.objects.exclude(pk__in=[member.pk for member in get_set_members(metadata_set)])


def add_set_member(metadata_set, selection):
    model, pk = selection.split(u',')
    metadata_type = get_object_or_404(MetadataType, pk=pk)
    new_member, created = MetadataSetItem.objects.get_or_create(metadata_set=metadata_set, metadata_type=metadata_type)
    if not created:
        raise Exception


def remove_set_member(metadata_set, selection):
    model, pk = selection.split(u',')
    metadata_type = get_object_or_404(MetadataType, pk=pk)
    member = MetadataSetItem.objects.get(metadata_type=metadata_type, metadata_set=metadata_set)
    member.delete()


def setup_metadata_set_edit(request, metadata_set_id):
    check_permissions(request.user, [PERMISSION_METADATA_SET_EDIT])

    metadata_set = get_object_or_404(MetadataSet, pk=metadata_set_id)

    return assign_remove(
        request,
        left_list=lambda: generate_choices_w_labels(get_non_set_members(metadata_set)),
        right_list=lambda: generate_choices_w_labels(get_set_members(metadata_set)),
        add_method=lambda x: add_set_member(metadata_set, x),
        remove_method=lambda x: remove_set_member(metadata_set, x),
        left_list_title=_(u'non members of metadata set: %s') % metadata_set,
        right_list_title=_(u'members of metadata set: %s') % metadata_set,
        extra_context={
            'object': metadata_set,
            'object_name': _(u'metadata set'),
        }
    )


def setup_metadata_set_create(request):
    check_permissions(request.user, [PERMISSION_METADATA_SET_CREATE])
    
    if request.method == 'POST':
        form = MetadataSetForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _(u'Metadata set created successfully'))
            return HttpResponseRedirect(reverse('setup_metadata_set_list'))
    else:
        form = MetadataSetForm()

    return render_to_response('generic_form.html', {
        'title': _(u'create metadata set'),
        'form': form,
    },
    context_instance=RequestContext(request))


def setup_metadata_set_delete(request, metadata_set_id):
    check_permissions(request.user, [PERMISSION_METADATA_SET_DELETE])
    
    metadata_set = get_object_or_404(MetadataSet, pk=metadata_set_id)

    post_action_redirect = reverse('setup_metadata_set_list')

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', post_action_redirect)))
    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', post_action_redirect)))

    if request.method == 'POST':
        try:
            metadata_set.delete()
            messages.success(request, _(u'Metadata set: %s deleted successfully.') % metadata_set)
        except Exception, e:
            messages.error(request, _(u'Metadata set: %(metadata_set)s delete error: %(error)s') % {
                'metadata_set': metadata_set, 'error': e})

        return HttpResponseRedirect(next)

    context = {
        'object_name': _(u'metadata set'),
        'delete_view': True,
        'next': next,
        'previous': previous,
        'object': metadata_set,
        'title': _(u'Are you sure you wish to delete the metadata set: %s?') % metadata_set,
        'form_icon': u'application_form_delete.png',
    }

    return render_to_response('generic_confirm.html', context,
        context_instance=RequestContext(request))


def get_document_type_metadata_members(document_type):
    metadata_types = set(document_type.documenttypedefaults_set.get().default_metadata.all())
    metadata_sets = set(document_type.documenttypedefaults_set.get().default_metadata_sets.all())
    return list(metadata_types | metadata_sets)


def get_document_type_metadata_non_members(document_type):
    members = set(get_document_type_metadata_members(document_type))
    all_metadata_objects = set(MetadataType.objects.all()) | set(MetadataSet.objects.all())
    return list(all_metadata_objects - members)


def add_document_type_metadata(document_type, selection):
    model, pk = selection.split(u',')
    if model == 'metadata type':
        metadata_type = get_object_or_404(MetadataType, pk=pk)
        document_type.documenttypedefaults_set.get().default_metadata.add(metadata_type)
    elif model == 'metadata set':
        metadata_set = get_object_or_404(MetadataSet, pk=pk)
        document_type.documenttypedefaults_set.get().default_metadata_sets.add(metadata_set)
    else:
        raise Exception


def remove_document_type_metadata(document_type, selection):
    model, pk = selection.split(u',')
    if model == 'metadata type':
        metadata_type = get_object_or_404(MetadataType, pk=pk)
        document_type.documenttypedefaults_set.get().default_metadata.remove(metadata_type)
    elif model == 'metadata set':
        metadata_set = get_object_or_404(MetadataSet, pk=pk)
        document_type.documenttypedefaults_set.get().default_metadata_sets.remove(metadata_set)
    else:
        raise Exception


def setup_document_type_metadata(request, document_type_id):
    check_permissions(request.user, [PERMISSION_DOCUMENT_TYPE_EDIT])

    document_type = get_object_or_404(DocumentType, pk=document_type_id)

    # Initialize defaults
    DocumentTypeDefaults.objects.get_or_create(document_type=document_type)
    
    return assign_remove(
        request,
        left_list=lambda: generate_choices_w_labels(get_document_type_metadata_non_members(document_type)),
        right_list=lambda: generate_choices_w_labels(get_document_type_metadata_members(document_type)),
        add_method=lambda x: add_document_type_metadata(document_type, x),
        remove_method=lambda x: remove_document_type_metadata(document_type, x),
        left_list_title=_(u'non members of document type: %s') % document_type,
        right_list_title=_(u'members of document type: %s') % document_type,
        extra_context={
            'document_type': document_type,
            'navigation_object_name': 'document_type',
            'object_name': _(u'document type'),
        },
    )
