from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.urls import reverse, reverse_lazy
from django.utils.html import mark_safe
from django.utils.translation import ugettext_lazy as _, ungettext

from mayan.apps.acls.models import AccessControlList
from mayan.apps.documents.events import event_document_type_edited
from mayan.apps.documents.models import Document, DocumentType
from mayan.apps.documents.permissions import (
    permission_document_type_edit, permission_document_view
)
from mayan.apps.documents.views.document_views import DocumentListView
from mayan.apps.views.generics import (
    AddRemoveView, ConfirmView, FormView, SingleObjectCreateView,
    SingleObjectDeleteView, SingleObjectEditView, SingleObjectListView
)
from mayan.apps.views.mixins import ExternalObjectMixin

from .events import event_index_template_edited
from .forms import IndexTemplateFilteredForm, IndexTemplateNodeForm
from .html_widgets import node_tree
from .icons import icon_index
from .links import link_index_template_create
from .models import (
    DocumentIndexInstanceNode, Index, IndexInstance, IndexInstanceNode,
    IndexTemplateNode
)
from .permissions import (
    permission_document_indexing_create, permission_document_indexing_delete,
    permission_document_indexing_edit,
    permission_document_indexing_instance_view,
    permission_document_indexing_rebuild, permission_document_indexing_view
)
from .tasks import task_rebuild_index


class DocumentTypeIndexesView(AddRemoveView):
    main_object_permission = permission_document_indexing_edit
    main_object_model = DocumentType
    main_object_pk_url_kwarg = 'document_type_id'
    secondary_object_model = Index
    secondary_object_permission = permission_document_type_edit
    list_available_title = _('Available indexes')
    list_added_title = _('Indexes linked')
    related_field = 'indexes'

    def action_add(self, queryset, _user):
        event_document_type_edited.commit(
            actor=_user, target=self.main_object
        )
        for obj in queryset:
            self.main_object.indexes.add(obj)
            event_index_template_edited.commit(
                actor=_user, action_object=self.main_object, target=obj
            )

    def action_remove(self, queryset, _user):
        event_document_type_edited.commit(
            actor=_user, target=self.main_object
        )
        for obj in queryset:
            self.main_object.indexes.remove(obj)
            event_index_template_edited.commit(
                actor=_user, action_object=self.main_object, target=obj
            )

    def get_actions_extra_kwargs(self):
        return {'_user': self.request.user}

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


# Setup views
class SetupIndexCreateView(SingleObjectCreateView):
    extra_context = {'title': _('Create index')}
    fields = ('label', 'slug', 'enabled')
    model = Index
    post_action_redirect = reverse_lazy(
        viewname='indexing:index_setup_list'
    )
    view_permission = permission_document_indexing_create

    def get_save_extra_data(self):
        return {'_user': self.request.user}


class SetupIndexDeleteView(SingleObjectDeleteView):
    model = Index
    object_permission = permission_document_indexing_delete
    pk_url_kwarg = 'index_template_id'
    post_action_redirect = reverse_lazy(
        viewname='indexing:index_setup_list'
    )

    def get_extra_context(self):
        return {
            'object': self.object,
            'title': _('Delete the index: %s?') % self.object,
        }


class SetupIndexEditView(SingleObjectEditView):
    fields = ('label', 'slug', 'enabled')
    model = Index
    object_permission = permission_document_indexing_edit
    pk_url_kwarg = 'index_template_id'
    post_action_redirect = reverse_lazy(
        viewname='indexing:index_setup_list'
    )

    def get_extra_context(self):
        return {
            'object': self.object,
            'title': _('Edit index: %s') % self.object,
        }

    def get_save_extra_data(self):
        return {'_user': self.request.user}


class SetupIndexListView(SingleObjectListView):
    model = Index
    object_permission = permission_document_indexing_view

    def get_extra_context(self):
        return {
            'hide_object': True,
            'no_results_icon': icon_index,
            'no_results_main_link': link_index_template_create.resolve(
                context=RequestContext(request=self.request)
            ),
            'no_results_text': _(
                'Indexes group document automatically into levels. Indexe are '
                'defined using template whose markers are replaced with '
                'direct properties of documents like label or description, or '
                'that of extended properties like metadata.'
            ),
            'no_results_title': _('There are no indexes.'),
            'title': _('Indexes'),
        }


class SetupIndexRebuildView(ConfirmView):
    post_action_redirect = reverse_lazy(
        viewname='indexing:index_setup_list'
    )

    def get_extra_context(self):
        return {
            'object': self.get_object(),
            'title': _('Rebuild index: %s') % self.get_object()
        }

    def get_object(self):
        return get_object_or_404(
            klass=self.get_queryset(), pk=self.kwargs['index_template_id']
        )

    def get_queryset(self):
        return AccessControlList.objects.restrict_queryset(
            permission=permission_document_indexing_rebuild,
            queryset=Index.objects.all(), user=self.request.user
        )

    def view_action(self):
        task_rebuild_index.apply_async(
            kwargs=dict(index_id=self.get_object().pk)
        )

        messages.success(
            message=_('Index queued for rebuild.'), request=self.request
        )


class SetupIndexDocumentTypesView(AddRemoveView):
    main_object_method_add = 'document_types_add'
    main_object_method_remove = 'document_types_remove'
    main_object_permission = permission_document_indexing_edit
    main_object_model = Index
    main_object_pk_url_kwarg = 'index_template_id'
    secondary_object_model = DocumentType
    secondary_object_permission = permission_document_type_edit
    list_available_title = _('Available document types')
    list_added_title = _('Document types linked')
    related_field = 'document_types'

    def get_actions_extra_kwargs(self):
        return {'_user': self.request.user}

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


class SetupIndexTreeTemplateListView(
    ExternalObjectMixin, SingleObjectListView
):
    external_object_class = Index
    external_object_permission = permission_document_indexing_edit
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


class TemplateNodeCreateView(SingleObjectCreateView):
    form_class = IndexTemplateNodeForm
    model = IndexTemplateNode

    def dispatch(self, request, *args, **kwargs):
        AccessControlList.objects.check_access(
            obj=self.get_parent_node().index,
            permissions=(permission_document_indexing_edit,), user=request.user
        )

        return super(
            TemplateNodeCreateView, self
        ).dispatch(request, *args, **kwargs)

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


class TemplateNodeDeleteView(SingleObjectDeleteView):
    model = IndexTemplateNode
    object_permission = permission_document_indexing_edit
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
            viewname='indexing:index_setup_view', kwargs={
                'index_template_id': self.object.index.pk
            }
        )


class TemplateNodeEditView(SingleObjectEditView):
    form_class = IndexTemplateNodeForm
    model = IndexTemplateNode
    object_permission = permission_document_indexing_edit
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
            viewname='indexing:index_setup_view', kwargs={
                'index_template_id': self.object.index.pk
            }
        )


class IndexListView(SingleObjectListView):
    object_permission = permission_document_indexing_instance_view

    def get_extra_context(self):
        return {
            'hide_links': True,
            'hide_object': True,
            'no_results_icon': icon_index,
            'no_results_main_link': link_index_template_create.resolve(
                context=RequestContext(request=self.request)
            ),
            'no_results_text': _(
                'This could mean that no index templates have been '
                'created or that there index templates '
                'but they are no properly defined.'
            ),
            'no_results_title': _('There are no index instances available.'),
            'title': _('Indexes'),
        }

    def get_source_queryset(self):
        queryset = IndexInstance.objects.filter(enabled=True)
        return queryset.filter(
            node_templates__index_instance_nodes__isnull=False
        ).distinct()


class IndexInstanceNodeView(DocumentListView):
    template_name = 'document_indexing/node_details.html'

    def dispatch(self, request, *args, **kwargs):
        self.index_instance_node = get_object_or_404(
            klass=IndexInstanceNode, pk=self.kwargs['index_instance_node_id']
        )

        AccessControlList.objects.check_access(
            obj=self.index_instance_node.index(),
            permissions=(permission_document_indexing_instance_view,),
            user=request.user
        )

        if self.index_instance_node:
            if self.index_instance_node.index_template_node.link_documents:
                return super(IndexInstanceNodeView, self).dispatch(
                    request, *args, **kwargs
                )

        return SingleObjectListView.dispatch(self, request, *args, **kwargs)

    def get_document_queryset(self):
        if self.index_instance_node:
            if self.index_instance_node.index_template_node.link_documents:
                return self.index_instance_node.documents.all()

    def get_extra_context(self):
        context = super(IndexInstanceNodeView, self).get_extra_context()
        context.update(
            {
                'column_class': 'col-xs-12 col-sm-6 col-md-4 col-lg-3',
                'object': self.index_instance_node,
                'navigation': mark_safe(
                    _('Navigation: %s') % node_tree(
                        node=self.index_instance_node, user=self.request.user
                    )
                ),
                'title': _(
                    'Contents for index: %s'
                ) % self.index_instance_node.get_full_path(),
            }
        )

        if self.index_instance_node and not self.index_instance_node.index_template_node.link_documents:
            context.update(
                {
                    'hide_object': True,
                    'list_as_items': False,
                }
            )

        return context

    def get_source_queryset(self):
        if self.index_instance_node:
            if self.index_instance_node.index_template_node.link_documents:
                return super(IndexInstanceNodeView, self).get_source_queryset()
            else:
                self.object_permission = None
                return self.index_instance_node.get_children().order_by(
                    'value'
                )
        else:
            self.object_permission = None
            return IndexInstanceNode.objects.none()


class DocumentIndexNodeListView(ExternalObjectMixin, SingleObjectListView):
    """
    Show a list of indexes where the current document can be found
    """
    external_object_class = Document
    external_object_permission = permission_document_view
    external_object_pk_url_kwarg = 'document_id'
    object_permission = permission_document_indexing_instance_view

    def get_extra_context(self):
        return {
            'hide_object': True,
            'no_results_icon': icon_index,
            'no_results_text': _(
                'Assign the document type of this document '
                'to an index to have it appear in instances of '
                'those indexes organization units. '
            ),
            'no_results_title': _(
                'This document is not in any index'
            ),
            'object': self.external_object,
            'title': _(
                'Indexes nodes containing document: %s'
            ) % self.external_object,
        }

    def get_source_queryset(self):
        return DocumentIndexInstanceNode.objects.get_for(
            document=self.external_object
        )


class IndexesRebuildView(FormView):
    extra_context = {
        'title': _('Rebuild indexes'),
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
                singular='%(count)d index queued for rebuild.',
                plural='%(count)d indexes queued for rebuild.',
                number=count
            ) % {
                'count': count,
            }, request=self.request
        )

        return super(IndexesRebuildView, self).form_valid(form=form)

    def get_form_extra_kwargs(self):
        return {
            'user': self.request.user
        }

    def get_post_action_redirect(self):
        return reverse(viewname='common:tools_list')


class IndexesResetView(FormView):
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

        return super(IndexesResetView, self).form_valid(form=form)

    def get_form_extra_kwargs(self):
        return {
            'help_text': _(
                'Index templates for which their instances will be deleted.'
            ),
            'user': self.request.user
        }

    def get_post_action_redirect(self):
        return reverse(viewname='common:tools_list')
