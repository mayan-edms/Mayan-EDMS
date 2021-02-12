from django.conf.urls import url

from .views import (
    CacheDetailView, CacheListView, CachePartitionPurgeView, CachePurgeView
)

urlpatterns = [
    url(
        regex=r'^caches/$', name='cache_list', view=CacheListView.as_view()
    ),
    url(
        regex=r'^caches/(?P<cache_id>\d+)/detail/$', name='cache_detail',
        view=CacheDetailView.as_view()
    ),
    url(
        regex=r'^caches/(?P<cache_id>\d+)/purge/$', name='cache_purge',
        view=CachePurgeView.as_view()
    ),
    url(
        regex=r'^caches/multiple/purge/$', name='cache_multiple_purge',
        view=CachePurgeView.as_view()
    ),
    url(
        regex=r'^apps/(?P<app_label>[-\w]+)/models/(?P<model_name>[-\w]+)/objects/(?P<object_id>\d+)/cache_partitions/purge/$',
        name='cache_partitions_purge', view=CachePartitionPurgeView.as_view()
    ),
]
