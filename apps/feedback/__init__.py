from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation.api import (register_links, register_top_menu,
    register_multi_item_links, register_sidebar_template)
from common import about_view, license_view

form_view = {'text': _('Feedback'), 'view': 'form_view', 'famfam': 'telephone'}

register_links(['form_view'], [about_view, license_view], menu_name='secondary_menu')
register_links(['form_view', 'about_view', 'license_view'], [form_view], menu_name='secondary_menu')
