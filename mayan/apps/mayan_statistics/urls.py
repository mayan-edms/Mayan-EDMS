from django.conf.urls import url

from .views import (
    NamespaceDetailView, NamespaceListView, StatisticDetailView,
    StatisticQueueView
)

urlpatterns = [
    url(regex=r'^namespace/$', view=NamespaceListView.as_view(), name='namespace_list'),
    url(
        regex=r'^namespaces/(?P<slug>[\w-]+)/$',
        view=NamespaceDetailView.as_view(), name='namespace_details'
    ),
    url(
        regex=r'^statistics/(?P<slug>[\w-]+)/view/$', view=StatisticDetailView.as_view(),
        name='statistic_detail'
    ),
    url(
        regex=r'^statistics/(?P<slug>[\w-]+)/queue/$', view=StatisticQueueView.as_view(),
        name='statistic_queue'
    ),
]
