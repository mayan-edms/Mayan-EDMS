from __future__ import absolute_import

from django.conf.urls.defaults import patterns, url

from djangorestframework.views import ListModelView
from djangorestframework.views import ListOrCreateModelView, InstanceModelView

from .views import APIBase, Version_0, ReadOnlyInstanceModelView, IsZoomable
from .resources import DocumentResourceSimple

urlpatterns = patterns('',
    url(r'^$', APIBase.as_view(), name='api-root'),
    url(r'^v0/$', Version_0.as_view(), name='api-version-0'),
    
    # Version 0 alpha API calls    
    url(r'^v0/document/(?P<pk>[0-9]+)/$', ReadOnlyInstanceModelView.as_view(resource=DocumentResourceSimple), name='documents-simple'),
    url(r'^v0/document/(?P<pk>[0-9]+)/version/(?P<version_pk>[0-9]+)/page/(?P<page_number>[0-9]+)/expensive/is_zoomable/$', IsZoomable.as_view(), name='documents-expensive-is_zoomable'),
)
