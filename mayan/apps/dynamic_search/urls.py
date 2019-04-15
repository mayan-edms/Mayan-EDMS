from __future__ import unicode_literals

from django.conf.urls import url

from .api_views import (
    APIAdvancedSearchView, APISearchModelList, APISearchView
)
from .views import (
    AdvancedSearchView, ResultsView, SearchAgainView, SearchView
)

urlpatterns = [
    url(
        regex=r'^(?P<search_model>[\.\w]+)/$', view=SearchView.as_view(),
        name='search'
    ),
    url(
        regex=r'^advanced/(?P<search_model>[\.\w]+)/$',
        view=AdvancedSearchView.as_view(), name='search_advanced'
    ),
    url(
        regex=r'^again/(?P<search_model>[\.\w]+)/$',
        view=SearchAgainView.as_view(), name='search_again'
    ),
    url(
        regex=r'^results/(?P<search_model>[\.\w]+)/$',
        view=ResultsView.as_view(), name='results'
    ),
]

api_urls = [
    url(
        regex=r'^search_models/$', view=APISearchModelList.as_view(),
        name='searchmodel-list'
    ),
    url(
        regex=r'^search/(?P<search_model>[\.\w]+)/$',
        view=APISearchView.as_view(), name='search-view'
    ),
    url(
        regex=r'^search/advanced/(?P<search_model>[\.\w]+)/$',
        view=APIAdvancedSearchView.as_view(), name='advanced-search-view'
    ),
]
