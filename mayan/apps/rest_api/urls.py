from __future__ import absolute_import

from django.conf.urls import patterns, url

from .views import APIBase, Version_1, DocumentDetailView, IsZoomable

urlpatterns = patterns('',
    url(r'^$', APIBase.as_view(), name='api-root'),
    url(r'^v1/$', Version_1.as_view(), name='api-version-1'),

    # Version 1 API calls
    url(r'^v1/document/(?P<pk>[0-9]+)/$', DocumentDetailView.as_view(), name='document-detail'),
    url(r'^v1/document/(?P<pk>[0-9]+)/version/(?P<version_pk>[0-9]+)/page/(?P<page_number>[0-9]+)/expensive/is_zoomable/$', IsZoomable.as_view(), name='documents-expensive-is_zoomable'),
)
