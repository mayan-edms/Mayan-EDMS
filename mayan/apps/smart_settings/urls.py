from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .views import NamespaceDetailView, NamespaceListView

urlpatterns = patterns(
    '',
    url(
        r'^namespace/all/$', NamespaceListView.as_view(),
        name='namespace_list'
    ),
    url(
        r'^namespace/(?P<namespace_name>\w+)/$',
        NamespaceDetailView.as_view(), name='namespace_detail'
    ),
)
