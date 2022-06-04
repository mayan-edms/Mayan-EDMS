from django.conf.urls import url

from .views import (
    StatisticDetailView, StatisticQueueView, StatisticNamespaceDetailView,
    StatisticNamespaceListView
)

urlpatterns = [
    url(
        regex=r'^namespace/$', view=StatisticNamespaceListView.as_view(),
        name='statistic_namespace_list'
    ),
    url(
        regex=r'^namespaces/(?P<slug>[\w-]+)/$',
        view=StatisticNamespaceDetailView.as_view(),
        name='statistic_namespace_detail'
    ),
    url(
        regex=r'^statistics/(?P<slug>[\w-]+)/view/$',
        view=StatisticDetailView.as_view(), name='statistic_detail'
    ),
    url(
        regex=r'^statistics/(?P<slug>[\w-]+)/queue/$',
        view=StatisticQueueView.as_view(), name='statistic_queue'
    )
]
