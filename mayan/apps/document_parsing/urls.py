from __future__ import unicode_literals

from django.conf.urls import url

from .api_views import APIDocumentPageContentView
from .views import (
    DocumentContentView, DocumentContentDownloadView,
    DocumentPageContentView, DocumentParsingErrorsListView,
    DocumentSubmitView, DocumentTypeSettingsEditView, DocumentTypeSubmitView,
    ParseErrorListView
)

urlpatterns = [
    url(
        regex=r'^documents/(?P<pk>\d+)/content/$',
        view=DocumentContentView.as_view(), name='document_content'
    ),
    url(
        regex=r'^documents/pages/(?P<pk>\d+)/content/$',
        view=DocumentPageContentView.as_view(), name='document_page_content'
    ),
    url(
        regex=r'^documents/(?P<pk>\d+)/content/download/$',
        view=DocumentContentDownloadView.as_view(), name='document_content_download'
    ),
    url(
        regex=r'^document_types/submit/$',
        view=DocumentTypeSubmitView.as_view(), name='document_type_submit'
    ),
    url(
        regex=r'^document_types/(?P<pk>\d+)/parsing/settings/$',
        view=DocumentTypeSettingsEditView.as_view(),
        name='document_type_parsing_settings'
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
        regex=r'^documents/(?P<pk>\d+)/errors/$',
        view=DocumentParsingErrorsListView.as_view(),
        name='document_parsing_error_list'
    ),
    url(
        regex=r'^errors/all/$', view=ParseErrorListView.as_view(),
        name='error_list'
    ),
]

api_urls = [
    url(
        regex=r'^documents/(?P<document_pk>\d+)/versions/(?P<version_pk>\d+)/pages/(?P<page_pk>\d+)/content/$',
        view=APIDocumentPageContentView.as_view(),
        name='document-page-content-view'
    ),
]
