from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation.api import Link

from clustering.permissions import (PERMISSION_NODES_VIEW)


node_workers = Link(text=_(u'workers'), view='node_workers', args='object.pk', sprite='lorry_go', permissions=[PERMISSION_NODES_VIEW])
#index_setup_create = Link(text=_(u'create index'), view='index_setup_create', sprite='tab_add', permissions=[PERMISSION_DOCUMENT_INDEXING_CREATE])
#index_setup_edit = Link(text=_(u'edit'), view='index_setup_edit', args='index.pk', sprite='tab_edit', permissions=[PERMISSION_DOCUMENT_INDEXING_EDIT])
#index_setup_delete = Link(text=_(u'delete'), view='index_setup_delete', args='index.pk', sprite='tab_delete', permissions=[PERMISSION_DOCUMENT_INDEXING_DELETE])
#index_setup_view = Link(text=_(u'tree template'), view='index_setup_view', args='index.pk', sprite='textfield', permissions=[PERMISSION_DOCUMENT_INDEXING_SETUP])
#index_setup_document_types = Link(text=_(u'document types'), view='index_setup_document_types', args='index.pk', sprite='layout', permissions=[PERMISSION_DOCUMENT_INDEXING_EDIT])  # children_view_regex=[r'^index_setup', r'^template_node'])
