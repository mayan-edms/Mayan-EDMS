from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .api_views import APISearchView
from .views import AdvancedSearchView, ResultsView, SearchView

urlpatterns = patterns(
    'dynamic_search.views',
    url(r'^$', SearchView.as_view(), name='search'),
    url(r'^advanced/$', AdvancedSearchView.as_view(), name='search_advanced'),
    url(r'^results/$', ResultsView.as_view(), name='results'),
)

api_urls = patterns(
    '',
    url(r'^search/$', APISearchView.as_view(), name='search-view'),
)
