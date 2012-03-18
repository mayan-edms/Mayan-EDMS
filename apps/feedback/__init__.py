from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation.api import bind_links, Link
from common import about_view, license_view

form_view = Link(text=_('Feedback'), view='form_view', sprite='telephone')

bind_links(['form_view'], [about_view, license_view], menu_name='secondary_menu')
bind_links(['form_view', 'about_view', 'license_view'], [form_view], menu_name='secondary_menu')
