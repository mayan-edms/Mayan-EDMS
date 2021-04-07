import logging

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.urls import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.models import AccessControlList
from mayan.apps.documents.models import Document, DocumentType
from mayan.apps.documents.permissions import (
    permission_document_type_edit, permission_document_view
)
from mayan.apps.documents.views.document_views import DocumentListView
from mayan.apps.views.generics import (
    AddRemoveView, SingleObjectCreateView, SingleObjectDeleteView,
    SingleObjectEditView, SingleObjectListView
)
from mayan.apps.views.mixins import ExternalObjectViewMixin

from .events import event_smart_link_edited
from .forms import SmartLinkConditionForm, SmartLinkForm
from .icons import icon_smart_link_setup, icon_smart_link_condition
from .links import link_smart_link_create, link_smart_link_condition_create
from .models import ResolvedSmartLink, SmartLink, SmartLinkCondition
from .permissions import (
    permission_smart_link_create, permission_smart_link_delete,
    permission_smart_link_edit, permission_smart_link_view
)

logger = logging.getLogger(name=__name__)


class DocumentTypeSmartLinkAddRemoveView(AddRemoveView):
    main_object_permission = permission_document_type_edit
    main_object_model = DocumentType
    main_object_pk_url_kwarg = 'document_type_id'
    secondary_object_model = SmartLink
    secondary_object_permission = permission_smart_link_edit
    list_available_title = _('Available smart links')
    list_added_title = _('Smart links enabled')
    related_field = 'smart_links'

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


class ResolvedSmartLinkView(ExternalObjectViewMixin, DocumentListView):
    external_object_permission = permission_document_view
    external_object_pk_url_kwarg = 'document_id'
    external_object_queryset = Document.valid

    def dispatch(self, request, *args, **kwargs):
        self.smart_link = self.get_smart_link()

        return super().dispatch(request, *args, **kwargs)

    def get_document_queryset(self):
        try:
            queryset = self.smart_link.get_linked_document_for(
                document=self.external_object
            )
        except Exception as exception:
            queryset = Document.objects.none()

            # Check if the user has the smart link edit permission before
            # showing the exception text.
            try:
                AccessControlList.objects.check_access(
                    obj=self.smart_link,
                    permissions=(permission_smart_link_edit,),
                    user=self.request.user
                )
            except PermissionDenied:
                """User doesn't have the required permission."""
            else:
                messages.error(
                    message=_('Smart link query error: %s' % exception),
                    request=self.request
                )

        return queryset

    def get_extra_context(self):
        dynamic_label = self.smart_link.get_dynamic_label(
            document=self.external_object
        )
        if dynamic_label:
            title = _('Documents in smart link: %s') % dynamic_label
        else:
            title = _(
                'Documents in smart link "%(smart_link)s" as related to '
                '"%(document)s"'
            ) % {
                'document': self.external_object,
                'smart_link': self.smart_link.label,
            }

        context = super().get_extra_context()
        context.update(
            {
                'object': self.external_object,
                'title': title,
            }
        )
        return context

    def get_smart_link(self):
        queryset = AccessControlList.objects.restrict_queryset(
            permission=permission_smart_link_view,
            queryset=SmartLink.objects.filter(enabled=True),
            user=self.request.user
        )

        return get_object_or_404(
            klass=queryset, pk=self.kwargs['smart_link_id']
        )


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

    def get_actions_extra_kwargs(self):
        return {'_event_actor': self.request.user}

    def get_extra_context(self):
        return {
            'object': self.main_object,
            'title': _(
                'Document type for which to enable smart link: %s'
            ) % self.main_object,
        }


class SmartLinkListView(SingleObjectListView):
    model = SmartLink
    object_permission = permission_smart_link_view

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


class DocumentSmartLinkListView(ExternalObjectViewMixin, SmartLinkListView):
    external_object_permission = permission_document_view
    external_object_pk_url_kwarg = 'document_id'
    external_object_queryset = Document.valid

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
                'There are no smart links for this document'
            ),
            'object': self.external_object,
            'title': _('Smart links for document: %s') % self.external_object,
        }

    def get_source_queryset(self):
        # Override SingleObjectListView source queryset from SmartLink to
        # ResolvedSmartLink.
        return ResolvedSmartLink.objects.get_for(
            document=self.external_object
        )


class SmartLinkCreateView(SingleObjectCreateView):
    extra_context = {'title': _('Create new smart link')}
    form_class = SmartLinkForm
    post_action_redirect = reverse_lazy(
        viewname='linking:smart_link_list'
    )
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

    def get_extra_context(self):
        return {
            'object': self.object,
            'title': _('Edit smart link: %s') % self.object
        }

    def get_instance_extra_data(self):
        return {'_event_actor': self.request.user}


class SmartLinkConditionListView(ExternalObjectViewMixin, SingleObjectListView):
    external_object_class = SmartLink
    external_object_permission = permission_smart_link_edit
    external_object_pk_url_kwarg = 'smart_link_id'

    def get_extra_context(self):
        return {
            'hide_link': True,
            'hide_object': True,
            'no_results_icon': icon_smart_link_condition,
            'no_results_main_link': link_smart_link_condition_create.resolve(
                context=RequestContext(
                    request=self.request, dict_={
                        'object': self.external_object
                    }
                )
            ),
            'no_results_text': _(
                'Conditions are small logic units that when combined '
                'define how the smart link will behave.'
            ),
            'no_results_title': _(
                'There are no conditions for this smart link'
            ),
            'object': self.external_object,
            'title': _(
                'Conditions for smart link: %s'
            ) % self.external_object,
        }

    def get_source_queryset(self):
        return self.external_object.conditions.all()


class SmartLinkConditionCreateView(
    ExternalObjectViewMixin, SingleObjectCreateView
):
    external_object_class = SmartLink
    external_object_permission = permission_smart_link_edit
    external_object_pk_url_kwarg = 'smart_link_id'
    form_class = SmartLinkConditionForm

    def get_extra_context(self):
        return {
            'title': _(
                'Add new conditions to smart link: "%s"'
            ) % self.external_object,
            'object': self.external_object,
        }

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user,
            'smart_link': self.external_object
        }

    def get_post_action_redirect(self):
        return reverse(
            viewname='linking:smart_link_condition_list', kwargs={
                'smart_link_id': self.external_object.pk
            }
        )

    def get_queryset(self):
        return self.external_object.conditions.all()


class SmartLinkConditionDeleteView(SingleObjectDeleteView):
    model = SmartLinkCondition
    object_permission = permission_smart_link_edit
    pk_url_kwarg = 'smart_link_condition_id'

    def get_extra_context(self):
        return {
            'condition': self.object,
            'navigation_object_list': ('object', 'condition'),
            'object': self.object.smart_link,
            'title': _(
                'Delete smart link condition: "%s"?'
            ) % self.object,
        }

    def get_instance_extra_data(self):
        return {'_event_actor': self.request.user}

    def get_post_action_redirect(self):
        return reverse(
            viewname='linking:smart_link_condition_list', kwargs={
                'smart_link_id': self.object.smart_link.pk
            }
        )


class SmartLinkConditionEditView(SingleObjectEditView):
    form_class = SmartLinkConditionForm
    model = SmartLinkCondition
    object_permission = permission_smart_link_edit
    pk_url_kwarg = 'smart_link_condition_id'

    def get_extra_context(self):
        return {
            'condition': self.object,
            'navigation_object_list': ('object', 'condition'),
            'object': self.object.smart_link,
            'title': _('Edit smart link condition'),
        }

    def get_instance_extra_data(self):
        return {'_event_actor': self.request.user}

    def get_post_action_redirect(self):
        return reverse(
            viewname='linking:smart_link_condition_list', kwargs={
                'smart_link_id': self.object.smart_link.pk
            }
        )
