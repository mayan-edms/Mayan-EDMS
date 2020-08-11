from django.conf.urls import url

from .views import (
    AssetCreateView, AssetDeleteView, AssetEditView, AssetListView,
    TransformationCreateView, TransformationDeleteView,
    TransformationEditView, TransformationListView, TransformationSelectView
)

urlpatterns_assets = [
    url(
        regex=r'^assets/$', name='asset_list',
        view=AssetListView.as_view()
    ),
    url(
        regex=r'^assets/create/$', name='asset_create',
        view=AssetCreateView.as_view()
    ),
    url(
        regex=r'^assets/(?P<asset_id>\d+)/delete/$',
        name='asset_single_delete', view=AssetDeleteView.as_view()
    ),
    url(
        regex=r'^assets/multiple/delete/$',
        name='asset_multiple_delete', view=AssetDeleteView.as_view()
    ),
    url(
        regex=r'^assets/(?P<asset_id>\d+)/edit/$', name='asset_edit',
        view=AssetEditView.as_view()
    ),
]

urlpatterns_transformations = [
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

urlpatterns = []
urlpatterns.extend(urlpatterns_assets)
urlpatterns.extend(urlpatterns_transformations)
