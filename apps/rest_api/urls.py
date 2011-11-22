from django.conf.urls.defaults import patterns, url

from djangorestframework.views import ListModelView
from djangorestframework.views import ListOrCreateModelView, InstanceModelView

from rest_api.views import APIBase, Version_0, ReadOnlyInstanceModelView, IsZoomable, Exists, Size
from rest_api.resources import DocumentResourceSimple

urlpatterns = patterns('',
    url(r'^$', APIBase.as_view(), name='api-root'),
    url(r'^v0/$', Version_0.as_view(), name='api-version-0'),
    
    # Version 0 alpha API calls    
    url(r'^v0/document/(?P<pk>[0-9]+)/$', ReadOnlyInstanceModelView.as_view(resource=DocumentResourceSimple), name='documents-simple'),
    url(r'^v0/document/(?P<pk>[0-9]+)/expensive/is_zoomable/$', IsZoomable.as_view(), name='documents-expensive-is_zoomable'),
    url(r'^v0/document/(?P<pk>[0-9]+)/expensive/exists/$', IsZoomable.as_view(), name='documents-expensive-exists'),
    url(r'^v0/document/(?P<pk>[0-9]+)/expensive/size/$', Size.as_view(), name='documents-expensive-size'),
)
