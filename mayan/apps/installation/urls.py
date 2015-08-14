from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .views import NamespaceDetailView, NamespaceListView

urlpatterns = patterns(
    'installation.views',
    url(r'^$', NamespaceListView.as_view(), name='namespace_list'),
    url(
        r'^(?P<namespace_id>\w+)/details/$', NamespaceDetailView.as_view(),
        name='namespace_details'
    ),
)
