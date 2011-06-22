from django.utils.translation import ugettext_lazy as _

from navigation.api import register_sidebar_template, register_links

search = {'text': _(u'search'), 'view': 'search', 'famfam': 'zoom'}
search_advanced = {'text': _(u'advanced search'), 'view': 'search_advanced', 'famfam': 'zoom_in'}

register_sidebar_template(['search', 'search_advanced'], 'search_help.html')

register_links(['search', 'search_advanced'], [search, search_advanced], menu_name='form_header')
