from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.urls import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _, ungettext

from mayan.apps.acls.models import AccessControlList
from mayan.apps.documents.models import DocumentType
from mayan.apps.documents.permissions import permission_document_type_edit
from mayan.apps.views.generics import (
    AddRemoveView, ConfirmView, FormView, SingleObjectCreateView,
    SingleObjectDeleteView, SingleObjectEditView, SingleObjectListView
)
from mayan.apps.views.mixins import ExternalObjectViewMixin

from ..events import event_index_template_edited
from ..forms import IndexTemplateFilteredForm, IndexTemplateNodeForm
from ..icons import icon_index
from ..links import link_index_template_create
from ..models import IndexTemplate, IndexTemplateNode
from ..permissions import (
    permission_index_template_create, permission_index_template_delete,
    permission_index_template_edit, permission_index_template_rebuild,
    permission_index_template_view
)
from ..tasks import task_rebuild_index

__all__ = (
    'DocumentTypeIndexTemplateListView', 'IndexTemplateListView',
    'IndexTemplateCreateView', 'IndexTemplateDeleteView',
    'IndexTemplateDocumentTypesView', 'IndexTemplateEditView',
    'IndexTemplateNodeListView', 'IndexTemplateNodeCreateView',
    'IndexTemplateNodeDeleteView', 'IndexTemplateNodeEditView',
    'IndexTemplateAllRebuildView', 'IndexTemplateRebuildView',
    'IndexTemplateResetView'
)


class DocumentTypeIndexTemplateListView(AddRemoveView):
    main_object_permission = permission_document_type_edit
    main_object_model = DocumentType
    main_object_pk_url_kwarg = 'document_type_id'
    secondary_object_model = IndexTemplate
    secondary_object_permission = permission_index_template_edit
    list_available_title = _('Available indexes')
    list_added_title = _('Indexes linked')
    related_field = 'index_templates'

    def action_add(self, queryset, _event_actor):
        for obj in queryset:
            self.main_object.index_templates.add(obj)
            event_index_template_edited.commit(
                action_object=self.main_object, actor=_event_actor, target=obj
            )

    def action_remove(self, queryset, _event_actor):
        for obj in queryset:
            self.main_object.index_templates.remove(obj)
            event_index_template_edited.commit(
                action_object=self.main_object, actor=_event_actor, target=obj
            )

    def get_actions_extra_kwargs(self):
        return {'_event_actor': self.request.user}

    def get_extra_context(self):
        return {
            'object': self.main_object,
            'subtitle': _(
                'Documents of this type will appear in the indexes linked '
                'when these are updated. Events of the documents of this type '
                'will trigger updates in the linked indexes.'
            ),
            'title': _('Indexes linked to document type: %s') % self.main_object,
        }


class IndexTemplateListView(SingleObjectListView):
    model = IndexTemplate
    object_permission = permission_index_template_view

    def get_extra_context(self):
        return {
            'hide_object': True,
            'no_results_icon': icon_index,
            'no_results_main_link': link_index_template_create.resolve(
                context=RequestContext(request=self.request)
            ),
            'no_results_text': _(
                'Indexes group document automatically into levels. Indexes are '
                'defined using template whose markers are replaced with '
                'direct properties of documents like label or description, or '
                'that of extended properties like metadata.'
            ),
            'no_results_title': _('There are no index templates.'),
            'title': _('Index templates'),
        }


class IndexTemplateCreateView(SingleObjectCreateView):
    extra_context = {'title': _('Create index')}
    fields = ('label', 'slug', 'enabled')
    model = IndexTemplate
    post_action_redirect = reverse_lazy(
        viewname='indexing:index_template_list'
    )
    view_permission = permission_index_template_create

    def get_instance_extra_data(self):
        return {'_event_actor': self.request.user}


class IndexTemplateDeleteView(SingleObjectDeleteView):
    model = IndexTemplate
    object_permission = permission_index_template_delete
    pk_url_kwarg = 'index_template_id'
    post_action_redirect = reverse_lazy(
        viewname='indexing:index_template_list'
    )

    def get_extra_context(self):
        return {
            'object': self.object,
            'title': _('Delete the index: %s?') % self.object,
        }


class IndexTemplateDocumentTypesView(AddRemoveView):
    main_object_method_add_name = 'document_types_add'
    main_object_method_remove_name = 'document_types_remove'
    main_object_permission = permission_index_template_edit
    main_object_model = IndexTemplate
    main_object_pk_url_kwarg = 'index_template_id'
    secondary_object_model = DocumentType
    secondary_object_permission = permission_document_type_edit
    list_available_title = _('Available document types')
    list_added_title = _('Document types linked')
    related_field = 'document_types'

    def get_actions_extra_kwargs(self):
        return {'_event_actor': self.request.user}

    def get_extra_context(self):
        return {
            'object': self.main_object,
            'subtitle': _(
                'Only the documents of the types selected will be shown '
                'in the index when built. Only the events of the documents '
                'of the types select will trigger updates in the index.'
            ),
            'title': _('Document types linked to index: %s') % self.main_object,
        }


class IndexTemplateEditView(SingleObjectEditView):
    fields = ('label', 'slug', 'enabled')
    model = IndexTemplate
    object_permission = permission_index_template_edit
    pk_url_kwarg = 'index_template_id'
    post_action_redirect = reverse_lazy(
        viewname='indexing:index_template_list'
    )

    def get_extra_context(self):
        return {
            'object': self.object,
            'title': _('Edit index: %s') % self.object,
        }

    def get_instance_extra_data(self):
        return {'_event_actor': self.request.user}


class IndexTemplateNodeListView(
    ExternalObjectViewMixin, SingleObjectListView
):
    external_object_class = IndexTemplate
    external_object_permission = permission_index_template_edit
    external_object_pk_url_kwarg = 'index_template_id'

    def get_extra_context(self):
        return {
            'hide_object': True,
            'index': self.external_object,
            'navigation_object_list': ('index',),
            'title': _(
                'Tree template nodes for index: %s'
            ) % self.external_object,
        }

    def get_source_queryset(self):
        return self.external_object.template_root.get_descendants(
            include_self=True
        )


class IndexTemplateNodeCreateView(SingleObjectCreateView):
    form_class = IndexTemplateNodeForm
    model = IndexTemplateNode

    def dispatch(self, request, *args, **kwargs):
        AccessControlList.objects.check_access(
            obj=self.get_parent_node().index,
            permissions=(permission_index_template_edit,), user=request.user
        )

        return super().dispatch(request, *args, **kwargs)

    def get_extra_context(self):
        return {
            'index': self.get_parent_node().index,
            'navigation_object_list': ('index',),
            'title': _('Create child node of: %s') % self.get_parent_node(),
        }

    def get_initial(self):
        parent_node = self.get_parent_node()
        return {
            'index': parent_node.index, 'parent': parent_node
        }

    def get_parent_node(self):
        return get_object_or_404(
            klass=IndexTemplateNode, pk=self.kwargs['index_template_node_id']
        )


class IndexTemplateNodeDeleteView(SingleObjectDeleteView):
    model = IndexTemplateNode
    object_permission = permission_index_template_edit
    pk_url_kwarg = 'index_template_node_id'

    def get_extra_context(self):
        return {
            'index': self.object.index,
            'navigation_object_list': ('index', 'node'),
            'node': self.object,
            'title': _(
                'Delete the index template node: %s?'
            ) % self.object,
        }

    def get_post_action_redirect(self):
        return reverse(
            viewname='indexing:index_template_view', kwargs={
                'index_template_id': self.object.index.pk
            }
        )


class IndexTemplateNodeEditView(SingleObjectEditView):
    form_class = IndexTemplateNodeForm
    model = IndexTemplateNode
    object_permission = permission_index_template_edit
    pk_url_kwarg = 'index_template_node_id'

    def get_extra_context(self):
        return {
            'index': self.object.index,
            'navigation_object_list': ('index', 'node'),
            'node': self.object,
            'title': _(
                'Edit the index template node: %s?'
            ) % self.object,
        }

    def get_post_action_redirect(self):
        return reverse(
            viewname='indexing:index_template_view', kwargs={
                'index_template_id': self.object.index.pk
            }
        )


class IndexTemplateRebuildView(ConfirmView):
    post_action_redirect = reverse_lazy(
        viewname='indexing:index_template_list'
    )

    def get_extra_context(self):
        return {
            'object': self.get_object(),
            'title': _('Rebuild index template: %s') % self.get_object()
        }

    def get_object(self):
        return get_object_or_404(
            klass=self.get_queryset(), pk=self.kwargs['index_template_id']
        )

    def get_queryset(self):
        return AccessControlList.objects.restrict_queryset(
            permission=permission_index_template_rebuild,
            queryset=IndexTemplate.objects.all(), user=self.request.user
        )

    def view_action(self):
        task_rebuild_index.apply_async(
            kwargs=dict(index_id=self.get_object().pk)
        )

        messages.success(
            message=_('Index template queued for rebuild.'),
            request=self.request
        )


class IndexTemplateAllRebuildView(FormView):
    extra_context = {
        'title': _('Rebuild index templates'),
    }
    form_class = IndexTemplateFilteredForm

    def form_valid(self, form):
        count = 0
        for index in form.cleaned_data['index_templates']:
            task_rebuild_index.apply_async(
                kwargs=dict(index_id=index.pk)
            )
            count += 1

        messages.success(
            message=ungettext(
                singular='%(count)d index template queued for rebuild.',
                plural='%(count)d index templates queued for rebuild.',
                number=count
            ) % {
                'count': count,
            }, request=self.request
        )

        return super().form_valid(form=form)

    def get_form_extra_kwargs(self):
        return {
            'user': self.request.user
        }

    def get_post_action_redirect(self):
        return reverse(viewname='common:tools_list')


class IndexTemplateResetView(FormView):
    extra_context = {
        'title': _('Reset indexes'),
    }
    form_class = IndexTemplateFilteredForm

    def form_valid(self, form):
        count = 0
        for index in form.cleaned_data['index_templates']:
            index.reset()
            count += 1

        messages.success(
            message=ungettext(
                singular='%(count)d index reset.',
                plural='%(count)d indexes reset.',
                number=count
            ) % {
                'count': count,
            }, request=self.request
        )

        return super().form_valid(form=form)

    def get_form_extra_kwargs(self):
        return {
            'help_text': _(
                'Index templates for which their instances will be deleted.'
            ),
            'user': self.request.user
        }

    def get_post_action_redirect(self):
        return reverse(viewname='common:tools_list')
