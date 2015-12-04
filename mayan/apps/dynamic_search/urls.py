from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .api_views import (
    APIRecentSearchListView, APIRecentSearchView, APISearchView
)
from .views import AdvancedSearchView, ResultsView, SearchView

urlpatterns = patterns(
    'dynamic_search.views',
    url(r'^$', SearchView.as_view(), name='search'),
    url(r'^advanced/$', AdvancedSearchView.as_view(), name='search_advanced'),
    url(r'^again/$', 'search_again', name='search_again'),
    url(r'^results/$', ResultsView.as_view(), name='results'),
)

api_urls = patterns(
    '',
    url(
        r'^recent_searches/$', APIRecentSearchListView.as_view(),
        name='recentsearch-list'
    ),
    url(
        r'^recent_searches/(?P<pk>[0-9]+)/$', APIRecentSearchView.as_view(),
        name='recentsearch-detail'
    ),
    url(r'^search/$', APISearchView.as_view(), name='search-view'),
)
