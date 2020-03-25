from django.conf.urls import url

from .views import CacheListView, CachePurgeView

urlpatterns = [
    url(
        regex=r'^caches/$', name='cache_list', view=CacheListView.as_view()
    ),
    url(
        regex=r'^caches/(?P<cache_id>\d+)/purge/$', name='cache_purge',
        view=CachePurgeView.as_view()
    ),
    url(
        regex=r'^caches/multiple/purge/$', name='cache_multiple_purge',
        view=CachePurgeView.as_view()
    ),
]
