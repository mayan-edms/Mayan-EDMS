from django.conf.urls import url

from .views import (
    DocumentDriverListView, DocumentFileDriverEntryFileMetadataListView,
    DocumentSubmitView, DocumentTypeSettingsEditView, DocumentTypeSubmitView
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
        regex=r'^document_file_driver/(?P<document_file_driver_id>\d+)/attributes/$',
        name='document_file_driver_file_metadata_list',
        view=DocumentFileDriverEntryFileMetadataListView.as_view()
    ),
]
