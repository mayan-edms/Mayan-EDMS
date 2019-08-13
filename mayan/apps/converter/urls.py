from __future__ import unicode_literals

from django.conf.urls import url

from .views import (
    TransformationCreateView, TransformationDeleteView, TransformationEditView,
    TransformationListView
)

urlpatterns = [
    url(
        regex=r'^object/(?P<app_label>[-\w]+)/(?P<model>[-\w]+)/(?P<object_id>\d+)/transformations/$',
        view=TransformationListView.as_view(), name='transformation_list'
    ),
    url(
        regex=r'^object/(?P<app_label>[-\w]+)/(?P<model>[-\w]+)/(?P<object_id>\d+)/transformations/create/$',
        view=TransformationCreateView.as_view(), name='transformation_create'
    ),
    url(
        regex=r'^transformations/(?P<pk>\d+)/delete/$', view=TransformationDeleteView.as_view(),
        name='transformation_delete'
    ),
    url(
        regex=r'^transformations/(?P<pk>\d+)/edit/$', view=TransformationEditView.as_view(),
        name='transformation_edit'
    ),
]
