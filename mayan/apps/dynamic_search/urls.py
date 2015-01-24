from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .api_views import (
    APIRecentSearchListView, APIRecentSearchView, APISearchView
)

urlpatterns = patterns('dynamic_search.views',
    url(r'^$', 'search', (), 'search'),
    url(r'^advanced/$', 'search', {'advanced': True}, 'search_advanced'),
    url(r'^again/$', 'search_again', (), 'search_again'),
    url(r'^results/$', 'results', (), 'results'),
)

api_urls = patterns('',
    url(r'^recent_searches/$', APIRecentSearchListView.as_view(), name='recentsearch-list'),
    url(r'^recent_searches/(?P<pk>[0-9]+)/$', APIRecentSearchView.as_view(), name='recentsearch-detail'),
    url(r'^search/$', APISearchView.as_view(), name='search-view'),
)
