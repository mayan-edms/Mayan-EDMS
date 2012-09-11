from __future__ import absolute_import

import datetime

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

default_available_functions = {
    'current_date': datetime.datetime.now().date,
}

default_available_models = {
    'User': User
}

#from .icons import icon_history_list
#from .links import history_list

label = _(u'Metadata')
#description = _(u'Handles the events registration and event logging.')
dependencies = ['app_registry', 'icons', 'navigation', 'documents', 'permissions', 'acls', 'common']
#icon = icon_history_list
#tool_links = [history_list]
"""
   app.add_setting(
        name=u'AVAILABLE_FUNCTIONS',
        default=default_available_functions,
    )

    app.add_setting(
        name=u'AVAILABLE_MODELS',
        default=default_available_models,
    )
"""
