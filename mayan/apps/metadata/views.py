from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import PermissionDenied, ValidationError
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.http import urlencode
from django.utils.translation import ugettext_lazy as _, ungettext

from acls.models import AccessControlList
from common.generics import (
    AssignRemoveView, SingleObjectCreateView, SingleObjectDeleteView,
    SingleObjectEditView, SingleObjectListView
)
from documents.models import Document, DocumentType
from documents.permissions import (
    permission_document_type_edit
)

from .api import save_metadata_list
from .forms import (
    AddMetadataForm, MetadataFormSet, MetadataRemoveFormSet, MetadataTypeForm
)
from .models import DocumentMetadata, MetadataType
from .permissions import (
    permission_metadata_document_add, permission_metadata_document_edit,
    permission_metadata_document_remove, permission_metadata_document_view,
    permission_metadata_type_create, permission_metadata_type_delete,
    permission_metadata_type_edit, permission_metadata_type_view
)


def metadata_edit(request, document_id=None, document_id_list=None):
    if document_id:
        documents = Document.objects.filter(pk=document_id)
        if not documents:
            raise Document.DoesNotExist
    elif document_id_list:
        documents = Document.objects.filter(pk__in=document_id_list)

    documents = AccessControlList.objects.filter_by_access(
        permission_metadata_document_edit, request.user, queryset=documents
    )

    if not documents:
        if document_id:
            raise PermissionDenied
        else:
            messages.error(request, _('Must provide at least one document.'))
            return HttpResponseRedirect(
                request.META.get(
                    'HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL)
                )
            )

    if len(set([document.document_type.pk for document in documents])) > 1:
        messages.error(request, _('Only select documents of the same type.'))
        return HttpResponseRedirect(
            request.META.get(
                'HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL)
            )
        )

    if set(documents.values_list('metadata__metadata_type', flat=True)) == set([None]):
        message = ungettext(
            'The selected document doesn\'t have any metadata.',
            'The selected documents don\'t have any metadata.',
            len(documents)
        )
        messages.warning(request, message)
        return HttpResponseRedirect(
            request.META.get(
                'HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL)
            )
        )

    post_action_redirect = reverse('documents:document_list_recent')

    next = request.POST.get(
        'next', request.GET.get(
            'next', request.META.get('HTTP_REFERER', post_action_redirect)
        )
    )

    metadata_dict = {}
    initial = []

    for document in documents:
        document.add_as_recent_document_for_user(request.user)

        for document_metadata in document.metadata.all():
            metadata_dict.setdefault(document_metadata.metadata_type, set())

            if document_metadata.value:
                metadata_dict[
                    document_metadata.metadata_type
                ].add(document_metadata.value)

    for key, value in metadata_dict.items():
        initial.append({
            'document_type': document.document_type,
            'metadata_type': key,
            'value': ', '.join(value) if value else '',
        })

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

                for error in errors:
                    if settings.DEBUG:
                        raise
                    else:
                        if isinstance(error, ValidationError):
                            exception_message = ', '.join(error.messages)
                        else:
                            exception_message = unicode(error)

                        messages.error(
                            request, _(
                                'Error editing metadata for document: '
                                '%(document)s; %(exception)s.'
                            ) % {
                                'document': document,
                                'exception': exception_message
                            }
                        )
                else:
                    messages.success(
                        request,
                        _(
                            'Metadata for document %s edited successfully.'
                        ) % document
                    )

            return HttpResponseRedirect(next)
    else:
        formset = MetadataFormSet(initial=initial)

    context = {
        'form_display_mode_table': True,
        'form': formset,
        'next': next,
    }

    if documents.count() == 1:
        context['object'] = documents.first()

    context['title'] = ungettext(
        'Edit document metadata',
        'Edit documents metadata',
        documents.count()
    )

    return render_to_response(
        'appearance/generic_form.html', context,
        context_instance=RequestContext(request)
    )


def metadata_multiple_edit(request):
    return metadata_edit(
        request, document_id_list=request.GET.get(
            'id_list', request.POST.get('id_list', '')
        ).split(',')
    )


def metadata_add(request, document_id=None, document_id_list=None):
    if document_id:
        documents = Document.objects.filter(pk=document_id)
        if not documents:
            raise Document.DoesNotExist
    elif document_id_list:
        documents = Document.objects.select_related('document_type').filter(pk__in=document_id_list)
        if len(set([document.document_type.pk for document in documents])) > 1:
            messages.error(
                request, _('Only select documents of the same type.')
            )
            return HttpResponseRedirect(
                request.META.get(
                    'HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL)
                )
            )

    documents = AccessControlList.objects.filter_by_access(
        permission_metadata_document_add, request.user, queryset=documents
    )

    if not documents:
        if document_id:
            raise PermissionDenied
        else:
            messages.error(request, _('Must provide at least one document.'))
            return HttpResponseRedirect(
                request.META.get(
                    'HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL)
                )
            )

    for document in documents:
        document.add_as_recent_document_for_user(request.user)

    post_action_redirect = reverse('documents:document_list_recent')

    next = request.POST.get(
        'next',
        request.GET.get(
            'next', request.META.get('HTTP_REFERER', post_action_redirect)
        )
    )

    if request.method == 'POST':
        form = AddMetadataForm(
            data=request.POST, document_type=document.document_type
        )
        if form.is_valid():
            metadata_type = form.cleaned_data['metadata_type']
            for document in documents:
                try:
                    document_metadata, created = DocumentMetadata.objects.get_or_create(
                        document=document,
                        metadata_type=metadata_type,
                        defaults={'value': ''}
                    )
                except Exception as exception:
                    if getattr(settings, 'DEBUG', False):
                        raise
                    else:
                        messages.error(
                            request,
                            _(
                                'Error adding metadata type '
                                '"%(metadata_type)s" to document: '
                                '%(document)s; %(exception)s'
                            ) % {
                                'metadata_type': metadata_type,
                                'document': document,
                                'exception': ', '.join(
                                    getattr(exception, 'messages', exception)
                                )
                            }
                        )
                else:
                    if created:
                        messages.success(
                            request,
                            _(
                                'Metadata type: %(metadata_type)s '
                                'successfully added to document %(document)s.'
                            ) % {
                                'metadata_type': metadata_type,
                                'document': document
                            }
                        )
                    else:
                        messages.warning(
                            request, _(
                                'Metadata type: %(metadata_type)s already '
                                'present in document %(document)s.'
                            ) % {
                                'metadata_type': metadata_type,
                                'document': document
                            }
                        )

            if documents.count() == 1:
                return HttpResponseRedirect('%s?%s' % (
                    reverse('metadata:metadata_edit', args=(document.pk,)),
                    urlencode({'next': next}))
                )
            elif documents.count() > 1:
                return HttpResponseRedirect('%s?%s' % (
                    reverse('metadata:metadata_multiple_edit'),
                    urlencode({'id_list': ','.join(document_id_list), 'next': next}))
                )

    else:
        form = AddMetadataForm(document_type=document.document_type)

    context = {
        'form': form,
        'next': next,
    }

    if documents.count() == 1:
        context['object'] = documents.first()

    context['title'] = ungettext(
        'Add metadata types to document',
        'Add metadata types to documents',
        documents.count()
    )

    return render_to_response(
        'appearance/generic_form.html', context,
        context_instance=RequestContext(request)
    )


def metadata_multiple_add(request):
    return metadata_add(
        request, document_id_list=request.GET.get(
            'id_list', request.POST.get('id_list', '')
        ).split(',')
    )


def metadata_remove(request, document_id=None, document_id_list=None):
    if document_id:
        documents = Document.objects.filter(pk=document_id)
        if not documents:
            raise Document.DoesNotExist
    elif document_id_list:
        documents = Document.objects.filter(pk__in=document_id_list)

    documents = AccessControlList.objects.filter_by_access(
        permission_metadata_document_remove, request.user, queryset=documents
    )

    if not documents:
        if document_id:
            raise PermissionDenied
        else:
            messages.error(request, _('Must provide at least one document.'))
            return HttpResponseRedirect(
                request.META.get(
                    'HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL)
                )
            )

    if len(set([document.document_type.pk for document in documents])) > 1:
        messages.error(request, _('Only select documents of the same type.'))
        return HttpResponseRedirect(
            request.META.get(
                'HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL)
            )
        )

    if set(documents.values_list('metadata__value', flat=True)) == set([None]):
        message = ungettext(
            'The selected document doesn\'t have any metadata.',
            'The selected documents doesn\'t have any metadata.',
            len(documents)
        )
        messages.warning(request, message)
        return HttpResponseRedirect(
            request.META.get(
                'HTTP_REFERER', reverse(settings.LOGIN_REDIRECT_URL)
            )
        )

    post_action_redirect = reverse('documents:document_list_recent')

    next = request.POST.get(
        'next', request.GET.get(
            'next', request.META.get('HTTP_REFERER', post_action_redirect)
        )
    )

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
        initial.append(
            {
                'document_type': documents[0].document_type,
                'metadata_type': key,
                'value': ', '.join(value)
            }
        )

    if request.method == 'POST':
        formset = MetadataRemoveFormSet(request.POST)
        if formset.is_valid():
            for document in documents:

                for form in formset.forms:
                    if form.cleaned_data['update']:
                        metadata_type = get_object_or_404(
                            MetadataType, pk=form.cleaned_data['id']
                        )
                        try:
                            document_metadata = DocumentMetadata.objects.get(
                                document=document, metadata_type=metadata_type
                            )
                            document_metadata.delete()
                            messages.success(
                                request,
                                _(
                                    'Successfully remove metadata type "%(metadata_type)s" from document: %(document)s.'
                                ) % {
                                    'metadata_type': metadata_type,
                                    'document': document
                                }
                            )
                        except Exception as exception:
                            messages.error(
                                request,
                                _(
                                    'Error removing metadata type "%(metadata_type)s" from document: %(document)s; %(exception)s'
                                ) % {
                                    'metadata_type': metadata_type,
                                    'document': document,
                                    'exception': ', '.join(exception.messages)
                                }
                            )

            return HttpResponseRedirect(next)
    else:
        formset = MetadataRemoveFormSet(initial=initial)

    context = {
        'form_display_mode_table': True,
        'form': formset,
        'next': next,
    }

    if documents.count() == 1:
        context['object'] = documents.first()

    context['title'] = ungettext(
        'Remove metadata types from the document',
        'Remove metadata types from the documents',
        documents.count()
    )

    return render_to_response(
        'appearance/generic_form.html', context,
        context_instance=RequestContext(request)
    )


def metadata_multiple_remove(request):
    return metadata_remove(
        request, document_id_list=request.GET.get(
            'id_list', request.POST.get('id_list', '')
        ).split(',')
    )


class DocumentMetadataListView(SingleObjectListView):
    def dispatch(self, request, *args, **kwargs):
        AccessControlList.objects.check_access(
            permissions=permission_metadata_document_view,
            user=self.request.user, obj=self.get_document()
        )

        return super(DocumentMetadataListView, self).dispatch(
            request, *args, **kwargs
        )

    def get_document(self):
        return get_object_or_404(Document, pk=self.kwargs['pk'])

    def get_extra_context(self):
        document = self.get_document()
        return {
            'hide_link': True,
            'object': document,
            'title': _('Metadata for document: %s') % document,
        }

    def get_queryset(self):
        return self.get_document().metadata.all()


# Setup views
class MetadataTypeCreateView(SingleObjectCreateView):
    extra_context = {'title': _('Create metadata type')}
    form_class = MetadataTypeForm
    model = MetadataType
    post_action_redirect = reverse_lazy('metadata:setup_metadata_type_list')
    view_permission = permission_metadata_type_create


class MetadataTypeDeleteView(SingleObjectDeleteView):
    model = MetadataType
    post_action_redirect = reverse_lazy('metadata:setup_metadata_type_list')
    view_permission = permission_metadata_type_delete

    def get_extra_context(self):
        return {
            'delete_view': True,
            'object': self.get_object(),
            'title': _('Delete the metadata type: %s?') % self.get_object(),
        }


class MetadataTypeEditView(SingleObjectEditView):
    form_class = MetadataTypeForm
    model = MetadataType
    post_action_redirect = reverse_lazy('metadata:setup_metadata_type_list')
    view_permission = permission_metadata_type_edit

    def get_extra_context(self):
        return {
            'object': self.get_object(),
            'title': _('Edit metadata type: %s') % self.get_object(),
        }


class MetadataTypeListView(SingleObjectListView):
    view_permission = permission_metadata_type_view

    def get_queryset(self):
        return MetadataType.objects.all()

    def get_extra_context(self):
        return {
            'extra_columns': (
                {
                    'name': _('Internal name'),
                    'attribute': 'name',
                },
            ),
            'hide_link': True,
            'title': _('Metadata types'),
        }


class SetupDocumentTypeMetadataOptionalView(AssignRemoveView):
    decode_content_type = True
    view_permission = permission_document_type_edit
    left_list_title = _('Available metadata types')
    right_list_title = _('Metadata types assigned')

    def add(self, item):
        self.get_object().metadata.create(metadata_type=item, required=False)

    def get_object(self):
        return get_object_or_404(DocumentType, pk=self.kwargs['pk'])

    def left_list(self):
        return AssignRemoveView.generate_choices(
            set(MetadataType.objects.all()) - set(
                MetadataType.objects.filter(
                    id__in=self.get_object().metadata.values_list(
                        'metadata_type', flat=True
                    )
                )
            )
        )

    def right_list(self):
        return AssignRemoveView.generate_choices(
            self.get_object().metadata.filter(required=False)
        )

    def remove(self, item):
        item.delete()

    def get_extra_context(self):
        return {
            'object': self.get_object(),
            'title': _(
                'Optional metadata types for document type: %s'
            ) % self.get_object(),
        }


class SetupDocumentTypeMetadataRequiredView(SetupDocumentTypeMetadataOptionalView):
    def add(self, item):
        self.get_object().metadata.create(metadata_type=item, required=True)

    def right_list(self):
        return AssignRemoveView.generate_choices(
            self.get_object().metadata.filter(required=True)
        )

    def get_extra_context(self):
        return {
            'object': self.get_object(),
            'title': _(
                'Required metadata types for document type: %s'
            ) % self.get_object(),
        }
