from __future__ import absolute_import, unicode_literals

from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.urls import reverse, reverse_lazy
from django.utils.html import mark_safe
from django.utils.translation import ugettext_lazy as _, ungettext

from mayan.apps.acls.models import AccessControlList
from mayan.apps.common.generics import (
    AddRemoveView, FormView, SingleObjectCreateView, SingleObjectDeleteView,
    SingleObjectEditView, SingleObjectListView
)
from mayan.apps.documents.events import event_document_type_edited
from mayan.apps.documents.models import Document, DocumentType
from mayan.apps.documents.permissions import (
    permission_document_type_edit, permission_document_view
)
from mayan.apps.documents.views import DocumentListView

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
    permission_document_indexing_view
)
from .tasks import task_rebuild_index


class DocumentTypeIndexesView(AddRemoveView):
    main_object_permission = permission_document_indexing_edit
    main_object_model = DocumentType
    main_object_pk_url_kwarg = 'pk'
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
    post_action_redirect = reverse_lazy(
        viewname='indexing:index_setup_list'
    )

    def get_extra_context(self):
        return {
            'object': self.get_object(),
            'title': _('Delete the index: %s?') % self.get_object(),
        }


class SetupIndexEditView(SingleObjectEditView):
    fields = ('label', 'slug', 'enabled')
    model = Index
    object_permission = permission_document_indexing_edit
    post_action_redirect = reverse_lazy(
        viewname='indexing:index_setup_list'
    )

    def get_extra_context(self):
        return {
            'object': self.get_object(),
            'title': _('Edit index: %s') % self.get_object(),
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


class SetupIndexDocumentTypesView(AddRemoveView):
    main_object_method_add = 'document_types_add'
    main_object_method_remove = 'document_types_remove'
    main_object_permission = permission_document_indexing_edit
    main_object_model = Index
    main_object_pk_url_kwarg = 'pk'
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


class SetupIndexTreeTemplateListView(SingleObjectListView):
    object_permission = permission_document_indexing_edit

    def get_extra_context(self):
        return {
            'hide_object': True,
            'index': self.get_index(),
            'navigation_object_list': ('index',),
            'title': _('Tree template nodes for index: %s') % self.get_index(),
        }

    def get_index(self):
        return get_object_or_404(klass=Index, pk=self.kwargs['pk'])

    def get_source_queryset(self):
        return self.get_index().template_root.get_descendants(
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
        return get_object_or_404(klass=IndexTemplateNode, pk=self.kwargs['pk'])


class TemplateNodeDeleteView(SingleObjectDeleteView):
    model = IndexTemplateNode
    object_permission = permission_document_indexing_edit

    def get_extra_context(self):
        return {
            'index': self.get_object().index,
            'navigation_object_list': ('index', 'node'),
            'node': self.get_object(),
            'title': _(
                'Delete the index template node: %s?'
            ) % self.get_object(),
        }

    def get_post_action_redirect(self):
        return reverse(
            viewname='indexing:index_setup_view', kwargs={
                'pk': self.get_object().index.pk
            }
        )


class TemplateNodeEditView(SingleObjectEditView):
    form_class = IndexTemplateNodeForm
    model = IndexTemplateNode
    object_permission = permission_document_indexing_edit

    def get_extra_context(self):
        return {
            'index': self.get_object().index,
            'navigation_object_list': ('index', 'node'),
            'node': self.get_object(),
            'title': _(
                'Edit the index template node: %s?'
            ) % self.get_object(),
        }

    def get_post_action_redirect(self):
        return reverse(
            viewname='indexing:index_setup_view', kwargs={
                'pk': self.get_object().index.pk
            }
        )


class IndexListView(SingleObjectListView):
    object_permission = permission_document_indexing_instance_view

    def get_extra_context(self):
        return {
            'hide_links': True,
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
            klass=IndexInstanceNode, pk=self.kwargs['pk']
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


class DocumentIndexNodeListView(SingleObjectListView):
    """
    Show a list of indexes where the current document can be found
    """
    object_permission = permission_document_indexing_instance_view

    def dispatch(self, request, *args, **kwargs):
        AccessControlList.objects.check_access(
            obj=self.get_document(), permissions=(permission_document_view,),
            user=request.user
        )

        return super(
            DocumentIndexNodeListView, self
        ).dispatch(request, *args, **kwargs)

    def get_document(self):
        return get_object_or_404(klass=Document, pk=self.kwargs['pk'])

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
            'object': self.get_document(),
            'title': _(
                'Indexes nodes containing document: %s'
            ) % self.get_document(),
        }

    def get_source_queryset(self):
        return DocumentIndexInstanceNode.objects.get_for(
            document=self.get_document()
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
