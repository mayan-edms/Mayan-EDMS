from __future__ import unicode_literals

from django.apps import apps
from django.utils.translation import ugettext_lazy as _

from acls import ModelPermission
from acls.links import link_acl_list
from acls.permissions import permission_acl_edit, permission_acl_view
from common import (
    MayanAppConfig, menu_facet, menu_secondary, menu_object, menu_main,
    menu_multi_item, menu_sidebar
)
from documents.search import document_search
from navigation import SourceColumn
from rest_api.classes import APIEndPoint

from .links import (
    link_multiple_documents_attach_tag, link_multiple_documents_tag_remove,
    link_single_document_multiple_tag_remove, link_tag_attach, link_tag_create,
    link_tag_delete, link_tag_document_list, link_tag_edit, link_tag_list,
    link_tag_multiple_delete, link_tag_tagged_item_list
)
from .permissions import (
    permission_tag_attach, permission_tag_delete, permission_tag_edit,
    permission_tag_remove, permission_tag_view
)
from .widgets import widget_document_tags, widget_single_tag


class TagsApp(MayanAppConfig):
    name = 'tags'
    test = True
    verbose_name = _('Tags')

    def ready(self):
        super(TagsApp, self).ready()

        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )

        DocumentTag = self.get_model('DocumentTag')
        Tag = self.get_model('Tag')

        APIEndPoint(app=self, version_string='1')

        Document.add_to_class(
            'attached_tags',
            lambda document: DocumentTag.objects.filter(documents=document)
        )

        ModelPermission.register(
            model=Document, permissions=(
                permission_tag_attach, permission_tag_remove,
                permission_tag_view
            )
        )

        ModelPermission.register(
            model=Tag, permissions=(
                permission_acl_edit, permission_acl_view,
                permission_tag_delete, permission_tag_edit,
                permission_tag_view,
            )
        )

        SourceColumn(
            source=DocumentTag, label=_('Preview'),
            func=lambda context: widget_single_tag(context['object'])
        )

        SourceColumn(
            source=Document, label=_('Tags'),
            func=lambda context: widget_document_tags(
                document=context['object'], user=context['request'].user
            )
        )

        SourceColumn(
            source=Tag, label=_('Preview'),
            func=lambda context: widget_single_tag(context['object'])
        )
        SourceColumn(
            source=Tag, label=_('Documents'),
            func=lambda context: context['object'].get_document_count(
                user=context['request'].user
            )
        )

        document_search.add_model_field(field='tags__label', label=_('Tags'))

        menu_facet.bind_links(
            links=(link_tag_document_list,), sources=(Document,)
        )
        menu_main.bind_links(links=(link_tag_list,))
        menu_multi_item.bind_links(
            links=(
                link_multiple_documents_attach_tag,
                link_multiple_documents_tag_remove
            ),
            sources=(Document,)
        )
        menu_multi_item.bind_links(
            links=(link_tag_multiple_delete,), sources=(Tag,)
        )
        menu_multi_item.bind_links(
            links=(link_single_document_multiple_tag_remove,),
            sources=(DocumentTag,)
        )
        menu_object.bind_links(
            links=(
                link_tag_tagged_item_list, link_tag_edit, link_acl_list,
                link_tag_delete
            ),
            sources=(Tag,)
        )
        menu_secondary.bind_links(
            links=(link_tag_list, link_tag_create),
            sources=(Tag, 'tags:tag_list', 'tags:tag_create')
        )
        menu_sidebar.bind_links(
            links=(link_tag_attach,),
            sources=(
                'tags:document_tags', 'tags:tag_remove',
                'tags:tag_multiple_remove', 'tags:tag_attach'
            )
        )
