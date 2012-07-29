from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation.api import Link

from documents.permissions import PERMISSION_DOCUMENT_TYPE_EDIT

from .permissions import (PERMISSION_METADATA_DOCUMENT_EDIT,
    PERMISSION_METADATA_DOCUMENT_ADD, PERMISSION_METADATA_DOCUMENT_REMOVE,
    PERMISSION_METADATA_DOCUMENT_VIEW, PERMISSION_METADATA_TYPE_EDIT,
    PERMISSION_METADATA_TYPE_CREATE, PERMISSION_METADATA_TYPE_DELETE,
    PERMISSION_METADATA_TYPE_VIEW, PERMISSION_METADATA_SET_EDIT,
    PERMISSION_METADATA_SET_CREATE, PERMISSION_METADATA_SET_DELETE,
    PERMISSION_METADATA_SET_VIEW)

metadata_edit = Link(text=_(u'edit metadata'), view='metadata_edit', args='object.pk', sprite='xhtml_go', permissions=[PERMISSION_METADATA_DOCUMENT_EDIT])
metadata_view = Link(text=_(u'metadata'), view='metadata_view', args='object.pk', sprite='xhtml_go', permissions=[PERMISSION_METADATA_DOCUMENT_VIEW])  # children_view_regex=['metadata'])
metadata_multiple_edit = Link(text=_(u'edit metadata'), view='metadata_multiple_edit', sprite='xhtml_go', permissions=[PERMISSION_METADATA_DOCUMENT_EDIT])
metadata_add = Link(text=_(u'add metadata'), view='metadata_add', args='object.pk', sprite='xhtml_add', permissions=[PERMISSION_METADATA_DOCUMENT_ADD])
metadata_multiple_add = Link(text=_(u'add metadata'), view='metadata_multiple_add', sprite='xhtml_add', permissions=[PERMISSION_METADATA_DOCUMENT_ADD])
metadata_remove = Link(text=_(u'remove metadata'), view='metadata_remove', args='object.pk', sprite='xhtml_delete', permissions=[PERMISSION_METADATA_DOCUMENT_REMOVE])
metadata_multiple_remove = Link(text=_(u'remove metadata'), view='metadata_multiple_remove', sprite='xhtml_delete', permissions=[PERMISSION_METADATA_DOCUMENT_REMOVE])

setup_metadata_type_list = Link(text=_(u'metadata types'), view='setup_metadata_type_list', sprite='xhtml_go', icon='xhtml.png', permissions=[PERMISSION_METADATA_TYPE_VIEW])  # children_view_regex=[r'setup_metadata_type'])
setup_metadata_type_edit = Link(text=_(u'edit'), view='setup_metadata_type_edit', args='object.pk', sprite='xhtml', permissions=[PERMISSION_METADATA_TYPE_EDIT])
setup_metadata_type_delete = Link(text=_(u'delete'), view='setup_metadata_type_delete', args='object.pk', sprite='xhtml_delete', permissions=[PERMISSION_METADATA_TYPE_DELETE])
setup_metadata_type_create = Link(text=_(u'create new'), view='setup_metadata_type_create', sprite='xhtml_add', permissions=[PERMISSION_METADATA_TYPE_CREATE])

setup_metadata_set_list = Link(text=_(u'metadata sets'), view='setup_metadata_set_list', sprite='table', icon='table.png', permissions=[PERMISSION_METADATA_SET_VIEW])  # children_view_regex=[r'setup_metadata_set'])
setup_metadata_set_edit = Link(text=_(u'edit'), view='setup_metadata_set_edit', args='object.pk', sprite='table_edit', permissions=[PERMISSION_METADATA_SET_EDIT])
setup_metadata_set_delete = Link(text=_(u'delete'), view='setup_metadata_set_delete', args='object.pk', sprite='table_delete', permissions=[PERMISSION_METADATA_SET_DELETE])
setup_metadata_set_create = Link(text=_(u'create new'), view='setup_metadata_set_create', sprite='table_add', permissions=[PERMISSION_METADATA_SET_CREATE])
setup_metadata_set_members = Link(text=_(u'members'), view='setup_metadata_set_members', args='object.pk', sprite='table_refresh', permissions=[PERMISSION_METADATA_SET_EDIT])

setup_document_type_metadata = Link(text=_(u'default metadata'), view='setup_document_type_metadata', args='document_type.pk', sprite='xhtml', permissions=[PERMISSION_DOCUMENT_TYPE_EDIT])
