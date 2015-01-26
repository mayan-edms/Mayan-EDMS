from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from documents.permissions import PERMISSION_DOCUMENT_TYPE_EDIT

from .permissions import (
    PERMISSION_METADATA_DOCUMENT_ADD, PERMISSION_METADATA_DOCUMENT_EDIT,
    PERMISSION_METADATA_DOCUMENT_REMOVE, PERMISSION_METADATA_DOCUMENT_VIEW,
    PERMISSION_METADATA_TYPE_CREATE, PERMISSION_METADATA_TYPE_DELETE,
    PERMISSION_METADATA_TYPE_EDIT, PERMISSION_METADATA_TYPE_VIEW
)


metadata_edit = {'text': _('Edit metadata'), 'view': 'metadata:metadata_edit', 'args': 'object.pk', 'famfam': 'xhtml_go', 'permissions': [PERMISSION_METADATA_DOCUMENT_EDIT]}
metadata_view = {'text': _('Metadata'), 'view': 'metadata:metadata_view', 'args': 'object.pk', 'famfam': 'xhtml_go', 'permissions': [PERMISSION_METADATA_DOCUMENT_VIEW]}
metadata_multiple_edit = {'text': _('Edit metadata'), 'view': 'metadata:metadata_multiple_edit', 'famfam': 'xhtml_go', 'permissions': [PERMISSION_METADATA_DOCUMENT_EDIT]}
metadata_add = {'text': _('Add metadata'), 'view': 'metadata:metadata_add', 'args': 'object.pk', 'famfam': 'xhtml_add', 'permissions': [PERMISSION_METADATA_DOCUMENT_ADD]}
metadata_multiple_add = {'text': _('Add metadata'), 'view': 'metadata:metadata_multiple_add', 'famfam': 'xhtml_add', 'permissions': [PERMISSION_METADATA_DOCUMENT_ADD]}
metadata_remove = {'text': _('Remove metadata'), 'view': 'metadata:metadata_remove', 'args': 'object.pk', 'famfam': 'xhtml_delete', 'permissions': [PERMISSION_METADATA_DOCUMENT_REMOVE]}
metadata_multiple_remove = {'text': _('Remove metadata'), 'view': 'metadata:metadata_multiple_remove', 'famfam': 'xhtml_delete', 'permissions': [PERMISSION_METADATA_DOCUMENT_REMOVE]}

setup_document_type_metadata = {'text': _('Optional metadata'), 'view': 'metadata:setup_document_type_metadata', 'args': 'document_type.pk', 'famfam': 'xhtml', 'permissions': [PERMISSION_DOCUMENT_TYPE_EDIT]}
setup_document_type_metadata_required = {'text': _('Required metadata'), 'view': 'metadata:setup_document_type_metadata_required', 'args': 'document_type.pk', 'famfam': 'xhtml', 'permissions': [PERMISSION_DOCUMENT_TYPE_EDIT]}

setup_metadata_type_list = {'text': _('Metadata types'), 'view': 'metadata:setup_metadata_type_list', 'famfam': 'xhtml_go', 'icon': 'main/icons/xhtml.png', 'permissions': [PERMISSION_METADATA_TYPE_VIEW]}
setup_metadata_type_edit = {'text': _('Edit'), 'view': 'metadata:setup_metadata_type_edit', 'args': 'object.pk', 'famfam': 'xhtml', 'permissions': [PERMISSION_METADATA_TYPE_EDIT]}
setup_metadata_type_delete = {'text': _('Delete'), 'view': 'metadata:setup_metadata_type_delete', 'args': 'object.pk', 'famfam': 'xhtml_delete', 'permissions': [PERMISSION_METADATA_TYPE_DELETE]}
setup_metadata_type_create = {'text': _('Create new'), 'view': 'metadata:setup_metadata_type_create', 'famfam': 'xhtml_add', 'permissions': [PERMISSION_METADATA_TYPE_CREATE]}

link_documents_missing_required_metadata = {'text': _('Missing required metadata'), 'view': 'metadata:documents_missing_required_metadata', 'icon': 'main/icons/to_do_list.png'}
