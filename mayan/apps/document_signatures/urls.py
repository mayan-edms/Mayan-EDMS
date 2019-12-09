from __future__ import unicode_literals

from django.conf.urls import url

from .api_views import (
    APIDocumentSignDetachedView, APIDocumentDetachedSignatureListView,
    APIDocumentDetachedSignatureView, APIDocumentEmbeddedSignatureListView,
    APIDocumentEmbeddedSignatureView, APIDocumentSignEmbeddedView
)

from .views import (
    AllDocumentSignatureVerifyView, DocumentVersionDetachedSignatureCreateView,
    DocumentVersionEmbeddedSignatureCreateView,
    DocumentVersionSignatureDeleteView, DocumentVersionSignatureDetailView,
    DocumentVersionSignatureDownloadView, DocumentVersionSignatureListView,
    DocumentVersionSignatureUploadView
)

urlpatterns = [
    url(
        regex=r'^signatures/(?P<pk>\d+)/details/$',
        view=DocumentVersionSignatureDetailView.as_view(),
        name='document_version_signature_details'
    ),
    url(
        regex=r'^signatures/(?P<pk>\d+)/download/$',
        view=DocumentVersionSignatureDownloadView.as_view(),
        name='document_version_signature_download'
    ),
    url(
        regex=r'^documents/versions/(?P<pk>\d+)/signatures/$',
        view=DocumentVersionSignatureListView.as_view(),
        name='document_version_signature_list'
    ),
    url(
        regex=r'^documents/versions/(?P<pk>\d+)/signatures/detached/upload/$',
        view=DocumentVersionSignatureUploadView.as_view(),
        name='document_version_signature_upload'
    ),
    url(
        regex=r'^documents/versions/(?P<pk>\d+)/signatures/detached/create/$',
        view=DocumentVersionDetachedSignatureCreateView.as_view(),
        name='document_version_signature_detached_create'
    ),
    url(
        regex=r'^documents/versions/(?P<pk>\d+)/signatures/embedded/create/$',
        view=DocumentVersionEmbeddedSignatureCreateView.as_view(),
        name='document_version_signature_embedded_create'
    ),
    url(
        regex=r'^signatures/(?P<pk>\d+)/delete/$',
        view=DocumentVersionSignatureDeleteView.as_view(),
        name='document_version_signature_delete'
    ),
    url(
        regex=r'^tools/all/document/version/signature/verify/$',
        view=AllDocumentSignatureVerifyView.as_view(),
        name='all_document_version_signature_verify'
    ),
]

api_urls = [
    url(
        regex=r'^documents/(?P<document_id>[0-9]+)/versions/(?P<document_version_id>[0-9]+)/signatures/detached/$',
        view=APIDocumentDetachedSignatureListView.as_view(),
        name='document-version-signature-detached-list'
    ),
    url(
        regex=r'^documents/(?P<document_id>[0-9]+)/versions/(?P<document_version_id>[0-9]+)/signatures/detached/sign/$',
        view=APIDocumentSignDetachedView.as_view(),
        name='document-version-signature-detached-sign'
    ),
    url(
        regex=r'^documents/(?P<document_id>[0-9]+)/versions/(?P<document_version_id>[0-9]+)/signatures/detached/(?P<detached_signature_id>[0-9]+)/$',
        view=APIDocumentDetachedSignatureView.as_view(),
        name='detachedsignature-detail'
    ),
    url(
        regex=r'^documents/(?P<document_id>[0-9]+)/versions/(?P<document_version_id>[0-9]+)/signatures/embedded/$',
        view=APIDocumentEmbeddedSignatureListView.as_view(),
        name='document-version-signature-embedded-list'
    ),
    url(
        regex=r'^documents/(?P<document_id>[0-9]+)/versions/(?P<document_version_id>[0-9]+)/signatures/embedded/sign/$',
        view=APIDocumentSignEmbeddedView.as_view(),
        name='document-version-signature-embedded-sign'
    ),
    url(
        regex=r'^documents/(?P<document_id>[0-9]+)/versions/(?P<document_version_id>[0-9]+)/signatures/embedded/(?P<embedded_signature_id>[0-9]+)/$',
        view=APIDocumentEmbeddedSignatureView.as_view(),
        name='embeddedsignature-detail'
    ),
]
