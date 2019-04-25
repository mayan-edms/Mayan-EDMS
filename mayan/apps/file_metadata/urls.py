from __future__ import unicode_literals

from django.conf.urls import url

from .views import (
    DocumentDriverListView, DocumentSubmitView, DocumentTypeSettingsEditView,
    DocumentTypeSubmitView, DocumentVersionDriverEntryFileMetadataListView
)

urlpatterns = [
    url(
        regex=r'^documents/(?P<document_id>\d+)/drivers/$',
        name='document_driver_list', view=DocumentDriverListView.as_view()

    ),
    url(
        regex=r'^documents/(?P<document_id>\d+)/submit/$',
        name='document_submit', view=DocumentSubmitView.as_view()
    ),
    url(
        regex=r'^documents/multiple/submit/$', name='document_multiple_submit',
        view=DocumentSubmitView.as_view()
    ),
    url(
        regex=r'^document_types/(?P<document_type_id>\d+)/file_metadata/settings/$',
        name='document_type_settings',
        view=DocumentTypeSettingsEditView.as_view()
    ),
    url(
        regex=r'^document_types/submit/$', name='document_type_submit',
        view=DocumentTypeSubmitView.as_view()
    ),
    url(
        regex=r'^document_version_driver/(?P<document_version_driver_id>\d+)/attributes/$',
        name='document_version_driver_file_metadata_list',
        view=DocumentVersionDriverEntryFileMetadataListView.as_view()
    ),
]
