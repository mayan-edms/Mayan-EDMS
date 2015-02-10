from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from acls.permissions import ACLS_VIEW_ACL
from documents.permissions import PERMISSION_DOCUMENT_VIEW

from .permissions import (
    PERMISSION_SMART_LINK_CREATE, PERMISSION_SMART_LINK_DELETE,
    PERMISSION_SMART_LINK_EDIT, PERMISSION_SMART_LINK_VIEW
)

smart_link_setup = {'text': _('Smart links'), 'view': 'linking:smart_link_list', 'icon': 'main/icons/link.png', 'permissions': [PERMISSION_SMART_LINK_CREATE]}
smart_link_list = {'text': _('Smart links'), 'view': 'linking:smart_link_list', 'famfam': 'link', 'permissions': [PERMISSION_SMART_LINK_CREATE]}
smart_link_create = {'text': _('Create new smart link'), 'view': 'linking:smart_link_create', 'famfam': 'link_add', 'permissions': [PERMISSION_SMART_LINK_CREATE]}
smart_link_edit = {'text': _('Edit'), 'view': 'linking:smart_link_edit', 'args': 'object.pk', 'famfam': 'link_edit', 'permissions': [PERMISSION_SMART_LINK_EDIT]}
smart_link_delete = {'text': _('Delete'), 'view': 'linking:smart_link_delete', 'args': 'object.pk', 'famfam': 'link_delete', 'permissions': [PERMISSION_SMART_LINK_DELETE]}
smart_link_document_types = {'text': _('Document types'), 'view': 'linking:smart_link_document_types', 'args': 'object.pk', 'famfam': 'layout', 'permissions': [PERMISSION_SMART_LINK_EDIT]}

smart_link_instances_for_document = {'text': _('Smart links'), 'view': 'linking:smart_link_instances_for_document', 'args': 'object.pk', 'famfam': 'page_link', 'permissions': [PERMISSION_DOCUMENT_VIEW]}
smart_link_instance_view = {'text': _('Documents'), 'view': 'linking:smart_link_instance_view', 'args': ['document.pk', 'object.smart_link.pk'], 'famfam': 'layout', 'page': [PERMISSION_SMART_LINK_VIEW]}

smart_link_condition_list = {'text': _('Conditions'), 'view': 'linking:smart_link_condition_list', 'args': 'object.pk', 'famfam': 'cog', 'permissions': [PERMISSION_SMART_LINK_EDIT]}
smart_link_condition_create = {'text': _('Create condition'), 'view': 'linking:smart_link_condition_create', 'args': 'object.pk', 'famfam': 'cog_add', 'permissions': [PERMISSION_SMART_LINK_EDIT]}
smart_link_condition_edit = {'text': _('Edit'), 'view': 'linking:smart_link_condition_edit', 'args': 'condition.pk', 'famfam': 'cog_edit', 'permissions': [PERMISSION_SMART_LINK_EDIT]}
smart_link_condition_delete = {'text': _('Delete'), 'view': 'linking:smart_link_condition_delete', 'args': 'condition.pk', 'famfam': 'cog_delete', 'permissions': [PERMISSION_SMART_LINK_EDIT]}

smart_link_acl_list = {'text': _('ACLs'), 'view': 'linking:smart_link_acl_list', 'args': 'object.pk', 'famfam': 'lock', 'permissions': [ACLS_VIEW_ACL]}
