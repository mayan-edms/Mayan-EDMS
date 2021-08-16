from django.conf.urls import url

from .api_views import (
    APIDocumentTypeOCRSettingsView, APIDocumentOCRSubmitView,
    APIDocumentVersionOCRSubmitView, APIDocumentVersionPageOCRContentView
)
from .views import (
    DocumentVersionOCRContentDeleteView, DocumentVersionOCRContentView,
    DocumentVersionOCRDownloadView,
    DocumentVersionOCRErrorsListView, DocumentVersionPageOCRContentView,
    DocumentVersionOCRSubmitView,
    DocumentTypeSettingsEditView, DocumentTypeSubmitView, EntryListView
)

urlpatterns_document_types = [
    url(
        regex=r'^document_types/submit/$', name='document_type_submit',
        view=DocumentTypeSubmitView.as_view()
    ),
    url(
        regex=r'^document_types/(?P<document_type_id>\d+)/ocr/settings/$',
        name='document_type_ocr_settings',
        view=DocumentTypeSettingsEditView.as_view()
    )
]

urlpatterns_document_versions = [
    url(
        regex=r'^documents/versions/(?P<document_version_id>\d+)/content/$',
        name='document_version_ocr_content_view',
        view=DocumentVersionOCRContentView.as_view()
    ),
    url(
        regex=r'^documents/versions/(?P<document_version_id>\d+)/content/delete/$',
        name='document_version_ocr_content_delete',
        view=DocumentVersionOCRContentDeleteView.as_view()
    ),
    url(
        regex=r'^documents/versions/multiple/content/delete/$',
        name='document_version_multiple_ocr_content_delete',
        view=DocumentVersionOCRContentDeleteView.as_view()
    ),
    url(
        regex=r'^documents/versions/(?P<document_version_id>\d+)/ocr/download/$',
        name='document_version_ocr_download',
        view=DocumentVersionOCRDownloadView.as_view()
    ),
    url(
        regex=r'^documents/versions/(?P<document_version_id>\d+)/ocr/errors/$',
        name='document_version_ocr_error_list',
        view=DocumentVersionOCRErrorsListView.as_view()
    ),
    url(
        regex=r'^documents/versions/(?P<document_version_id>\d+)/submit/$',
        name='document_version_ocr_submit',
        view=DocumentVersionOCRSubmitView.as_view()
    ),
    url(
        regex=r'^documents/versions/multiple/submit/$',
        name='document_version_multiple_ocr_submit',
        view=DocumentVersionOCRSubmitView.as_view()
    ),
    url(
        regex=r'^documents/versions/pages/(?P<document_version_page_id>\d+)/content/$',
        name='document_version_page_ocr_content_detail_view',
        view=DocumentVersionPageOCRContentView.as_view()
    ),
    url(regex=r'^logs/$', name='entry_list', view=EntryListView.as_view())
]

urlpatterns = []
urlpatterns.extend(urlpatterns_document_types)
urlpatterns.extend(urlpatterns_document_versions)

api_urls = [
    url(
        regex=r'^document_types/(?P<document_type_id>\d+)/ocr/settings/$',
        name='document-type-ocr-settings-view',
        view=APIDocumentTypeOCRSettingsView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>\d+)/ocr/submit/$',
        name='document-ocr-submit-view',
        view=APIDocumentOCRSubmitView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>\d+)/versions/(?P<document_version_id>\d+)/ocr/submit/$',
        name='document-version-ocr-submit-view',
        view=APIDocumentVersionOCRSubmitView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>\d+)/versions/(?P<document_version_id>\d+)/pages/(?P<document_version_page_id>\d+)/ocr/$',
        name='document-version-page-ocr-content-detail-view',
        view=APIDocumentVersionPageOCRContentView.as_view()
    ),
]
