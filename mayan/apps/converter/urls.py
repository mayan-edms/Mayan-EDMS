from __future__ import unicode_literals

from django.conf.urls import url

from .views import (
    TransformationCreateView, TransformationDeleteView,
    TransformationEditView, TransformationListView, TransformationSelectView
)

urlpatterns = [
    url(
        regex=r'^object/(?P<app_label>[-\w]+)/(?P<model>[-\w]+)/(?P<object_id>\d+)/layers/(?P<layer_name>[-_\w]+)/transformations/$',
        view=TransformationListView.as_view(), name='transformation_list'
    ),
    url(
        regex=r'^object/(?P<app_label>[-\w]+)/(?P<model>[-\w]+)/(?P<object_id>\d+)/layers/(?P<layer_name>[-_\w]+)/transformations/select/$',
        view=TransformationSelectView.as_view(), name='transformation_select'
    ),
    url(
        regex=r'^object/(?P<app_label>[-\w]+)/(?P<model>[-\w]+)/(?P<object_id>\d+)/layers/(?P<layer_name>[-_\w]+)/transformations/(?P<transformation_name>[-_\w]+)/create/$',
        view=TransformationCreateView.as_view(), name='transformation_create'
    ),
    url(
        regex=r'^layers/(?P<layer_name>[-_\w]+)/transformations/(?P<pk>\d+)/delete/$',
        view=TransformationDeleteView.as_view(), name='transformation_delete'
    ),
    url(
        regex=r'^layers/(?P<layer_name>[-_\w]+)/transformations/(?P<pk>\d+)/edit/$',
        view=TransformationEditView.as_view(), name='transformation_edit'
    ),
]
