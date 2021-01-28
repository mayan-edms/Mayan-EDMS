from django.conf.urls import url

from .api_views import (
    APIDocumentSignDetachedView, APIDocumentDetachedSignatureListView,
    APIDocumentDetachedSignatureView, APIDocumentEmbeddedSignatureListView,
    APIDocumentEmbeddedSignatureView, APIDocumentSignEmbeddedView
)

from .views import (
    AllDocumentSignatureRefreshView, AllDocumentSignatureVerifyView,
    DocumentFileDetachedSignatureCreateView,
    DocumentFileEmbeddedSignatureCreateView, DocumentFileSignatureDeleteView,
    DocumentFileSignatureDetailView, DocumentFileSignatureDownloadView,
    DocumentFileSignatureListView, DocumentFileSignatureUploadView
)

urlpatterns = [
    url(
        regex=r'^documents/files/(?P<document_file_id>\d+)/signatures/$',
        name='document_file_signature_list',
        view=DocumentFileSignatureListView.as_view()
    ),
    url(
        regex=r'^documents/files/(?P<document_file_id>\d+)/signatures/detached/create/$',
        name='document_file_signature_detached_create',
        view=DocumentFileDetachedSignatureCreateView.as_view()
    ),
    url(
        regex=r'^documents/files/(?P<document_file_id>\d+)/signatures/detached/upload/$',
        name='document_file_signature_upload',
        view=DocumentFileSignatureUploadView.as_view()
    ),
    url(
        regex=r'^documents/files/(?P<document_file_id>\d+)/signatures/embedded/create/$',
        name='document_file_signature_embedded_create',
        view=DocumentFileEmbeddedSignatureCreateView.as_view()
    ),
    url(
        regex=r'^signatures/(?P<signature_id>\d+)/delete/$',
        name='document_file_signature_delete',
        view=DocumentFileSignatureDeleteView.as_view()
    ),
    url(
        regex=r'^signatures/(?P<signature_id>\d+)/details/$',
        name='document_file_signature_details',
        view=DocumentFileSignatureDetailView.as_view()
    ),
    url(
        regex=r'^signatures/(?P<signature_id>\d+)/download/$',
        name='document_file_signature_download',
        view=DocumentFileSignatureDownloadView.as_view()
    ),
    url(
        regex=r'^tools/all/document/file/signature/refresh/$',
        name='all_document_file_signature_refresh',
        view=AllDocumentSignatureRefreshView.as_view()
    ),
    url(
        regex=r'^tools/all/document/file/signature/verify/$',
        name='all_document_file_signature_verify',
        view=AllDocumentSignatureVerifyView.as_view()
    )
]

api_urls = [
    url(
        regex=r'^documents/(?P<document_id>[0-9]+)/files/(?P<document_file_id>[0-9]+)/signatures/detached/$',
        name='document-file-signature-detached-list',
        view=APIDocumentDetachedSignatureListView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>[0-9]+)/files/(?P<document_file_id>[0-9]+)/signatures/detached/sign/$',
        name='document-file-signature-detached-sign',
        view=APIDocumentSignDetachedView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>[0-9]+)/files/(?P<document_file_id>[0-9]+)/signatures/detached/(?P<detached_signature_id>[0-9]+)/$',
        name='detachedsignature-detail',
        view=APIDocumentDetachedSignatureView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>[0-9]+)/files/(?P<document_file_id>[0-9]+)/signatures/embedded/$',
        name='document-file-signature-embedded-list',
        view=APIDocumentEmbeddedSignatureListView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>[0-9]+)/files/(?P<document_file_id>[0-9]+)/signatures/embedded/sign/$',
        name='document-file-signature-embedded-sign',
        view=APIDocumentSignEmbeddedView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>[0-9]+)/files/(?P<document_file_id>[0-9]+)/signatures/embedded/(?P<embedded_signature_id>[0-9]+)/$',
        name='embeddedsignature-detail',
        view=APIDocumentEmbeddedSignatureView.as_view()
    ),
]
