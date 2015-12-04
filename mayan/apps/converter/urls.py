from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .views import (
    TransformationCreateView, TransformationDeleteView, TransformationEditView,
    TransformationListView
)

urlpatterns = patterns(
    'converter.views',
    url(
        r'^create_for/(?P<app_label>[-\w]+)/(?P<model>[-\w]+)/(?P<object_id>\d+)/$',
        TransformationCreateView.as_view(), name='transformation_create'
    ),
    url(
        r'^list_for/(?P<app_label>[-\w]+)/(?P<model>[-\w]+)/(?P<object_id>\d+)/$',
        TransformationListView.as_view(), name='transformation_list'
    ),
    url(
        r'^delete/(?P<pk>\d+)/$', TransformationDeleteView.as_view(),
        name='transformation_delete'
    ),
    url(
        r'^edit/(?P<pk>\d+)/$', TransformationEditView.as_view(),
        name='transformation_edit'
    ),
)
