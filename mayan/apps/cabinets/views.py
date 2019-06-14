from __future__ import absolute_import, unicode_literals

import logging

from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _, ungettext

from mayan.apps.acls.models import AccessControlList
from mayan.apps.common.generics import (
    MultipleObjectFormActionView, SingleObjectCreateView,
    SingleObjectDeleteView, SingleObjectEditView, SingleObjectListView
)
from mayan.apps.common.mixins import ExternalObjectMixin
from mayan.apps.documents.permissions import permission_document_view
from mayan.apps.documents.models import Document
from mayan.apps.documents.views import DocumentListView

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

logger = logging.getLogger(__name__)


class CabinetCreateView(SingleObjectCreateView):
    fields = ('label',)
    model = Cabinet
    post_action_redirect = reverse_lazy(viewname='cabinets:cabinet_list')
    view_permission = permission_cabinet_create

    def get_extra_context(self):
        return {
            'title': _('Create cabinet'),
        }

    def get_save_extra_data(self):
        return {'_user': self.request.user}


class CabinetChildAddView(ExternalObjectMixin, SingleObjectCreateView):
    fields = ('label',)
    external_object_class = Cabinet
    external_object_permission = permission_cabinet_edit

    def get_extra_context(self):
        return {
            'title': _(
                'Add new level to: %s'
            ) % self.external_object.get_full_path(),
            'object': self.external_object
        }

    def get_instance_extra_data(self):
        return {
            'parent': self.external_object,
        }

    def get_queryset(self):
        return self.external_object.get_descendants()

    def get_save_extra_data(self):
        return {
            '_user': self.request.user
        }


class CabinetDeleteView(SingleObjectDeleteView):
    model = Cabinet
    object_permission = permission_cabinet_delete
    post_action_redirect = reverse_lazy(viewname='cabinets:cabinet_list')

    def get_extra_context(self):
        return {
            'object': self.get_object(),
            'title': _('Delete the cabinet: %s?') % self.get_object(),
        }


class CabinetDetailView(ExternalObjectMixin, DocumentListView):
    external_object_class = Cabinet
    external_object_permission = permission_cabinet_view
    template_name = 'cabinets/cabinet_details.html'

    def get_document_queryset(self):
        return self.external_object.documents.all()

    def get_context_data(self, **kwargs):
        context = super(CabinetDetailView, self).get_context_data(**kwargs)

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

    def get_save_extra_data(self):
        return {'_user': self.request.user}


class CabinetEditView(SingleObjectEditView):
    fields = ('label',)
    model = Cabinet
    object_permission = permission_cabinet_edit
    post_action_redirect = reverse_lazy(viewname='cabinets:cabinet_list')

    def get_extra_context(self):
        return {
            'object': self.get_object(),
            'title': _('Edit cabinet: %s') % self.get_object(),
        }

    def get_save_extra_data(self):
        return {'_user': self.request.user}


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
        # Add explicit ordering of root nodes since the queryset returned
        # is not affected by the model's order Meta option.
        return Cabinet.objects.root_nodes().order_by('label')


class DocumentCabinetListView(CabinetListView):
    def dispatch(self, request, *args, **kwargs):
        self.document = get_object_or_404(klass=Document, pk=self.kwargs['pk'])

        AccessControlList.objects.check_access(
            obj=self.document, permissions=(permission_document_view,),
            user=request.user
        )

        return super(DocumentCabinetListView, self).dispatch(
            request, *args, **kwargs
        )

    def get_extra_context(self):
        return {
            'hide_link': True,
            'no_results_icon': icon_cabinet,
            'no_results_main_link': link_document_cabinet_add.resolve(
                context=RequestContext(
                    request=self.request, dict_={'object': self.document}
                )
            ),
            'no_results_text': _(
                'Documents can be added to many cabinets.'
            ),
            'no_results_title': _(
                'This document is not in any cabinet'
            ),
            'object': self.document,
            'title': _('Cabinets containing document: %s') % self.document,
        }

    def get_source_queryset(self):
        return self.document.document_cabinets()


class DocumentAddToCabinetView(MultipleObjectFormActionView):
    form_class = CabinetListForm
    model = Document
    object_permission = permission_cabinet_add_document
    success_message = _(
        'Add to cabinet request performed on %(count)d document'
    )
    success_message_plural = _(
        'Add to cabinet request performed on %(count)d documents'
    )

    def get_extra_context(self):
        queryset = self.object_list

        result = {
            'submit_label': _('Add'),
            'title': ungettext(
                singular='Add %(count)d document to cabinets',
                plural='Add %(count)d documents to cabinets',
                number=queryset.count()
            ) % {
                'count': queryset.count(),
            }
        }

        if queryset.count() == 1:
            result.update(
                {
                    'object': queryset.first(),
                    'title': _(
                        'Add document "%s" to cabinets'
                    ) % queryset.first()
                }
            )

        return result

    def get_form_extra_kwargs(self):
        queryset = self.object_list
        result = {
            'help_text': _(
                'Cabinets to which the selected documents will be added.'
            ),
            'permission': permission_cabinet_add_document,
            'queryset': Cabinet.objects.all(),
            'user': self.request.user
        }

        if queryset.count() == 1:
            result.update(
                {
                    'queryset': Cabinet.objects.exclude(
                        pk__in=queryset.first().cabinets.all()
                    )
                }
            )

        return result

    def object_action(self, form, instance):
        cabinet_membership = instance.cabinets.all()

        for cabinet in form.cleaned_data['cabinets']:
            AccessControlList.objects.check_access(
                obj=cabinet, permissions=(permission_cabinet_add_document,),
                user=self.request.user
            )
            if cabinet in cabinet_membership:
                messages.warning(
                    message=_(
                        'Document: %(document)s is already in '
                        'cabinet: %(cabinet)s.'
                    ) % {
                        'document': instance, 'cabinet': cabinet
                    }, request=self.request
                )
            else:
                cabinet.document_add(
                    document=instance, _user=self.request.user
                )
                messages.success(
                    message=_(
                        'Document: %(document)s added to cabinet: '
                        '%(cabinet)s successfully.'
                    ) % {
                        'document': instance, 'cabinet': cabinet
                    }, request=self.request
                )


class DocumentRemoveFromCabinetView(MultipleObjectFormActionView):
    form_class = CabinetListForm
    model = Document
    object_permission = permission_cabinet_remove_document
    success_message = _(
        'Remove from cabinet request performed on %(count)d document'
    )
    success_message_plural = _(
        'Remove from cabinet request performed on %(count)d documents'
    )

    def get_extra_context(self):
        queryset = self.object_list

        result = {
            'submit_label': _('Remove'),
            'title': ungettext(
                singular='Remove %(count)d document from cabinets',
                plural='Remove %(count)d documents from cabinets',
                number=queryset.count()
            ) % {
                'count': queryset.count(),
            }
        }

        if queryset.count() == 1:
            result.update(
                {
                    'object': queryset.first(),
                    'title': _(
                        'Remove document "%s" from cabinets'
                    ) % queryset.first()
                }
            )

        return result

    def get_form_extra_kwargs(self):
        queryset = self.object_list
        result = {
            'help_text': _(
                'Cabinets from which the selected documents will be removed.'
            ),
            'permission': permission_cabinet_remove_document,
            'queryset': Cabinet.objects.all(),
            'user': self.request.user
        }

        if queryset.count() == 1:
            result.update(
                {
                    'queryset': queryset.first().cabinets.all()
                }
            )

        return result

    def object_action(self, form, instance):
        cabinet_membership = instance.cabinets.all()

        for cabinet in form.cleaned_data['cabinets']:
            AccessControlList.objects.check_access(
                obj=cabinet, permissions=(permission_cabinet_remove_document,),
                user=self.request.user
            )

            if cabinet not in cabinet_membership:
                messages.warning(
                    message=_(
                        'Document: %(document)s is not in cabinet: '
                        '%(cabinet)s.'
                    ) % {
                        'document': instance, 'cabinet': cabinet
                    }, request=self.request
                )
            else:
                cabinet.document_remove(
                    document=instance, _user=self.request.user
                )
                messages.success(
                    message=_(
                        'Document: %(document)s removed from cabinet: '
                        '%(cabinet)s.'
                    ) % {
                        'document': instance, 'cabinet': cabinet
                    }, request=self.request
                )
