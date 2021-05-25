import logging

from django.template import RequestContext
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.models import AccessControlList
from mayan.apps.documents.models import Document
from mayan.apps.documents.views.document_views import DocumentListView
from mayan.apps.views.generics import (
    MultipleObjectFormActionView, SingleObjectCreateView,
    SingleObjectDeleteView, SingleObjectEditView, SingleObjectListView
)
from mayan.apps.views.mixins import ExternalObjectViewMixin

from .forms import CabinetListForm
from .icons import icon_cabinet
from .links import (
    link_document_cabinet_add, link_cabinet_child_add, link_cabinet_create
)
from .models import Cabinet
from .permissions import (
    permission_cabinet_add_document, permission_cabinet_create,
    permission_cabinet_delete, permission_cabinet_edit,
    permission_cabinet_view, permission_cabinet_remove_document
)
from .widgets import jstree_data

logger = logging.getLogger(name=__name__)


class CabinetCreateView(SingleObjectCreateView):
    fields = ('label',)
    model = Cabinet
    post_action_redirect = reverse_lazy(viewname='cabinets:cabinet_list')
    view_permission = permission_cabinet_create

    def get_extra_context(self):
        return {
            'title': _('Create cabinet'),
        }

    def get_instance_extra_data(self):
        return {'_event_actor': self.request.user}


class CabinetChildAddView(ExternalObjectViewMixin, SingleObjectCreateView):
    fields = ('label',)
    external_object_class = Cabinet
    external_object_permission = permission_cabinet_edit
    external_object_pk_url_kwarg = 'cabinet_id'

    def get_extra_context(self):
        return {
            'title': _(
                'Add new level to: %s'
            ) % self.external_object.get_full_path(),
            'object': self.external_object
        }

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user,
            'parent': self.external_object
        }

    def get_queryset(self):
        return self.external_object.get_descendants()


class CabinetDeleteView(SingleObjectDeleteView):
    model = Cabinet
    object_permission = permission_cabinet_delete
    post_action_redirect = reverse_lazy(viewname='cabinets:cabinet_list')
    pk_url_kwarg = 'cabinet_id'

    def get_extra_context(self):
        return {
            'object': self.object,
            'title': _('Delete the cabinet: %s?') % self.object,
        }


class CabinetDetailView(ExternalObjectViewMixin, DocumentListView):
    external_object_class = Cabinet
    external_object_permission = permission_cabinet_view
    external_object_pk_url_kwarg = 'cabinet_id'
    template_name = 'cabinets/cabinet_details.html'

    def get_document_queryset(self):
        return self.external_object.get_documents_queryset()

    def get_extra_context(self, **kwargs):
        context = super().get_extra_context(**kwargs)

        context.update(
            {
                'column_class': 'col-xs-12 col-sm-6 col-md-4 col-lg-3',
                'hide_links': True,
                'jstree_data': '\n'.join(
                    jstree_data(
                        node=self.external_object.get_root(),
                        selected_node=self.external_object
                    )
                ),
                'list_as_items': True,
                'no_results_icon': icon_cabinet,
                'no_results_main_link': link_cabinet_child_add.resolve(
                    context=RequestContext(
                        request=self.request, dict_={
                            'object': self.external_object
                        }
                    )
                ),
                'no_results_text': _(
                    'Cabinet levels can contain documents or other '
                    'cabinet sub levels. To add documents to a cabinet, '
                    'select the cabinet view of a document view.'
                ),
                'no_results_title': _('This cabinet level is empty'),
                'object': self.external_object,
                'title': _(
                    'Details of cabinet: %s'
                ) % self.external_object.get_full_path(),
            }
        )

        return context


class CabinetEditView(SingleObjectEditView):
    fields = ('label',)
    model = Cabinet
    object_permission = permission_cabinet_edit
    post_action_redirect = reverse_lazy(viewname='cabinets:cabinet_list')
    pk_url_kwarg = 'cabinet_id'

    def get_extra_context(self):
        return {
            'object': self.object,
            'title': _('Edit cabinet: %s') % self.object,
        }

    def get_instance_extra_data(self):
        return {'_event_actor': self.request.user}


class CabinetListView(SingleObjectListView):
    object_permission = permission_cabinet_view

    def get_extra_context(self):
        return {
            'hide_link': True,
            'hide_object': True,
            'title': _('Cabinets'),
            'no_results_icon': icon_cabinet,
            'no_results_main_link': link_cabinet_create.resolve(
                context=RequestContext(request=self.request)
            ),
            'no_results_text': _(
                'Cabinets are a multi-level method to organize '
                'documents. Each cabinet can contain documents as '
                'well as other sub level cabinets.'
            ),
            'no_results_title': _('No cabinets available'),
        }

    def get_source_queryset(self):
        return Cabinet.objects.root_nodes()


class DocumentCabinetAddView(MultipleObjectFormActionView):
    form_class = CabinetListForm
    object_permission = permission_cabinet_add_document
    pk_url_kwarg = 'document_id'
    source_queryset = Document.valid
    success_message_single = _(
        'Document "%(object)s" added to cabinets successfully.'
    )
    success_message_singular = _(
        '%(count)d document added to cabinets successfully.'
    )
    success_message_plural = _(
        '%(count)d documents added to cabinets successfully.'
    )
    title_single = _('Add document "%(object)s" to cabinets.')
    title_singular = _('Add %(count)d document to cabinets.')
    title_plural = _('Add %(count)d documents to cabinets.')

    def get_extra_context(self):
        context = {
            'submit_label': _('Add'),
        }

        if self.object_list.count() == 1:
            context.update(
                {
                    'object': self.object_list.first(),
                }
            )

        return context

    def get_form_extra_kwargs(self):
        kwargs = {
            'help_text': _(
                'Cabinets to which the selected documents will be added.'
            ),
            'permission': permission_cabinet_add_document,
            'queryset': Cabinet.objects.all(),
            'user': self.request.user
        }

        if self.object_list.count() == 1:
            kwargs.update(
                {
                    'queryset': Cabinet.objects.exclude(
                        pk__in=self.object_list.first().cabinets.all()
                    )
                }
            )

        return kwargs

    def object_action(self, form, instance):
        for cabinet in form.cleaned_data['cabinets']:
            AccessControlList.objects.check_access(
                obj=cabinet, permissions=(permission_cabinet_add_document,),
                user=self.request.user
            )

            cabinet._event_actor = self.request.user
            cabinet.document_add(document=instance)


class DocumentCabinetListView(ExternalObjectViewMixin, CabinetListView):
    external_object_permission = permission_cabinet_view
    external_object_pk_url_kwarg = 'document_id'
    external_object_queryset = Document.valid

    def get_extra_context(self):
        return {
            'hide_link': True,
            'no_results_icon': icon_cabinet,
            'no_results_main_link': link_document_cabinet_add.resolve(
                context=RequestContext(
                    request=self.request, dict_={
                        'object': self.external_object
                    }
                )
            ),
            'no_results_text': _(
                'Documents can be added to many cabinets.'
            ),
            'no_results_title': _(
                'This document is not in any cabinet'
            ),
            'object': self.external_object,
            'title': _(
                'Cabinets containing document: %s'
            ) % self.external_object,
        }

    def get_source_queryset(self):
        return self.external_object.get_cabinets(
            permission=permission_cabinet_view, user=self.request.user
        )


class DocumentCabinetRemoveView(MultipleObjectFormActionView):
    form_class = CabinetListForm
    object_permission = permission_cabinet_remove_document
    pk_url_kwarg = 'document_id'
    source_queryset = Document.valid
    success_message_single = _(
        'Document "%(object)s" removed from cabinets successfully.'
    )
    success_message_singular = _(
        '%(count)d document removed from cabinets successfully.'
    )
    success_message_plural = _(
        '%(count)d documents removed from cabinets successfully.'
    )
    title_single = _('Remove document "%(object)s" from cabinets.')
    title_singular = _('Remove %(count)d document from cabinets.')
    title_plural = _('Remove %(count)d documents from cabinets.')

    def get_extra_context(self):
        context = {
            'submit_label': _('Remove'),
        }

        if self.object_list.count() == 1:
            context.update(
                {
                    'object': self.object_list.first(),
                }
            )

        return context

    def get_form_extra_kwargs(self):
        kwargs = {
            'help_text': _(
                'Cabinets from which the selected documents will be removed.'
            ),
            'permission': permission_cabinet_remove_document,
            'queryset': Cabinet.objects.all(),
            'user': self.request.user
        }

        if self.object_list.count() == 1:
            kwargs.update(
                {
                    'queryset': self.object_list.first().cabinets.all()
                }
            )

        return kwargs

    def object_action(self, form, instance):
        for cabinet in form.cleaned_data['cabinets']:
            AccessControlList.objects.check_access(
                obj=cabinet, permissions=(permission_cabinet_remove_document,),
                user=self.request.user
            )

            cabinet._event_actor = self.request.user
            cabinet.document_remove(document=instance)
