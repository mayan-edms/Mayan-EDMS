from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .api_views import (
    APIRecentSearchListView, APIRecentSearchView, APISearchView
)
from .views import (
    AdvancedSearchView, ResultsView, SearchAgainView, SearchView
)

urlpatterns = patterns(
    'dynamic_search.views',
    url(r'^(?P<search_model>[\.\w]+)/$', SearchView.as_view(), name='search'),
    url(
        r'^advanced/(?P<search_model>[\.\w]+)/$', AdvancedSearchView.as_view(),
        name='search_advanced'
    ),
    url(
        r'^again/(?P<search_model>[\.\w]+)/$', SearchAgainView.as_view(),
        name='search_again'
    ),
    url(
        r'^results/(?P<search_model>[\.\w]+)/$', ResultsView.as_view(),
        name='results'
    ),
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
