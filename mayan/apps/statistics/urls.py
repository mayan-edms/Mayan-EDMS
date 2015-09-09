from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .views import NamespaceDetailView, NamespaceListView, StatisticExecute

urlpatterns = patterns(
    'statistics.views',
    url(r'^$', NamespaceListView.as_view(), name='namespace_list'),
    url(
        r'^namespace/(?P<namespace_id>\w+)/details/$',
        NamespaceDetailView.as_view(), name='namespace_details'
    ),
    url(
        r'^(?P<statistic_id>[\w,-]+)/view/$', StatisticExecute.as_view(),
        name='statistic_execute'
    ),
)
