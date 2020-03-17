from __future__ import unicode_literals

from django.conf.urls import url

from .api_views import (
    APIDocumentOCRView, APIDocumentPageOCRContentView,
    APIDocumentVersionOCRView
)
from .views import (
    DocumentOCRContentDeleteView, DocumentOCRContentView,
    DocumentOCRDownloadView,
    DocumentOCRErrorsListView, DocumentPageOCRContentView, DocumentSubmitView,
    DocumentTypeSettingsEditView, DocumentTypeSubmitView, EntryListView
)

urlpatterns = [
    url(
        regex=r'^document_types/submit/$', name='document_type_submit',
        view=DocumentTypeSubmitView.as_view()
    ),
    url(
        regex=r'^document_types/(?P<document_type_id>\d+)/ocr/settings/$',
        name='document_type_ocr_settings',
        view=DocumentTypeSettingsEditView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>\d+)/content/$',
        name='document_ocr_content', view=DocumentOCRContentView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>\d+)/content/delete/$',
        name='document_ocr_content_delete',
        view=DocumentOCRContentDeleteView.as_view()
    ),
    url(
        regex=r'^documents/multiple/content/delete/$',
        name='document_ocr_content_delete_multiple',
        view=DocumentOCRContentDeleteView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>\d+)/ocr/download/$',
        name='document_ocr_download', view=DocumentOCRDownloadView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>\d+)/ocr/errors/$',
        name='document_ocr_error_list',
        view=DocumentOCRErrorsListView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>\d+)/submit/$',
        name='document_submit', view=DocumentSubmitView.as_view()
    ),
    url(
        regex=r'^documents/multiple/submit/$',
        name='document_submit_multiple', view=DocumentSubmitView.as_view()
    ),
    url(
        regex=r'^documents/pages/(?P<document_page_id>\d+)/content/$',
        name='document_page_ocr_content',
        view=DocumentPageOCRContentView.as_view()
    ),
    url(regex=r'^logs/$', name='entry_list', view=EntryListView.as_view())
]

api_urls = [
    url(
        regex=r'^documents/(?P<pk>\d+)/ocr/submit/$',
        name='document-ocr-submit-view', view=APIDocumentOCRView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_pk>\d+)/versions/(?P<version_pk>\d+)/ocr/$',
        name='document-version-ocr-submit-view',
        view=APIDocumentVersionOCRView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_pk>\d+)/versions/(?P<version_pk>\d+)/pages/(?P<page_pk>\d+)/ocr/$',
        name='document-page-ocr-content-view',
        view=APIDocumentPageOCRContentView.as_view()
    ),
]
