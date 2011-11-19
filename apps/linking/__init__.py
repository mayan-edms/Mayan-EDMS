from django.utils.translation import ugettext_lazy as _

from navigation.api import register_links, register_sidebar_template
from permissions.api import register_permission, set_namespace_title
from project_setup.api import register_setup
from documents.literals import PERMISSION_DOCUMENT_VIEW
from documents.models import Document

from linking.models import SmartLink, SmartLinkCondition

PERMISSION_SMART_LINK_VIEW = {'namespace': 'linking', 'name': 'group_view', 'label': _(u'View existing smart links')}
PERMISSION_SMART_LINK_CREATE = {'namespace': 'linking', 'name': 'group_create', 'label': _(u'Create new smart links')}
PERMISSION_SMART_LINK_DELETE = {'namespace': 'linking', 'name': 'group_delete', 'label': _(u'Delete smart links')}
PERMISSION_SMART_LINK_EDIT = {'namespace': 'linking', 'name': 'group_edit', 'label': _(u'Edit smart links')}

set_namespace_title('linking', _(u'Smart links'))
register_permission(PERMISSION_SMART_LINK_VIEW)
register_permission(PERMISSION_SMART_LINK_CREATE)
register_permission(PERMISSION_SMART_LINK_DELETE)
register_permission(PERMISSION_SMART_LINK_EDIT)

smart_link_instance_view_link = {'text': _(u'smart links actions'), 'view': 'smart_link_instance_view', 'famfam': 'page_link', 'permissions': [PERMISSION_DOCUMENT_VIEW]}
smart_link_instances_for_document = {'text': _(u'smart links'), 'view': 'smart_link_instances_for_document', 'args': 'object.pk', 'famfam': 'page_link', 'permissions': [PERMISSION_DOCUMENT_VIEW]}

document_groups_setup = {'text': _(u'smart links'), 'view': 'document_group_list', 'icon': 'link.png', 'permissions': [PERMISSION_SMART_LINK_CREATE]}
document_group_list = {'text': _(u'smart links list'), 'view': 'document_group_list', 'famfam': 'link', 'permissions': [PERMISSION_SMART_LINK_CREATE]}
document_group_create = {'text': _(u'create new smart link'), 'view': 'document_group_create', 'famfam': 'link_add', 'permissions': [PERMISSION_SMART_LINK_CREATE]}
document_group_edit = {'text': _(u'edit'), 'view': 'document_group_edit', 'args': 'smart_link.pk', 'famfam': 'link_edit', 'permissions': [PERMISSION_SMART_LINK_EDIT]}
document_group_delete = {'text': _(u'delete'), 'view': 'document_group_delete', 'args': 'smart_link.pk', 'famfam': 'link_delete', 'permissions': [PERMISSION_SMART_LINK_DELETE]}

smart_link_condition_list = {'text': _(u'conditions'), 'view': 'smart_link_condition_list', 'args': 'smart_link.pk', 'famfam': 'cog', 'permissions': [PERMISSION_SMART_LINK_CREATE, PERMISSION_SMART_LINK_CREATE]}
smart_link_condition_create = {'text': _(u'create condition'), 'view': 'smart_link_condition_create', 'args': 'smart_link.pk', 'famfam': 'cog_add', 'permissions': [PERMISSION_SMART_LINK_CREATE, PERMISSION_SMART_LINK_EDIT]}
smart_link_condition_edit = {'text': _(u'edit'), 'view': 'smart_link_condition_edit', 'args': 'condition.pk', 'famfam': 'cog_edit', 'permissions': [PERMISSION_SMART_LINK_CREATE, PERMISSION_SMART_LINK_EDIT]}
smart_link_condition_delete = {'text': _(u'delete'), 'view': 'smart_link_condition_delete', 'args': 'condition.pk', 'famfam': 'cog_delete', 'permissions': [PERMISSION_SMART_LINK_CREATE, PERMISSION_SMART_LINK_EDIT]}

register_links(Document, [smart_link_instances_for_document], menu_name='form_header')

register_links(SmartLink, [document_group_edit, document_group_delete, smart_link_condition_list])
register_links(SmartLinkCondition, [smart_link_condition_edit, smart_link_condition_delete])
register_links(['document_group_list', 'document_group_create', 'document_group_edit', 'document_group_delete', 'smart_link_condition_list', 'smart_link_condition_create', 'smart_link_condition_edit', 'smart_link_condition_delete'], [document_group_list, document_group_create], menu_name='sidebar')
register_links(['smart_link_condition_list', 'smart_link_condition_create', 'smart_link_condition_edit', 'smart_link_condition_delete'], [smart_link_condition_create], menu_name='sidebar')

register_setup(document_groups_setup)
register_sidebar_template(['document_group_list'], 'smart_links_help.html')
