from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from documents.permissions import PERMISSION_DOCUMENT_TYPE_EDIT

from .permissions import (PERMISSION_METADATA_DOCUMENT_EDIT,
    PERMISSION_METADATA_DOCUMENT_ADD, PERMISSION_METADATA_DOCUMENT_REMOVE,
    PERMISSION_METADATA_DOCUMENT_VIEW, PERMISSION_METADATA_TYPE_EDIT,
    PERMISSION_METADATA_TYPE_CREATE, PERMISSION_METADATA_TYPE_DELETE,
    PERMISSION_METADATA_TYPE_VIEW, PERMISSION_METADATA_SET_EDIT,
    PERMISSION_METADATA_SET_CREATE, PERMISSION_METADATA_SET_DELETE,
    PERMISSION_METADATA_SET_VIEW)

metadata_edit = {'text': _(u'edit metadata'), 'view': 'metadata_edit', 'args': 'object.pk', 'famfam': 'xhtml_go', 'permissions': [PERMISSION_METADATA_DOCUMENT_EDIT]}
metadata_view = {'text': _(u'metadata'), 'view': 'metadata_view', 'args': 'object.pk', 'famfam': 'xhtml_go', 'permissions': [PERMISSION_METADATA_DOCUMENT_VIEW], 'children_view_regex': ['metadata']}
metadata_multiple_edit = {'text': _(u'edit metadata'), 'view': 'metadata_multiple_edit', 'famfam': 'xhtml_go', 'permissions': [PERMISSION_METADATA_DOCUMENT_EDIT]}
metadata_add = {'text': _(u'add metadata'), 'view': 'metadata_add', 'args': 'object.pk', 'famfam': 'xhtml_add', 'permissions': [PERMISSION_METADATA_DOCUMENT_ADD]}
metadata_multiple_add = {'text': _(u'add metadata'), 'view': 'metadata_multiple_add', 'famfam': 'xhtml_add', 'permissions': [PERMISSION_METADATA_DOCUMENT_ADD]}
metadata_remove = {'text': _(u'remove metadata'), 'view': 'metadata_remove', 'args': 'object.pk', 'famfam': 'xhtml_delete', 'permissions': [PERMISSION_METADATA_DOCUMENT_REMOVE]}
metadata_multiple_remove = {'text': _(u'remove metadata'), 'view': 'metadata_multiple_remove', 'famfam': 'xhtml_delete', 'permissions': [PERMISSION_METADATA_DOCUMENT_REMOVE]}

setup_metadata_type_list = {'text': _(u'metadata types'), 'view': 'setup_metadata_type_list', 'famfam': 'xhtml_go', 'icon': 'xhtml.png', 'permissions': [PERMISSION_METADATA_TYPE_VIEW]}
setup_metadata_type_edit = {'text': _(u'edit'), 'view': 'setup_metadata_type_edit', 'args': 'object.pk', 'famfam': 'xhtml', 'permissions': [PERMISSION_METADATA_TYPE_EDIT]}
setup_metadata_type_delete = {'text': _(u'delete'), 'view': 'setup_metadata_type_delete', 'args': 'object.pk', 'famfam': 'xhtml_delete', 'permissions': [PERMISSION_METADATA_TYPE_DELETE]}
setup_metadata_type_create = {'text': _(u'create new'), 'view': 'setup_metadata_type_create', 'famfam': 'xhtml_add', 'permissions': [PERMISSION_METADATA_TYPE_CREATE]}

setup_metadata_set_list = {'text': _(u'metadata sets'), 'view': 'setup_metadata_set_list', 'famfam': 'table', 'icon': 'table.png', 'permissions': [PERMISSION_METADATA_SET_VIEW]}
setup_metadata_set_edit = {'text': _(u'edit'), 'view': 'setup_metadata_set_edit', 'args': 'object.pk', 'famfam': 'table_edit', 'permissions': [PERMISSION_METADATA_SET_EDIT]}
setup_metadata_set_members = {'text': _(u'members'), 'view': 'setup_metadata_set_members', 'args': 'object.pk', 'famfam': 'table_link', 'permissions': [PERMISSION_METADATA_SET_EDIT]}
setup_metadata_set_delete = {'text': _(u'delete'), 'view': 'setup_metadata_set_delete', 'args': 'object.pk', 'famfam': 'table_delete', 'permissions': [PERMISSION_METADATA_SET_DELETE]}
setup_metadata_set_create = {'text': _(u'create new'), 'view': 'setup_metadata_set_create', 'famfam': 'table_add', 'permissions': [PERMISSION_METADATA_SET_CREATE]}

setup_document_type_metadata = {'text': _(u'default metadata'), 'view': 'setup_document_type_metadata', 'args': 'document_type.pk', 'famfam': 'xhtml', 'permissions': [PERMISSION_DOCUMENT_TYPE_EDIT]}
