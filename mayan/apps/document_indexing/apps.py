from __future__ import absolute_import, unicode_literals

from kombu import Exchange, Queue

from django.db.models.signals import post_save, post_delete
from django.utils.translation import ugettext_lazy as _

from common import (
    MayanAppConfig, menu_facet, menu_main, menu_object, menu_secondary,
    menu_setup, menu_tools
)
from common.classes import Package
from common.widgets import two_state_template
from documents.models import Document
from documents.signals import post_document_created
from mayan.celery import app
from metadata.models import DocumentMetadata
from navigation import SourceColumn
from rest_api.classes import APIEndPoint

from .handlers import (
    document_created_index_update, document_index_delete,
    document_metadata_index_update, document_metadata_index_post_delete
)
from .links import (
    link_document_index_list, link_index_main_menu, link_index_setup,
    link_index_setup_create, link_index_setup_document_types,
    link_index_setup_delete, link_index_setup_edit, link_index_setup_list,
    link_index_setup_view, link_rebuild_index_instances,
    link_template_node_create, link_template_node_delete,
    link_template_node_edit
)
from .models import (
    DocumentIndexInstanceNode, Index, IndexInstance, IndexInstanceNode,
    IndexTemplateNode
)
from .widgets import get_breadcrumbs, index_instance_item_link, node_level


class DocumentIndexingApp(MayanAppConfig):
    app_namespace = 'indexing'
    app_url = 'indexing'
    name = 'document_indexing'
    test = True
    verbose_name = _('Document indexing')

    def ready(self):
        super(DocumentIndexingApp, self).ready()

        APIEndPoint(app=self, version_string='1')

        Package(label='Django MPTT', license_text='''
Django MPTT
-----------

Copyright (c) 2007, Jonathan Buchanan

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
        ''')

        Package(label='djangorestframework-recursive', license_text='''
Copyright (c) 2015, Warren Jin <jinwarren@gmail.com>

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
        ''')

        SourceColumn(source=Index, label=_('Label'), attribute='label')
        SourceColumn(source=Index, label=_('Slug'), attribute='slug')
        SourceColumn(
            source=Index, label=_('Enabled'),
            func=lambda context: two_state_template(context['object'].enabled)
        )

        SourceColumn(
            source=IndexInstance, label=_('Items'),
            func=lambda context: context['object'].get_items_count(
                user=context['request'].user
            )
        )
        SourceColumn(
            source=IndexInstance, label=_('Document types'),
            attribute='get_document_types_names'
        )

        SourceColumn(
            source=IndexTemplateNode, label=_('Level'),
            func=lambda context: node_level(context['object'])
        )
        SourceColumn(
            source=IndexTemplateNode, label=_('Enabled'),
            func=lambda context: two_state_template(context['object'].enabled)
        )
        SourceColumn(
            source=IndexTemplateNode, label=_('Has document links?'),
            func=lambda context: two_state_template(
                context['object'].link_documents
            )
        )

        SourceColumn(
            source=IndexInstanceNode, label=_('Node'),
            func=lambda context: index_instance_item_link(context['object'])
        )
        SourceColumn(
            source=IndexInstanceNode, label=_('Items'),
            func=lambda context: context['object'].get_item_count(
                user=context['request'].user
            )
        )

        SourceColumn(
            source=DocumentIndexInstanceNode, label=_('Node'),
            func=lambda context: get_breadcrumbs(
                index_instance_node=context['object'], single_link=True,
            )
        )
        SourceColumn(
            source=DocumentIndexInstanceNode, label=_('Items'),
            func=lambda context: context['object'].get_item_count(
                user=context['request'].user
            )
        )

        app.conf.CELERY_QUEUES.append(
            Queue('indexing', Exchange('indexing'), routing_key='indexing'),
        )

        app.conf.CELERY_ROUTES.update(
            {
                'document_indexing.tasks.task_delete_empty_index_nodes': {
                    'queue': 'indexing'
                },
                'document_indexing.tasks.task_index_document': {
                    'queue': 'indexing'
                },
                'document_indexing.tasks.task_do_rebuild_all_indexes': {
                    'queue': 'tools'
                },
            }
        )

        menu_facet.bind_links(
            links=(link_document_index_list,), sources=(Document,)
        )
        menu_object.bind_links(
            links=(
                link_index_setup_edit, link_index_setup_view,
                link_index_setup_document_types, link_index_setup_delete
            ), sources=(Index,)
        )
        menu_object.bind_links(
            links=(
                link_template_node_create, link_template_node_edit,
                link_template_node_delete
            ), sources=(IndexTemplateNode,)
        )
        menu_main.bind_links(links=(link_index_main_menu,))
        menu_secondary.bind_links(
            links=(link_index_setup_list, link_index_setup_create),
            sources=(
                Index, 'indexing:index_setup_list',
                'indexing:index_setup_create'
            )
        )
        menu_setup.bind_links(links=(link_index_setup,))
        menu_tools.bind_links(links=(link_rebuild_index_instances,))

        post_delete.connect(
            document_index_delete, dispatch_uid='document_index_delete',
            sender=Document
        )
        post_delete.connect(
            document_metadata_index_post_delete,
            dispatch_uid='document_metadata_index_post_delete',
            sender=DocumentMetadata
        )
        post_document_created.connect(
            document_created_index_update,
            dispatch_uid='document_created_index_update', sender=Document
        )
        post_save.connect(
            document_metadata_index_update,
            dispatch_uid='document_metadata_index_update',
            sender=DocumentMetadata
        )
