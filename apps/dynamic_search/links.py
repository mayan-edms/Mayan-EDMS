from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation import Link

from .icons import icon_search

menu_link = Link(text=_(u'search'), view='search', icon=icon_search, children_url_regex=[r'^search/'])
search = Link(text=_(u'search'), view='search', icon=icon_search)
#search_advanced = Link(text=_(u'advanced search'), view='search_advanced', sprite='zoom_in')
#search_again = Link(text=_(u'search again'), view='search_again', sprite='arrow_undo')
