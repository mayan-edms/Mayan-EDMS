from django.conf.urls import url

from .views import (
    TransformationCreateView, TransformationDeleteView,
    TransformationEditView, TransformationListView, TransformationSelectView
)

urlpatterns = [
    url(
        regex=r'^object/(?P<app_label>[-\w]+)/(?P<model_name>[-\w]+)/(?P<object_id>\d+)/layers/(?P<layer_name>[-_\w]+)/transformations/$',
        name='transformation_list', view=TransformationListView.as_view()
    ),
    url(
        regex=r'^object/(?P<app_label>[-\w]+)/(?P<model_name>[-\w]+)/(?P<object_id>\d+)/layers/(?P<layer_name>[-_\w]+)/transformations/select/$',
        name='transformation_select', view=TransformationSelectView.as_view()
    ),
    url(
        regex=r'^object/(?P<app_label>[-\w]+)/(?P<model_name>[-\w]+)/(?P<object_id>\d+)/layers/(?P<layer_name>[-_\w]+)/transformations/(?P<transformation_name>[-_\w]+)/create/$',
        name='transformation_create', view=TransformationCreateView.as_view()
    ),
    url(
        regex=r'^layers/(?P<layer_name>[-_\w]+)/transformations/(?P<transformation_id>\d+)/delete/$',
        name='transformation_delete', view=TransformationDeleteView.as_view()
    ),
    url(
        regex=r'^layers/(?P<layer_name>[-_\w]+)/transformations/(?P<transformation_id>\d+)/edit/$',
        name='transformation_edit', view=TransformationEditView.as_view()
    ),
]
