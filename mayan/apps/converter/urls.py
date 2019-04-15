from __future__ import unicode_literals

from django.conf.urls import url

from .views import (
    TransformationCreateView, TransformationDeleteView, TransformationEditView,
    TransformationListView
)

urlpatterns = [
    url(
        regex=r'^create_for/(?P<app_label>[-\w]+)/(?P<model>[-\w]+)/(?P<object_id>\d+)/$',
        view=TransformationCreateView.as_view(), name='transformation_create'
    ),
    url(
        regex=r'^list_for/(?P<app_label>[-\w]+)/(?P<model>[-\w]+)/(?P<object_id>\d+)/$',
        view=TransformationListView.as_view(), name='transformation_list'
    ),
    url(
        regex=r'^delete/(?P<pk>\d+)/$', view=TransformationDeleteView.as_view(),
        name='transformation_delete'
    ),
    url(
        regex=r'^edit/(?P<pk>\d+)/$', view=TransformationEditView.as_view(),
        name='transformation_edit'
    ),
]
