from django.conf.urls import url

from .api_views import (
    APISignatureCaptureDetailView, APISignatureCapturesImageView,
    APISignatureCaptureListView
)
from .views import (
    SignatureCaptureCreateView, SignatureCaptureDeleteView,
    SignatureCaptureDetailView, SignatureCaptureEditView,
    SignatureCaptureListView
)

urlpatterns = [
    url(
        regex=r'^documents/(?P<document_id>\d+)/signature_captures/$',
        name='signature_capture_list',
        view=SignatureCaptureListView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>\d+)/signature_captures/create/$',
        name='signature_capture_create',
        view=SignatureCaptureCreateView.as_view()
    ),
    url(
        regex=r'^signature_captures/(?P<signature_capture_id>\d+)/delete/$',
        name='signature_capture_delete',
        view=SignatureCaptureDeleteView.as_view()
    ),
    url(
        regex=r'^signature_captures/(?P<signature_capture_id>\d+)/detail/$',
        name='signature_capture_detail',
        view=SignatureCaptureDetailView.as_view()
    ),
    url(
        regex=r'^signature_captures/(?P<signature_capture_id>\d+)/edit/$',
        name='signature_capture_edit',
        view=SignatureCaptureEditView.as_view()
    )
]

api_urls = [
    url(
        regex=r'^documents/(?P<document_id>[0-9]+)/signature_captures/$',
        name='signature_capture-list',
        view=APISignatureCaptureListView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>[0-9]+)/signature_captures/(?P<signature_capture_id>[0-9]+)/$',
        name='signature_capture-detail',
        view=APISignatureCaptureDetailView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>[0-9]+)/signature_captures/(?P<signature_capture_id>[0-9]+)/image/$',
        name='signature_capture-image',
        view=APISignatureCapturesImageView.as_view()
    )
]
