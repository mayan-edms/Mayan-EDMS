from __future__ import unicode_literals

from django.conf.urls import url

from .views import (
    AllDocumentSignatureVerifyView, DocumentVersionDetachedSignatureCreateView,
    DocumentVersionEmbeddedSignatureCreateView,
    DocumentVersionSignatureDeleteView, DocumentVersionSignatureDetailView,
    DocumentVersionSignatureDownloadView, DocumentVersionSignatureListView,
    DocumentVersionSignatureUploadView
)

urlpatterns = [
    url(
        regex=r'^(?P<pk>\d+)/details/$',
        view=DocumentVersionSignatureDetailView.as_view(),
        name='document_version_signature_details'
    ),
    url(
        regex=r'^signature/(?P<pk>\d+)/download/$',
        view=DocumentVersionSignatureDownloadView.as_view(),
        name='document_version_signature_download'
    ),
    url(
        regex=r'^document/version/(?P<pk>\d+)/signatures/list/$',
        view=DocumentVersionSignatureListView.as_view(),
        name='document_version_signature_list'
    ),
    url(
        regex=r'^documents/version/(?P<pk>\d+)/signature/detached/upload/$',
        view=DocumentVersionSignatureUploadView.as_view(),
        name='document_version_signature_upload'
    ),
    url(
        regex=r'^documents/version/(?P<pk>\d+)/signature/detached/create/$',
        view=DocumentVersionDetachedSignatureCreateView.as_view(),
        name='document_version_signature_detached_create'
    ),
    url(
        regex=r'^documents/version/(?P<pk>\d+)/signature/embedded/create/$',
        view=DocumentVersionEmbeddedSignatureCreateView.as_view(),
        name='document_version_signature_embedded_create'
    ),
    url(
        regex=r'^signature/(?P<pk>\d+)/delete/$',
        view=DocumentVersionSignatureDeleteView.as_view(),
        name='document_version_signature_delete'
    ),
    url(
        regex=r'^tools/all/document/version/signature/verify/$',
        view=AllDocumentSignatureVerifyView.as_view(),
        name='all_document_version_signature_verify'
    ),
]
