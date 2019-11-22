from __future__ import unicode_literals

from django.conf.urls import url

from .api_views import (
    APIDocumentOCRView, APIDocumentPageOCRContentView,
    APIDocumentVersionOCRView
)
from .views import (
    DocumentOCRContentDeleteView, DocumentOCRContentView,
    DocumentOCRDownloadView, DocumentOCRErrorsListView,
    DocumentPageOCRContentView, DocumentSubmitView,
    DocumentTypeSettingsEditView, DocumentTypeSubmitView,
    DocumentVersionPageOCRContentView, EntryListView
)

urlpatterns = [
    url(
        regex=r'^documents/(?P<pk>\d+)/content/$',
        view=DocumentOCRContentView.as_view(), name='document_ocr_content'
    ),
    url(
        regex=r'^documents/(?P<pk>\d+)/content/delete/$',
        view=DocumentOCRContentDeleteView.as_view(),
        name='document_ocr_content_delete'
    ),
    url(
        regex=r'^documents/multiple/content/delete/$',
        view=DocumentOCRContentDeleteView.as_view(),
        name='document_ocr_content_delete_multiple'
    ),
    url(
        regex=r'^documents/(?P<pk>\d+)/ocr/download/$',
        view=DocumentOCRDownloadView.as_view(), name='document_ocr_download'
    ),
    url(
        regex=r'^documents/(?P<pk>\d+)/ocr/errors/$',
        view=DocumentOCRErrorsListView.as_view(),
        name='document_ocr_error_list'
    ),
    url(
        regex=r'^documents/(?P<pk>\d+)/submit/$',
        view=DocumentSubmitView.as_view(), name='document_submit'
    ),
    url(
        regex=r'^documents/multiple/submit/$',
        view=DocumentSubmitView.as_view(), name='document_submit_multiple'
    ),
    url(
        regex=r'^documents/pages/(?P<pk>\d+)/content/$',
        view=DocumentPageOCRContentView.as_view(),
        name='document_page_ocr_content'
    ),
    url(
        regex=r'^documents/versions/pages/(?P<pk>\d+)/content/$',
        view=DocumentVersionPageOCRContentView.as_view(),
        name='document_version_page_ocr_content'
    ),
    url(
        regex=r'^document_types/submit/$',
        view=DocumentTypeSubmitView.as_view(), name='document_type_submit'
    ),
    url(
        regex=r'^document_types/(?P<pk>\d+)/ocr/settings/$',
        view=DocumentTypeSettingsEditView.as_view(),
        name='document_type_ocr_settings'
    ),
    url(regex=r'^logs/$', view=EntryListView.as_view(), name='entry_list'),
]

api_urls = [
    url(
        regex=r'^documents/(?P<pk>\d+)/ocr/submit/$',
        view=APIDocumentOCRView.as_view(), name='document-ocr-submit-view'
    ),
    url(
        regex=r'^documents/(?P<document_pk>\d+)/versions/(?P<version_pk>\d+)/ocr/$',
        view=APIDocumentVersionOCRView.as_view(),
        name='document-version-ocr-submit-view'
    ),
    url(
        regex=r'^documents/(?P<document_pk>\d+)/versions/(?P<version_pk>\d+)/pages/(?P<page_pk>\d+)/ocr/$',
        view=APIDocumentPageOCRContentView.as_view(),
        name='document-page-ocr-content-view'
    ),
]
