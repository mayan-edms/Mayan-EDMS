from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.http import urlencode
from django.utils.translation import ugettext_lazy as _, ungettext

from acls.models import AccessEntry
from documents.models import Document, DocumentType
from documents.permissions import (
    PERMISSION_DOCUMENT_TYPE_EDIT, PERMISSION_DOCUMENT_VIEW
)
from documents.views import document_list
from permissions.models import Permission

from common.utils import encapsulate, generate_choices_w_labels
from common.views import assign_remove

from .api import save_metadata_list
from .forms import (
    AddMetadataForm, MetadataFormSet, MetadataRemoveFormSet, MetadataTypeForm
)
from .models import DocumentMetadata, MetadataType
from .permissions import (
    PERMISSION_METADATA_DOCUMENT_ADD, PERMISSION_METADATA_DOCUMENT_EDIT,
    PERMISSION_METADATA_DOCUMENT_REMOVE, PERMISSION_METADATA_DOCUMENT_VIEW,
    PERMISSION_METADATA_TYPE_CREATE, PERMISSION_METADATA_TYPE_DELETE,
    PERMISSION_METADATA_TYPE_EDIT, PERMISSION_METADATA_TYPE_VIEW
)


def metadata_edit(request, document_id=None, document_id_list=None):
    if document_id:
        document_id_list = unicode(document_id)

    documents = Document.objects.select_related('metadata').filter(pk__in=document_id_list.split(','))

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_METADATA_DOCUMENT_EDIT])
    except PermissionDenied:
        documents = AccessEntry.objects.filter_objects_by_access(PERMISSION_METADATA_DOCUMENT_EDIT, request.user, documents)

    if not documents:
        if document_id:
            raise Http404
        else:
            messages.error(request, _('Must provide at least one document.'))
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('main:home')))

    if len(set([document.document_type.pk for document in documents])) > 1:
        messages.error(request, _('Only select documents of the same type.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('main:home')))

    if set(documents.values_list('metadata__value', flat=True)) == set([None]):
        message = ungettext(
            'The selected document doesn\'t have any metadata.',
            'The selected documents don\'t have any metadata.',
            len(documents)
        )
        messages.warning(request, message)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('main:home')))

    post_action_redirect = reverse('documents:document_list_recent')

    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', post_action_redirect)))

    metadata = {}
    initial = []

    for document in documents:
        document.add_as_recent_document_for_user(request.user)

        for item in document.metadata.all():
            value = item.value
            if item.metadata_type in metadata:
                if value not in metadata[item.metadata_type]:
                    metadata[item.metadata_type].append(value)
            else:
                metadata[item.metadata_type] = [value] if value else []

    for key, value in metadata.items():
        initial.append({
            'metadata_type': key,
            'value': ', '.join(value) if value else '',
            'required': key in document.document_type.metadata.filter(required=True),
        })

    formset = MetadataFormSet(initial=initial)
    if request.method == 'POST':
        formset = MetadataFormSet(data=request.POST, initial=initial)
        if formset.is_valid():
            for document in documents:

                errors = []
                for form in formset.forms:
                    if form.cleaned_data['update']:
                        try:
                            save_metadata_list([form.cleaned_data], document)
                        except Exception as exception:
                            errors.append(exception)

                if errors:
                    for error in errors:
                        if settings.DEBUG:
                            raise
                        else:
                            messages.error(request, _('Error editing metadata for document %(document)s; %(exception)s.') % {
                                'document': document, 'exception': ', '.join(exception.messages)})
                else:
                    messages.success(request, _('Metadata for document %s edited successfully.') % document)

            return HttpResponseRedirect(next)

    context = {
        'form_display_mode_table': True,
        'form': formset,
        'next': next,
    }

    if len(documents) == 1:
        context['object'] = documents[0]

    context['title'] = ungettext(
        'Edit document metadata',
        'Edit documents metadata',
        len(documents)
    )

    return render_to_response('main/generic_form.html', context,
                              context_instance=RequestContext(request))


def metadata_multiple_edit(request):
    return metadata_edit(request, document_id_list=request.GET.get('id_list', ''))


def metadata_add(request, document_id=None, document_id_list=None):
    if document_id:
        documents = [get_object_or_404(Document, pk=document_id)]
    elif document_id_list:
        documents = [get_object_or_404(Document.objects.select_related('document_type'), pk=document_id) for document_id in document_id_list.split(',')]
        if len(set([document.document_type.pk for document in documents])) > 1:
            messages.error(request, _('Only select documents of the same type.'))
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('main:home')))

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_METADATA_DOCUMENT_ADD])
    except PermissionDenied:
        documents = AccessEntry.objects.filter_objects_by_access(PERMISSION_METADATA_DOCUMENT_ADD, request.user, documents)

    if not documents:
        messages.error(request, _('Must provide at least one document.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('main:home')))

    for document in documents:
        document.add_as_recent_document_for_user(request.user)

    post_action_redirect = reverse('documents:document_list_recent')

    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', post_action_redirect)))

    if request.method == 'POST':
        form = AddMetadataForm(data=request.POST, document_type=document.document_type)
        if form.is_valid():
            metadata_type = form.cleaned_data['metadata_type']
            for document in documents:
                try:
                    document_metadata, created = DocumentMetadata.objects.get_or_create(document=document, metadata_type=metadata_type.metadata_type, defaults={'value': ''})
                except Exception as exception:
                    if getattr(settings, 'DEBUG', False):
                        raise
                    else:
                        messages.error(request, _('Error adding metadata type "%(metadata_type)s" to document: %(document)s; %(exception)s') % {
                            'metadata_type': metadata_type, 'document': document, 'exception': ', '.join(getattr(exception, 'messages', exception))})
                else:
                    if created:
                        messages.success(request, _('Metadata type: %(metadata_type)s successfully added to document %(document)s.') % {
                            'metadata_type': metadata_type, 'document': document})
                    else:
                        messages.warning(request, _('Metadata type: %(metadata_type)s already present in document %(document)s.') % {
                            'metadata_type': metadata_type, 'document': document})

            if len(documents) == 1:
                return HttpResponseRedirect('%s?%s' % (
                    reverse('metadata:metadata_edit', args=[document.pk]),
                    urlencode({'next': next}))
                )
            elif len(documents) > 1:
                return HttpResponseRedirect('%s?%s' % (
                    reverse('metadata:metadata_multiple_edit'),
                    urlencode({'id_list': document_id_list, 'next': next}))
                )

    else:
        form = AddMetadataForm(document_type=document.document_type)

    context = {
        'form': form,
        'next': next,
    }

    if len(documents) == 1:
        context['object'] = documents[0]

    context['title'] = ungettext(
        'Add metadata types to document',
        'Add metadata types to documents',
        len(documents)
    )

    return render_to_response('main/generic_form.html', context,
                              context_instance=RequestContext(request))


def metadata_multiple_add(request):
    return metadata_add(request, document_id_list=request.GET.get('id_list', []))


def metadata_remove(request, document_id=None, document_id_list=None):
    if document_id:
        document_id_list = unicode(document_id)

    documents = Document.objects.select_related('metadata').filter(pk__in=document_id_list.split(','))

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_METADATA_DOCUMENT_REMOVE])
    except PermissionDenied:
        documents = AccessEntry.objects.filter_objects_by_access(PERMISSION_METADATA_DOCUMENT_REMOVE, request.user, documents)

    if not documents:
        if document_id:
            raise Http404
        else:
            messages.error(request, _('Must provide at least one document.'))
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('main:home')))

    if len(set([document.document_type.pk for document in documents])) > 1:
        messages.error(request, _('Only select documents of the same type.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('main:home')))

    if set(documents.values_list('metadata__value', flat=True)) == set([None]):
        message = ungettext(
            'The selected document doesn\'t have any metadata.',
            'The selected documents doesn\'t have any metadata.',
            len(documents)
        )
        messages.warning(request, message)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('main:home')))

    post_action_redirect = reverse('documents:document_list_recent')

    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', post_action_redirect)))

    metadata = {}
    for document in documents:
        document.add_as_recent_document_for_user(request.user)

        for item in document.metadata.all():
            value = item.value
            if item.metadata_type in metadata:
                if value not in metadata[item.metadata_type]:
                    metadata[item.metadata_type].append(value)
            else:
                metadata[item.metadata_type] = [value] if value else ''

    initial = []
    for key, value in metadata.items():
        initial.append({
            'metadata_type': key,
            'value': ', '.join(value)
        })

    formset = MetadataRemoveFormSet(initial=initial)
    if request.method == 'POST':
        formset = MetadataRemoveFormSet(request.POST)
        if formset.is_valid():
            for document in documents:

                for form in formset.forms:
                    if form.cleaned_data['update']:
                        metadata_type = get_object_or_404(MetadataType, pk=form.cleaned_data['id'])
                        try:
                            document_metadata = DocumentMetadata.objects.get(document=document, metadata_type=metadata_type)
                            document_metadata.delete()
                            messages.success(request, _('Successfully remove metadata type "%(metadata_type)s" from document: %(document)s.') % {
                                'metadata_type': metadata_type, 'document': document})
                        except Exception as exception:
                            messages.error(request, _('Error removing metadata type "%(metadata_type)s" from document: %(document)s; %(exception)s') % {
                                'metadata_type': metadata_type, 'document': document, 'exception': ', '.join(exception.messages)})

            return HttpResponseRedirect(next)

    context = {
        'form_display_mode_table': True,
        'form': formset,
        'next': next,
    }

    if len(documents) == 1:
        context['object'] = documents[0]

    context['title'] = ungettext(
        'Remove metadata types from the document',
        'Remove metadata types from the documents',
        len(documents)
    )

    return render_to_response('main/generic_form.html', context,
                              context_instance=RequestContext(request))


def metadata_multiple_remove(request):
    return metadata_remove(request, document_id_list=request.GET.get('id_list', []))


def metadata_view(request, document_id):
    document = get_object_or_404(Document, pk=document_id)

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_METADATA_DOCUMENT_VIEW])
    except PermissionDenied:
        AccessEntry.objects.check_access(PERMISSION_METADATA_DOCUMENT_VIEW, request.user, document)

    return render_to_response('main/generic_list.html', {
        'title': _('Metadata for document: %s') % document,
        'object_list': document.metadata.all(),
        'extra_columns': [
            {'name': _('Value'), 'attribute': 'value'},
            {'name': _('Required'), 'attribute': encapsulate(lambda x: x.metadata_type in document.document_type.metadata.filter(required=True))}
        ],
        'hide_link': True,
        'object': document,
    }, context_instance=RequestContext(request))


def documents_missing_required_metadata(request):
    pre_object_list = Document.objects.filter(document_type__metadata__required=True, metadata__value__isnull=True)

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_DOCUMENT_VIEW])
    except PermissionDenied:
        # If user doesn't have global permission, get a list of document
        # for which he/she does hace access use it to filter the
        # provided object_list
        object_list = AccessEntry.objects.filter_objects_by_access(
            PERMISSION_DOCUMENT_VIEW, request.user, pre_object_list)
    else:
        object_list = pre_object_list

    context = {
        'object_list': object_list,
        'title': _('Documents missing required metadata'),
        'hide_links': True,
    }

    return document_list(
        request,
        extra_context=context
    )


# Setup views
def setup_metadata_type_list(request):
    Permission.objects.check_permissions(request.user, [PERMISSION_METADATA_TYPE_VIEW])

    context = {
        'object_list': MetadataType.objects.all(),
        'title': _('Metadata types'),
        'hide_link': True,
        'extra_columns': [
            {
                'name': _('Internal name'),
                'attribute': 'name',
            },
        ]
    }

    return render_to_response('main/generic_list.html', context,
                              context_instance=RequestContext(request))


def setup_metadata_type_edit(request, metadatatype_id):
    Permission.objects.check_permissions(request.user, [PERMISSION_METADATA_TYPE_EDIT])

    metadata_type = get_object_or_404(MetadataType, pk=metadatatype_id)

    if request.method == 'POST':
        form = MetadataTypeForm(instance=metadata_type, data=request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, _('Metadata type edited successfully'))
                return HttpResponseRedirect(reverse('metadata:setup_metadata_type_list'))
            except Exception as exception:
                messages.error(request, _('Error editing metadata type; %s') % exception)
            pass
    else:
        form = MetadataTypeForm(instance=metadata_type)

    return render_to_response('main/generic_form.html', {
        'title': _('Edit metadata type: %s') % metadata_type,
        'form': form,
        'object': metadata_type,
    }, context_instance=RequestContext(request))


def setup_metadata_type_create(request):
    Permission.objects.check_permissions(request.user, [PERMISSION_METADATA_TYPE_CREATE])

    if request.method == 'POST':
        form = MetadataTypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Metadata type created successfully'))
            return HttpResponseRedirect(reverse('metadata:setup_metadata_type_list'))
    else:
        form = MetadataTypeForm()

    return render_to_response('main/generic_form.html', {
        'title': _('Create metadata type'),
        'form': form,
    }, context_instance=RequestContext(request))


def setup_metadata_type_delete(request, metadatatype_id):
    Permission.objects.check_permissions(request.user, [PERMISSION_METADATA_TYPE_DELETE])

    metadata_type = get_object_or_404(MetadataType, pk=metadatatype_id)

    post_action_redirect = reverse('metadata:setup_metadata_type_list')

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', post_action_redirect)))
    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', post_action_redirect)))

    if request.method == 'POST':
        try:
            metadata_type.delete()
            messages.success(request, _('Metadata type: %s deleted successfully.') % metadata_type)
        except Exception as exception:
            messages.error(request, _('Metadata type: %(metadata_type)s delete error: %(error)s') % {
                'metadata_type': metadata_type, 'error': exception})

        return HttpResponseRedirect(next)

    context = {
        'delete_view': True,
        'next': next,
        'previous': previous,
        'object': metadata_type,
        'title': _('Are you sure you wish to delete the metadata type: %s?') % metadata_type,
    }

    return render_to_response('main/generic_confirm.html', context,
                              context_instance=RequestContext(request))


def setup_document_type_metadata(request, document_type_id):
    Permission.objects.check_permissions(request.user, [PERMISSION_DOCUMENT_TYPE_EDIT])

    document_type = get_object_or_404(DocumentType, pk=document_type_id)

    return assign_remove(
        request,
        left_list=lambda: generate_choices_w_labels(set(MetadataType.objects.all()) - set(MetadataType.objects.filter(id__in=document_type.metadata.values_list('metadata_type', flat=True))), display_object_type=False),
        right_list=lambda: generate_choices_w_labels(document_type.metadata.filter(required=False), display_object_type=False),
        add_method=lambda x: document_type.metadata.create(metadata_type=x, required=False),
        remove_method=lambda x: x.delete(),
        extra_context={
            'document_type': document_type,
            'navigation_object_name': 'document_type',
            'main_title': _('Optional metadata types for document type: %s') % document_type,
        },
        decode_content_type=True,
    )


def setup_document_type_metadata_required(request, document_type_id):
    Permission.objects.check_permissions(request.user, [PERMISSION_DOCUMENT_TYPE_EDIT])

    document_type = get_object_or_404(DocumentType, pk=document_type_id)

    return assign_remove(
        request,
        left_list=lambda: generate_choices_w_labels(set(MetadataType.objects.all()) - set(MetadataType.objects.filter(id__in=document_type.metadata.values_list('metadata_type', flat=True))), display_object_type=False),
        right_list=lambda: generate_choices_w_labels(document_type.metadata.filter(required=True), display_object_type=False),
        add_method=lambda x: document_type.metadata.create(metadata_type=x, required=True),
        remove_method=lambda x: x.delete(),
        extra_context={
            'document_type': document_type,
            'navigation_object_name': 'document_type',
            'main_title': _('Required metadata types for document type: %s') % document_type,
        },
        decode_content_type=True,
    )
