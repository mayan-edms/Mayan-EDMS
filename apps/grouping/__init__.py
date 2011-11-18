from django.utils.translation import ugettext_lazy as _

from navigation.api import register_links
from permissions.api import register_permission, set_namespace_title
from project_setup.api import register_setup
from documents.literals import PERMISSION_DOCUMENT_VIEW
from documents.models import Document

from grouping.models import DocumentGroup


PERMISSION_DOCUMENT_GROUP_VIEW = {'namespace': 'grouping', 'name': 'group_view', 'label': _(u'View existing document groups')}
PERMISSION_DOCUMENT_GROUP_CREATE = {'namespace': 'grouping', 'name': 'group_create', 'label': _(u'Create new document groups')}
PERMISSION_DOCUMENT_GROUP_DELETE = {'namespace': 'grouping', 'name': 'group_delete', 'label': _(u'Delete document groups')}

set_namespace_title('grouping', _(u'Grouping'))
register_permission(PERMISSION_DOCUMENT_GROUP_VIEW)
register_permission(PERMISSION_DOCUMENT_GROUP_CREATE)
register_permission(PERMISSION_DOCUMENT_GROUP_DELETE)

document_group_link = {'text': _(u'group actions'), 'view': 'document_group_view', 'famfam': 'package_go', 'permissions': [PERMISSION_DOCUMENT_VIEW]}
groups_for_document = {'text': _(u'groups'), 'view': 'groups_for_document', 'args': 'object.pk', 'famfam': 'package_go', 'permissions': [PERMISSION_DOCUMENT_VIEW]}

document_groups_setup = {'text': _(u'document groups'), 'view': 'document_group_list', 'icon': 'package.png', 'permissions': [PERMISSION_DOCUMENT_GROUP_VIEW]}
document_group_list = {'text': _(u'document groups'), 'view': 'document_group_list', 'famfam': 'package', 'permissions': [PERMISSION_DOCUMENT_GROUP_VIEW]}
document_group_create = {'text': _(u'create new'), 'view': 'document_group_create', 'famfam': 'package_add', 'permissions': [PERMISSION_DOCUMENT_GROUP_CREATE]}
document_group_delete = {'text': _(u'delete'), 'view': 'document_group_delete', 'args': 'object.pk', 'famfam': 'package_delete', 'permissions': [PERMISSION_DOCUMENT_GROUP_DELETE]}

register_links(Document, [groups_for_document], menu_name='form_header')

register_links(DocumentGroup, [document_group_delete])
register_links(['document_group_list', 'document_group_create', 'document_group_delete'], [document_group_list, document_group_create], menu_name='sidebar')

register_setup(document_groups_setup)
