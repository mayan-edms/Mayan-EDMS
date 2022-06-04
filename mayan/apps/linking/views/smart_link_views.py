import logging

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.models import AccessControlList
from mayan.apps.documents.models import Document, DocumentType
from mayan.apps.documents.permissions import permission_document_type_edit
from mayan.apps.documents.views.document_views import DocumentListView
from mayan.apps.views.generics import (
    AddRemoveView, SingleObjectCreateView, SingleObjectDeleteView,
    SingleObjectEditView, SingleObjectListView
)
from mayan.apps.views.mixins import ExternalObjectViewMixin

from ..events import event_smart_link_edited
from ..forms import SmartLinkForm
from ..icons import (
    icon_document_smart_link_instance_list, icon_document_type_smart_links,
    icon_smart_link_create, icon_smart_link_delete,
    icon_smart_link_document_type_list, icon_smart_link_edit,
    icon_smart_link_instance_detail, icon_smart_link_list,
    icon_smart_link_setup
)
from ..links import link_smart_link_create
from ..models import ResolvedSmartLink, SmartLink
from ..permissions import (
    permission_resolved_smart_link_view, permission_smart_link_create,
    permission_smart_link_delete, permission_smart_link_edit,
    permission_smart_link_view
)

logger = logging.getLogger(name=__name__)


class DocumentResolvedSmartLinkDocumentListView(
    ExternalObjectViewMixin, DocumentListView
):
    external_object_permission = permission_resolved_smart_link_view
    external_object_pk_url_kwarg = 'document_id'
    external_object_queryset = Document.valid.all()
    view_icon = icon_smart_link_instance_detail

    def dispatch(self, request, *args, **kwargs):
        self.resolved_smart_link = self.get_resolved_smart_link()

        return super().dispatch(request, *args, **kwargs)

    def get_document_queryset(self):
        try:
            queryset = self.resolved_smart_link.get_linked_documents_for(
                document=self.external_object
            )
        except Exception as exception:
            queryset = Document.objects.none()

            # Check if the user has the smart link edit permission before
            # showing the exception text.
            try:
                AccessControlList.objects.check_access(
                    obj=self.resolved_smart_link,
                    permissions=(permission_smart_link_edit,),
                    user=self.request.user
                )
            except PermissionDenied:
                """User doesn't have the required permission."""
            else:
                messages.error(
                    message=_(
                        'Resolved smart link query error: %s' % exception
                    ), request=self.request
                )

        return queryset

    def get_extra_context(self):
        try:
            resolved_smart_link_label = self.resolved_smart_link.get_label_for(
                document=self.external_object
            )
        except Exception as exception:
            resolved_smart_link_label = self.resolved_smart_link.label

            # Check if the user has the smart link edit permission before
            # showing the exception text.
            try:
                AccessControlList.objects.check_access(
                    obj=self.resolved_smart_link,
                    permissions=(permission_smart_link_edit,),
                    user=self.request.user
                )
            except PermissionDenied:
                """User doesn't have the required permission."""
            else:
                messages.error(
                    message=_(
                        'Resolved smart link dynamic label error: %s' % exception
                    ), request=self.request
                )

        title = _(
            'Documents in resolved smart link "%(resolved_smart_link)s" for '
            '"%(document)s"'
        ) % {
            'document': self.external_object,
            'resolved_smart_link': resolved_smart_link_label
        }

        context = super().get_extra_context()
        context.update(
            {
                'object': self.external_object,
                'title': title,
            }
        )
        return context

    def get_resolved_smart_link(self):
        queryset = AccessControlList.objects.restrict_queryset(
            permission=permission_resolved_smart_link_view,
            queryset=ResolvedSmartLink.objects.filter(enabled=True),
            user=self.request.user
        )

        return get_object_or_404(
            klass=queryset, pk=self.kwargs['smart_link_id']
        )


class SmartLinkListView(SingleObjectListView):
    model = SmartLink
    object_permission = permission_smart_link_view
    view_icon = icon_smart_link_list

    def get_extra_context(self):
        return {
            'hide_link': True,
            'hide_object': True,
            'no_results_icon': icon_smart_link_setup,
            'no_results_main_link': link_smart_link_create.resolve(
                context=RequestContext(request=self.request)
            ),
            'no_results_text': _(
                'Indexes group documents into units, usually with similar '
                'properties and of equal or similar types. Smart links '
                'allow defining relationships between documents even '
                'if they are in different indexes and are of different '
                'types.'
            ),
            'no_results_title': _(
                'There are no smart links'
            ),
            'title': _('Smart links'),
        }


class DocumentResolvedSmartLinkListView(
    ExternalObjectViewMixin, SingleObjectListView
):
    external_object_permission = permission_resolved_smart_link_view
    external_object_pk_url_kwarg = 'document_id'
    external_object_queryset = Document.valid.all()
    object_permission = permission_resolved_smart_link_view
    view_icon = icon_document_smart_link_instance_list

    def get_extra_context(self):
        return {
            'document': self.external_object,
            'hide_link': True,
            'hide_object': True,
            'no_results_icon': icon_smart_link_setup,
            'no_results_text': _(
                'Smart links allow defining relationships between '
                'documents even if they are in different indexes and '
                'are of different types.'
            ),
            'no_results_title': _(
                'There are no resolved smart links for this document'
            ),
            'object': self.external_object,
            'title': _(
                'Resolved smart links for document: %s'
            ) % self.external_object,
        }

    def get_source_queryset(self):
        return ResolvedSmartLink.objects.get_for(
            document=self.external_object
        )


class DocumentTypeSmartLinkAddRemoveView(AddRemoveView):
    main_object_permission = permission_document_type_edit
    main_object_model = DocumentType
    main_object_pk_url_kwarg = 'document_type_id'
    secondary_object_model = SmartLink
    secondary_object_permission = permission_smart_link_edit
    list_available_title = _('Available smart links')
    list_added_title = _('Smart links enabled')
    related_field = 'smart_links'
    view_icon = icon_document_type_smart_links

    def action_add(self, queryset, _event_actor):
        for obj in queryset:
            self.main_object.smart_links.add(obj)
            event_smart_link_edited.commit(
                actor=_event_actor or self._event_actor,
                action_object=self.main_object, target=obj
            )

    def action_remove(self, queryset, _event_actor):
        for obj in queryset:
            self.main_object.smart_links.remove(obj)
            event_smart_link_edited.commit(
                actor=_event_actor or self._event_actor,
                action_object=self.main_object, target=obj
            )

    def get_actions_extra_kwargs(self):
        return {'_event_actor': self.request.user}

    def get_extra_context(self):
        return {
            'object': self.main_object,
            'title': _(
                'Smart links to enable for document type: %s'
            ) % self.main_object,
        }


class SmartLinkDocumentTypeAddRemoveView(AddRemoveView):
    main_object_method_add_name = 'document_types_add'
    main_object_method_remove_name = 'document_types_remove'
    main_object_permission = permission_smart_link_edit
    main_object_model = SmartLink
    main_object_pk_url_kwarg = 'smart_link_id'
    secondary_object_model = DocumentType
    secondary_object_permission = permission_document_type_edit
    list_available_title = _('Available document types')
    list_added_title = _('Document types enabled')
    related_field = 'document_types'
    view_icon = icon_smart_link_document_type_list

    def get_actions_extra_kwargs(self):
        return {'_event_actor': self.request.user}

    def get_extra_context(self):
        return {
            'object': self.main_object,
            'title': _(
                'Document type for which to enable smart link: %s'
            ) % self.main_object,
        }


class SmartLinkCreateView(SingleObjectCreateView):
    extra_context = {'title': _('Create new smart link')}
    form_class = SmartLinkForm
    post_action_redirect = reverse_lazy(
        viewname='linking:smart_link_list'
    )
    view_icon = icon_smart_link_create
    view_permission = permission_smart_link_create

    def get_instance_extra_data(self):
        return {'_event_actor': self.request.user}


class SmartLinkDeleteView(SingleObjectDeleteView):
    model = SmartLink
    object_permission = permission_smart_link_delete
    pk_url_kwarg = 'smart_link_id'
    post_action_redirect = reverse_lazy(
        viewname='linking:smart_link_list'
    )
    view_icon = icon_smart_link_delete

    def get_extra_context(self):
        return {
            'object': self.object,
            'title': _('Delete smart link: %s') % self.object
        }


class SmartLinkEditView(SingleObjectEditView):
    form_class = SmartLinkForm
    model = SmartLink
    object_permission = permission_smart_link_edit
    pk_url_kwarg = 'smart_link_id'
    post_action_redirect = reverse_lazy(
        viewname='linking:smart_link_list'
    )
    view_icon = icon_smart_link_edit

    def get_extra_context(self):
        return {
            'object': self.object,
            'title': _('Edit smart link: %s') % self.object
        }

    def get_instance_extra_data(self):
        return {'_event_actor': self.request.user}
