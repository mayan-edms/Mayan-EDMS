from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation.api import register_links, register_multi_item_links
from project_setup.api import register_setup

from .permissions import (PERMISSION_WORKFLOW_SETUP_VIEW,
    PERMISSION_WORKFLOW_SETUP_CREATE, PERMISSION_WORKFLOW_SETUP_EDIT,
    PERMISSION_WORKFLOW_SETUP_DELETE)
from .models import Workflow

setup_workflow_link = {'text': _(u'workflows'), 'view': 'setup_workflow_list', 'icon': 'chart_organisation.png', 'permissions': [PERMISSION_WORKFLOW_SETUP_VIEW]}

setup_workflow_list_link = {'text': _(u'workflow list'), 'view': 'setup_workflow_list', 'famfam': 'chart_organisation', 'permissions': [PERMISSION_WORKFLOW_SETUP_VIEW]}
setup_workflow_create_link = {'text': _(u'create new'), 'view': 'setup_workflow_create', 'famfam': 'chart_organisation_add', 'permissions': [PERMISSION_WORKFLOW_SETUP_CREATE]}
setup_workflow_edit_link = {'text': _(u'edit'), 'view': 'setup_workflow_edit', 'args': 'object.pk', 'famfam': 'chart_organisation', 'permissions': [PERMISSION_WORKFLOW_SETUP_EDIT]}
setup_workflow_delete_link = {'text': _(u'delete'), 'view': 'setup_workflow_delete', 'args': 'object.pk', 'famfam': 'chart_organisation_delete', 'permissions': [PERMISSION_WORKFLOW_SETUP_DELETE]}

register_links(Workflow, [setup_workflow_edit_link, setup_workflow_delete_link])
register_links([Workflow, 'setup_workflow_list', 'setup_workflow_create'], [setup_workflow_list_link], menu_name=u'form_header')
register_links([Workflow, 'setup_workflow_list', 'setup_workflow_create'], [setup_workflow_create_link], menu_name=u'secondary_menu')
#register_multi_item_links(['user_list'], [user_multiple_set_password, user_multiple_delete])

register_setup(setup_workflow_link)
