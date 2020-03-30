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
        regex=r'^documents/versions/(?P<document_version_id>\d+)/signatures/$',
        name='document_version_signature_list',
        view=DocumentVersionSignatureListView.as_view()
    ),
    url(
        regex=r'^documents/versions/(?P<document_version_id>\d+)/signatures/detached/create/$',
        name='document_version_signature_detached_create',
        view=DocumentVersionDetachedSignatureCreateView.as_view()
    ),
    url(
        regex=r'^documents/versions/(?P<document_version_id>\d+)/signatures/detached/upload/$',
        name='document_version_signature_upload',
        view=DocumentVersionSignatureUploadView.as_view()
    ),
    url(
        regex=r'^documents/versions/(?P<document_version_id>\d+)/signatures/embedded/create/$',
        name='document_version_signature_embedded_create',
        view=DocumentVersionEmbeddedSignatureCreateView.as_view()
    ),
    url(
        regex=r'^signatures/(?P<signature_id>\d+)/delete/$',
        name='document_version_signature_delete',
        view=DocumentVersionSignatureDeleteView.as_view()
    ),
    url(
        regex=r'^signatures/(?P<signature_id>\d+)/details/$',
        name='document_version_signature_details',
        view=DocumentVersionSignatureDetailView.as_view()
    ),
    url(
        regex=r'^signatures/(?P<signature_id>\d+)/download/$',
        name='document_version_signature_download',
        view=DocumentVersionSignatureDownloadView.as_view()
    ),
    url(
        regex=r'^tools/all/document/version/signature/verify/$',
        name='all_document_version_signature_verify',
        view=AllDocumentSignatureVerifyView.as_view()
    )
]

api_urls = [
    url(
        regex=r'^documents/(?P<document_id>[0-9]+)/versions/(?P<document_version_id>[0-9]+)/signatures/detached/$',
        name='document-version-signature-detached-list',
        view=APIDocumentDetachedSignatureListView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>[0-9]+)/versions/(?P<document_version_id>[0-9]+)/signatures/detached/sign/$',
        name='document-version-signature-detached-sign',
        view=APIDocumentSignDetachedView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>[0-9]+)/versions/(?P<document_version_id>[0-9]+)/signatures/detached/(?P<detached_signature_id>[0-9]+)/$',
        name='detachedsignature-detail',
        view=APIDocumentDetachedSignatureView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>[0-9]+)/versions/(?P<document_version_id>[0-9]+)/signatures/embedded/$',
        name='document-version-signature-embedded-list',
        view=APIDocumentEmbeddedSignatureListView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>[0-9]+)/versions/(?P<document_version_id>[0-9]+)/signatures/embedded/sign/$',
        name='document-version-signature-embedded-sign',
        view=APIDocumentSignEmbeddedView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>[0-9]+)/versions/(?P<document_version_id>[0-9]+)/signatures/embedded/(?P<embedded_signature_id>[0-9]+)/$',
        name='embeddedsignature-detail',
        view=APIDocumentEmbeddedSignatureView.as_view()
    ),
]
