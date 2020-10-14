from django.conf.urls import url

from .api_views import (
    APIAdvancedSearchView, APISearchModelList, APISearchView
)
from .views import (
    AdvancedSearchView, ResultsView, SearchAgainView,
    SearchBackendReindexView, SearchView
)

urlpatterns_search = [
    url(
        regex=r'^again/(?P<search_model_name>[\.\w]+)/$', name='search_again',
        view=SearchAgainView.as_view()
    ),
    url(
        regex=r'^advanced/(?P<search_model_name>[\.\w]+)/$',
        name='search_advanced', view=AdvancedSearchView.as_view()
    ),
    url(
        regex=r'^advanced/$', name='search_advanced',
        view=AdvancedSearchView.as_view()
    ),
    url(
        regex=r'^results/$', name='results', view=ResultsView.as_view()
    ),
    url(
        regex=r'^results/(?P<search_model_name>[\.\w]+)/$', name='results',
        view=ResultsView.as_view()
    ),
    url(
        regex=r'^search/(?P<search_model_name>[\.\w]+)/$', name='search',
        view=SearchView.as_view()
    )
]

urlpatterns_tools = [
    url(
        regex=r'^backend/reindex/$', name='search_backend_reindex',
        view=SearchBackendReindexView.as_view()
    )
]

urlpatterns = []
urlpatterns.extend(urlpatterns_search)
urlpatterns.extend(urlpatterns_tools)

api_urls = [
    url(
        regex=r'^search/(?P<search_model_name>[\.\w]+)/$', name='search-view',
        view=APISearchView.as_view()
    ),
    url(
        regex=r'^search/advanced/(?P<search_model_name>[\.\w]+)/$',
        name='advanced-search-view', view=APIAdvancedSearchView.as_view()
    ),
    url(
        regex=r'^search_models/$', name='searchmodel-list',
        view=APISearchModelList.as_view()
    )
]
