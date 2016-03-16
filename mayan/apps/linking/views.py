from __future__ import absolute_import, unicode_literals

import logging

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from acls.models import AccessControlList
from common.generics import (
    AssignRemoveView, SingleObjectCreateView, SingleObjectDeleteView,
    SingleObjectEditView, SingleObjectListView
)
from documents.models import Document, DocumentType
from documents.permissions import permission_document_view
from documents.views import DocumentListView
from permissions import Permission

from .forms import SmartLinkConditionForm, SmartLinkForm
from .models import ResolvedSmartLink, SmartLink, SmartLinkCondition
from .permissions import (
    permission_smart_link_create, permission_smart_link_delete,
    permission_smart_link_edit, permission_smart_link_view
)

logger = logging.getLogger(__name__)


class SetupSmartLinkDocumentTypesView(AssignRemoveView):
    decode_content_type = True
    left_list_title = _('Available document types')
    right_list_title = _('Document types enabled')
    object_permission = permission_smart_link_edit

    def add(self, item):
        self.get_object().document_types.add(item)

    def get_object(self):
        return get_object_or_404(SmartLink, pk=self.kwargs['pk'])

    def left_list(self):
        return AssignRemoveView.generate_choices(
            DocumentType.objects.exclude(
                pk__in=self.get_object().document_types.all()
            )
        )

    def right_list(self):
        return AssignRemoveView.generate_choices(
            self.get_object().document_types.all()
        )

    def remove(self, item):
        self.get_object().document_types.remove(item)

    def get_extra_context(self):
        return {
            'object': self.get_object(),
            'title': _(
                'Document type for which to enable smart link: %s'
            ) % self.get_object()
        }


class ResolvedSmartLinkView(DocumentListView):
    def dispatch(self, request, *args, **kwargs):
        self.document = get_object_or_404(
            Document, pk=self.kwargs['document_pk']
        )
        self.smart_link = get_object_or_404(
            SmartLink, pk=self.kwargs['smart_link_pk']
        )

        try:
            Permission.check_permissions(
                request.user, (permission_document_view,)
            )
        except PermissionDenied:
            AccessControlList.objects.check_access(
                permission_document_view, request.user, self.document
            )

        try:
            Permission.check_permissions(
                request.user, (permission_smart_link_view,)
            )
        except PermissionDenied:
            AccessControlList.objects.check_access(
                permission_smart_link_view, request.user, self.smart_link
            )

        return super(
            ResolvedSmartLinkView, self
        ).dispatch(request, *args, **kwargs)

    def get_document_queryset(self):
        try:
            queryset = self.smart_link.get_linked_document_for(self.document)
        except Exception as exception:
            queryset = Document.objects.none()

            if self.request.user.is_staff or self.request.user.is_superuser:
                messages.error(
                    self.request, _('Smart link query error: %s' % exception)
                )

        return queryset

    def get_extra_context(self):
        dynamic_label = self.smart_link.get_dynamic_label(self.document)
        if dynamic_label:
            title = _('Documents in smart link: %s') % dynamic_label
        else:
            title = _(
                'Documents in smart link "%(smart_link)s" as related to '
                '"%(document)s"'
            ) % {
                'document': self.document,
                'smart_link': self.smart_link.label,
            }

        return {
            'hide_links': True,
            'object': self.document,
            'title': title,
        }


class SmartLinkListView(SingleObjectListView):
    object_permission = permission_smart_link_view

    def get_queryset(self):
        self.queryset = self.get_smart_link_queryset()
        return super(SmartLinkListView, self).get_queryset()

    def get_smart_link_queryset(self):
        return SmartLink.objects.all()

    def get_extra_context(self):
        return {
            'hide_link': True,
            'title': _('Smart links'),
        }


class DocumentSmartLinkListView(SmartLinkListView):
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
            DocumentSmartLinkListView, self
        ).dispatch(request, *args, **kwargs)

    def get_smart_link_queryset(self):
        return ResolvedSmartLink.objects.filter(
            document_types=self.document.document_type, enabled=True
        )

    def get_extra_context(self):
        return {
            'document': self.document,
            'hide_object': True,
            'hide_link': True,
            'object': self.document,
            'title': _('Smart links for document: %s') % self.document,
        }


class SmartLinkCreateView(SingleObjectCreateView):
    extra_context = {'title': _('Create new smart link')}
    form_class = SmartLinkForm
    post_action_redirect = reverse_lazy('linking:smart_link_list')
    view_permission = permission_smart_link_create


class SmartLinkEditView(SingleObjectEditView):
    form_class = SmartLinkForm
    model = SmartLink
    post_action_redirect = reverse_lazy('linking:smart_link_list')
    view_permission = permission_smart_link_edit

    def get_extra_context(self):
        return {
            'object': self.get_object(),
            'title': _('Edit smart link: %s') % self.get_object()
        }


class SmartLinkDeleteView(SingleObjectDeleteView):
    model = SmartLink
    post_action_redirect = reverse_lazy('linking:smart_link_list')
    view_permission = permission_smart_link_delete

    def get_extra_context(self):
        return {
            'object': self.get_object(),
            'title': _('Delete smart link: %s') % self.get_object()
        }


class SmartLinkConditionListView(SingleObjectListView):
    view_permission = permission_smart_link_edit

    def get_extra_context(self):
        return {
            'hide_link': True,
            'object': self.get_smart_link(),
            'title': _(
                'Conditions for smart link: %s'
            ) % self.get_smart_link(),
        }

    def get_smart_link(self):
        return get_object_or_404(SmartLink, pk=self.kwargs['pk'])

    def get_queryset(self):
        return self.get_smart_link().conditions.all()


class SmartLinkConditionCreateView(SingleObjectCreateView):
    form_class = SmartLinkConditionForm
    object_name = _('SmartLink condition')

    def dispatch(self, request, *args, **kwargs):
        try:
            Permission.check_permissions(
                request.user, (permission_smart_link_edit,)
            )
        except PermissionDenied:
            AccessControlList.objects.check_access(
                (permission_smart_link_edit,), request.user,
                self.get_smart_link()
            )
        return super(
            SmartLinkConditionCreateView, self
        ).dispatch(request, *args, **kwargs)

    def get_extra_context(self):
        return {
            'title': _(
                'Add new conditions to smart link: "%s"'
            ) % self.get_smart_link(),
            'object': self.get_smart_link(),
            'object_name': _('Smart link condition'),
        }

    def get_instance_extra_data(self):
        return {'smart_link': self.get_smart_link()}

    def get_post_action_redirect(self):
        return reverse(
            'linking:smart_link_condition_list', args=(self.get_smart_link().pk,)
        )

    def get_smart_link(self):
        return get_object_or_404(SmartLink, pk=self.kwargs['pk'])

    def get_queryset(self):
        return self.get_smart_link().conditions.all()


class SmartLinkConditionEditView(SingleObjectEditView):
    form_class = SmartLinkConditionForm
    model = SmartLinkCondition

    def dispatch(self, request, *args, **kwargs):
        try:
            Permission.check_permissions(
                request.user, (permission_smart_link_edit,)
            )
        except PermissionDenied:
            AccessControlList.objects.check_access(
                (permission_smart_link_edit,), request.user,
                self.get_object().smart_link
            )

        return super(
            SmartLinkConditionEditView, self
        ).dispatch(request, *args, **kwargs)

    def get_extra_context(self):
        return {
            'condition': self.get_object(),
            'navigation_object_list': ('object', 'condition'),
            'object': self.get_object().smart_link,
            'object_name': _('Smart link condition'),
            'title': _('Edit smart link condition'),
        }

    def get_post_action_redirect(self):
        return reverse(
            'linking:smart_link_condition_list', args=(
                self.get_object().smart_link.pk,
            )
        )


class SmartLinkConditionDeleteView(SingleObjectDeleteView):
    model = SmartLinkCondition

    def dispatch(self, request, *args, **kwargs):
        try:
            Permission.check_permissions(
                request.user, (permission_smart_link_edit,)
            )
        except PermissionDenied:
            AccessControlList.objects.check_access(
                (permission_smart_link_edit,), request.user,
                self.get_object().smart_link
            )

        return super(
            SmartLinkConditionDeleteView, self
        ).dispatch(request, *args, **kwargs)

    def get_extra_context(self):
        return {
            'condition': self.get_object(),
            'navigation_object_list': ('object', 'condition'),
            'object': self.get_object().smart_link,
            'object_name': _('Smart link condition'),
            'title': _(
                'Delete smart link condition: "%s"?'
            ) % self.get_object(),
        }

    def get_post_action_redirect(self):
        return reverse(
            'linking:smart_link_condition_list', args=(
                self.get_object().smart_link.pk,
            )
        )
