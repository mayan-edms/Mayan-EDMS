from __future__ import absolute_import, unicode_literals

import logging

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.urls import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.models import AccessControlList
from mayan.apps.common.generics import (
    AddRemoveView, SingleObjectCreateView, SingleObjectDeleteView,
    SingleObjectEditView, SingleObjectListView
)
from mayan.apps.documents.events import event_document_type_edited
from mayan.apps.documents.models import Document, DocumentType
from mayan.apps.documents.permissions import (
    permission_document_type_edit, permission_document_view
)
from mayan.apps.documents.views.document_views import DocumentListView

from .events import event_smart_link_edited
from .forms import SmartLinkConditionForm, SmartLinkForm
from .icons import icon_smart_link_setup, icon_smart_link_condition
from .links import link_smart_link_create, link_smart_link_condition_create
from .models import ResolvedSmartLink, SmartLink, SmartLinkCondition
from .permissions import (
    permission_smart_link_create, permission_smart_link_delete,
    permission_smart_link_edit, permission_smart_link_view
)

logger = logging.getLogger(__name__)


class DocumentTypeSmartLinksView(AddRemoveView):
    main_object_method_add = 'smart_link_add'
    main_object_method_remove = 'smart_link_remove'
    main_object_permission = permission_document_type_edit
    main_object_model = DocumentType
    main_object_pk_url_kwarg = 'pk'
    secondary_object_model = SmartLink
    secondary_object_permission = permission_smart_link_edit
    list_available_title = _('Available smart links')
    list_added_title = _('Smart links enabled')
    related_field = 'smart_links'

    def action_add(self, queryset, _user):
        with transaction.atomic():
            event_document_type_edited.commit(
                actor=_user, target=self.main_object
            )
            for obj in queryset:
                self.main_object.smart_links.add(obj)
                event_smart_link_edited.commit(
                    actor=_user, action_object=self.main_object, target=obj
                )

    def action_remove(self, queryset, _user):
        with transaction.atomic():
            event_document_type_edited.commit(
                actor=_user, target=self.main_object
            )
            for obj in queryset:
                self.main_object.smart_links.remove(obj)
                event_smart_link_edited.commit(
                    actor=_user, action_object=self.main_object, target=obj
                )

    def get_actions_extra_kwargs(self):
        return {'_user': self.request.user}

    def get_extra_context(self):
        return {
            'object': self.main_object,
            'title': _(
                'Smart links to enable for document type: %s'
            ) % self.main_object,
        }


class ResolvedSmartLinkView(DocumentListView):
    def dispatch(self, request, *args, **kwargs):
        self.document = get_object_or_404(
            klass=Document, pk=self.kwargs['document_pk']
        )
        self.smart_link = get_object_or_404(
            klass=SmartLink, pk=self.kwargs['smart_link_pk']
        )

        AccessControlList.objects.check_access(
            obj=self.document, permissions=(permission_document_view,),
            user=request.user
        )

        AccessControlList.objects.check_access(
            obj=self.smart_link, permissions=(permission_smart_link_view,),
            user=request.user
        )

        return super(
            ResolvedSmartLinkView, self
        ).dispatch(request, *args, **kwargs)

    def get_document_queryset(self):
        try:
            queryset = self.smart_link.get_linked_document_for(self.document)
        except Exception as exception:
            queryset = Document.objects.none()

            try:
                AccessControlList.objects.check_access(
                    obj=self.smart_link,
                    permissions=(permission_smart_link_edit,),
                    user=self.request.user
                )
            except PermissionDenied:
                pass
            else:
                messages.error(
                    message=_('Smart link query error: %s' % exception),
                    request=self.request
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

        context = super(ResolvedSmartLinkView, self).get_extra_context()
        context.update(
            {
                'object': self.document,
                'title': title,
            }
        )
        return context


class SetupSmartLinkDocumentTypesView(AddRemoveView):
    main_object_method_add = 'document_types_add'
    main_object_method_remove = 'document_types_remove'
    main_object_permission = permission_smart_link_edit
    main_object_model = SmartLink
    main_object_pk_url_kwarg = 'pk'
    secondary_object_model = DocumentType
    secondary_object_permission = permission_document_type_edit
    list_available_title = _('Available document types')
    list_added_title = _('Document types enabled')
    related_field = 'document_types'

    def get_actions_extra_kwargs(self):
        return {'_user': self.request.user}

    def get_extra_context(self):
        return {
            'object': self.main_object,
            'title': _(
                'Document type for which to enable smart link: %s'
            ) % self.main_object,
        }


class SmartLinkListView(SingleObjectListView):
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

    def get_source_queryset(self):
        return self.get_smart_link_queryset()

    def get_smart_link_queryset(self):
        return SmartLink.objects.all()


class DocumentSmartLinkListView(SmartLinkListView):
    def dispatch(self, request, *args, **kwargs):
        self.document = get_object_or_404(klass=Document, pk=self.kwargs['pk'])

        AccessControlList.objects.check_access(
            obj=self.document, permissions=(permission_document_view,),
            user=request.user
        )

        return super(
            DocumentSmartLinkListView, self
        ).dispatch(request, *args, **kwargs)

    def get_extra_context(self):
        return {
            'document': self.document,
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
            'object': self.document,
            'title': _('Smart links for document: %s') % self.document,
        }

    def get_smart_link_queryset(self):
        return ResolvedSmartLink.objects.get_for(document=self.document)


class SmartLinkCreateView(SingleObjectCreateView):
    extra_context = {'title': _('Create new smart link')}
    form_class = SmartLinkForm
    post_action_redirect = reverse_lazy(
        viewname='linking:smart_link_list'
    )
    view_permission = permission_smart_link_create

    def get_save_extra_data(self):
        return {'_user': self.request.user}


class SmartLinkDeleteView(SingleObjectDeleteView):
    model = SmartLink
    object_permission = permission_smart_link_delete
    post_action_redirect = reverse_lazy(
        viewname='linking:smart_link_list'
    )

    def get_extra_context(self):
        return {
            'object': self.get_object(),
            'title': _('Delete smart link: %s') % self.get_object()
        }


class SmartLinkEditView(SingleObjectEditView):
    form_class = SmartLinkForm
    model = SmartLink
    object_permission = permission_smart_link_edit
    post_action_redirect = reverse_lazy(
        viewname='linking:smart_link_list'
    )

    def get_extra_context(self):
        return {
            'object': self.get_object(),
            'title': _('Edit smart link: %s') % self.get_object()
        }

    def get_save_extra_data(self):
        return {'_user': self.request.user}


class SmartLinkConditionListView(SingleObjectListView):
    object_permission = permission_smart_link_edit

    def get_extra_context(self):
        return {
            'hide_link': True,
            'hide_object': True,
            'no_results_icon': icon_smart_link_condition,
            'no_results_main_link': link_smart_link_condition_create.resolve(
                context=RequestContext(
                    request=self.request, dict_={
                        'object': self.get_smart_link()
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
            'object': self.get_smart_link(),
            'title': _(
                'Conditions for smart link: %s'
            ) % self.get_smart_link(),
        }

    def get_source_queryset(self):
        return self.get_smart_link().conditions.all()

    def get_smart_link(self):
        return get_object_or_404(klass=SmartLink, pk=self.kwargs['pk'])


class SmartLinkConditionCreateView(SingleObjectCreateView):
    form_class = SmartLinkConditionForm

    def dispatch(self, request, *args, **kwargs):
        AccessControlList.objects.check_access(
            obj=self.get_smart_link(),
            permissions=(permission_smart_link_edit,),
            user=request.user
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
        }

    def get_instance_extra_data(self):
        return {'smart_link': self.get_smart_link()}

    def get_post_action_redirect(self):
        return reverse(
            viewname='linking:smart_link_condition_list', kwargs={
                'pk': self.get_smart_link().pk
            }
        )

    def get_queryset(self):
        return self.get_smart_link().conditions.all()

    def get_smart_link(self):
        return get_object_or_404(klass=SmartLink, pk=self.kwargs['pk'])


class SmartLinkConditionEditView(SingleObjectEditView):
    form_class = SmartLinkConditionForm
    model = SmartLinkCondition

    def dispatch(self, request, *args, **kwargs):
        AccessControlList.objects.check_access(
            obj=self.get_object().smart_link,
            permissions=(permission_smart_link_edit,), user=request.user
        )

        return super(
            SmartLinkConditionEditView, self
        ).dispatch(request, *args, **kwargs)

    def get_extra_context(self):
        return {
            'condition': self.get_object(),
            'navigation_object_list': ('object', 'condition'),
            'object': self.get_object().smart_link,
            'title': _('Edit smart link condition'),
        }

    def get_post_action_redirect(self):
        return reverse(
            viewname='linking:smart_link_condition_list', kwargs={
                'pk': self.get_object().smart_link.pk
            }
        )


class SmartLinkConditionDeleteView(SingleObjectDeleteView):
    model = SmartLinkCondition

    def dispatch(self, request, *args, **kwargs):
        AccessControlList.objects.check_access(
            obj=self.get_object().smart_link,
            permissions=(permission_smart_link_edit,), user=request.user
        )

        return super(
            SmartLinkConditionDeleteView, self
        ).dispatch(request, *args, **kwargs)

    def get_extra_context(self):
        return {
            'condition': self.get_object(),
            'navigation_object_list': ('object', 'condition'),
            'object': self.get_object().smart_link,
            'title': _(
                'Delete smart link condition: "%s"?'
            ) % self.get_object(),
        }

    def get_post_action_redirect(self):
        return reverse(
            viewname='linking:smart_link_condition_list', kwargs={
                'pk': self.get_object().smart_link.pk
            }
        )
