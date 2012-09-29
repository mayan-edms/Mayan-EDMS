from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation import Link

from documents.permissions import PERMISSION_DOCUMENT_TYPE_EDIT

from .permissions import (PERMISSION_METADATA_DOCUMENT_EDIT,
    PERMISSION_METADATA_DOCUMENT_ADD, PERMISSION_METADATA_DOCUMENT_REMOVE,
    PERMISSION_METADATA_DOCUMENT_VIEW, PERMISSION_METADATA_TYPE_EDIT,
    PERMISSION_METADATA_TYPE_CREATE, PERMISSION_METADATA_TYPE_DELETE,
    PERMISSION_METADATA_TYPE_VIEW, PERMISSION_METADATA_SET_EDIT,
    PERMISSION_METADATA_SET_CREATE, PERMISSION_METADATA_SET_DELETE,
    PERMISSION_METADATA_SET_VIEW)
from .icons import (icon_metadata_view, icon_metadata_edit, icon_metadata_add,
    icon_metadata_remove, icon_metadata_sets, icon_metadata_set_create,
    icon_metadata_set_edit, icon_metadata_set_delete, icon_metadata_set_members)

metadata_view = Link(text=_(u'metadata'), view='metadata_view', args='object.pk', icon=icon_metadata_view, permissions=[PERMISSION_METADATA_DOCUMENT_VIEW])  # children_view_regex=['metadata'])
metadata_edit = Link(text=_(u'edit metadata'), view='metadata_edit', args='object.pk', icon=icon_metadata_edit, permissions=[PERMISSION_METADATA_DOCUMENT_EDIT])
metadata_multiple_edit = Link(text=_(u'edit metadata'), view='metadata_multiple_edit', icon=icon_metadata_edit, permissions=[PERMISSION_METADATA_DOCUMENT_EDIT])
metadata_add = Link(text=_(u'add metadata'), view='metadata_add', args='object.pk', icon=icon_metadata_add, permissions=[PERMISSION_METADATA_DOCUMENT_ADD])
metadata_multiple_add = Link(text=_(u'add metadata'), view='metadata_multiple_add', icon=icon_metadata_add, permissions=[PERMISSION_METADATA_DOCUMENT_ADD])
metadata_remove = Link(text=_(u'remove metadata'), view='metadata_remove', args='object.pk', icon=icon_metadata_remove, permissions=[PERMISSION_METADATA_DOCUMENT_REMOVE])
metadata_multiple_remove = Link(text=_(u'remove metadata'), view='metadata_multiple_remove', icon=icon_metadata_remove, permissions=[PERMISSION_METADATA_DOCUMENT_REMOVE])

setup_metadata_type_list = Link(text=_(u'metadata types'), view='setup_metadata_type_list', icon=icon_metadata_view, permissions=[PERMISSION_METADATA_TYPE_VIEW])  # children_view_regex=[r'setup_metadata_type'])
setup_metadata_type_edit = Link(text=_(u'edit'), view='setup_metadata_type_edit', args='object.pk', icon=icon_metadata_edit, permissions=[PERMISSION_METADATA_TYPE_EDIT])
setup_metadata_type_delete = Link(text=_(u'delete'), view='setup_metadata_type_delete', args='object.pk', icon=icon_metadata_remove, permissions=[PERMISSION_METADATA_TYPE_DELETE])
setup_metadata_type_create = Link(text=_(u'create new'), view='setup_metadata_type_create', icon=icon_metadata_add, permissions=[PERMISSION_METADATA_TYPE_CREATE])

setup_metadata_set_list = Link(text=_(u'metadata sets'), view='setup_metadata_set_list', icon=icon_metadata_sets, permissions=[PERMISSION_METADATA_SET_VIEW])  # children_view_regex=[r'setup_metadata_set'])
setup_metadata_set_edit = Link(text=_(u'edit'), view='setup_metadata_set_edit', args='object.pk', icon=icon_metadata_set_edit, permissions=[PERMISSION_METADATA_SET_EDIT])
setup_metadata_set_delete = Link(text=_(u'delete'), view='setup_metadata_set_delete', args='object.pk', icon=icon_metadata_set_delete, permissions=[PERMISSION_METADATA_SET_DELETE])
setup_metadata_set_create = Link(text=_(u'create new'), view='setup_metadata_set_create', icon=icon_metadata_set_create, permissions=[PERMISSION_METADATA_SET_CREATE])
setup_metadata_set_members = Link(text=_(u'members'), view='setup_metadata_set_members', args='object.pk', icon=icon_metadata_set_members, permissions=[PERMISSION_METADATA_SET_EDIT])

setup_document_type_metadata = Link(text=_(u'default metadata'), view='setup_document_type_metadata', args='document_type.pk', icon=icon_metadata_view, permissions=[PERMISSION_DOCUMENT_TYPE_EDIT])
