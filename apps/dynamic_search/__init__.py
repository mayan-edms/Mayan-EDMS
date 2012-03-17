from django.utils.translation import ugettext_lazy as _

from navigation.api import register_sidebar_template, bind_links, Link

search = Link(text=_(u'search'), view='search', sprite='zoom')
search_advanced = Link(text=_(u'advanced search'), view='search_advanced', sprite='zoom_in')
search_again = Link(text=_(u'search again'), view='search_again', sprite='arrow_undo')

register_sidebar_template(['search', 'search_advanced'], 'search_help.html')

bind_links(['search', 'search_advanced', 'results'], [search, search_advanced], menu_name='form_header')
bind_links(['results'], [search_again], menu_name='sidebar')

register_sidebar_template(['search', 'search_advanced', 'results'], 'recent_searches.html')
