from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation.api import register_links, register_multi_item_links
from project_setup.api import register_setup

from .permissions import PERMISSION_WORKFLOW_SETUP_VIEW

setup_workflow_link = {'text': _(u'workflows'), 'view': 'setup_workflow_list', 'icon': 'chart_organisation.png', 'permissions': [PERMISSION_WORKFLOW_SETUP_VIEW]}

setup_workflow_list_link = {'text': _(u'workflow list'), 'view': 'setup_workflow_list', 'famfam': 'chart_organisation', 'permissions': [PERMISSION_WORKFLOW_SETUP_VIEW]}

#register_links(User, [user_edit, user_set_password, user_delete])
register_links(['setup_workflow_list'], [setup_workflow_link], menu_name=u'secondary_menu')
#register_multi_item_links(['user_list'], [user_multiple_set_password, user_multiple_delete])


register_setup(setup_workflow_link)
