from django.conf.urls import url

from .views import (
    DocumentFileDriverListView, DocumentFileDriverEntryFileMetadataListView,
    DocumentFileSubmitView, DocumentTypeSettingsEditView,
    DocumentTypeSubmitView
)

urlpatterns = [
    url(
        regex=r'^documents/files/(?P<document_file_id>\d+)/drivers/$',
        name='document_file_driver_list', view=DocumentFileDriverListView.as_view()

    ),
    url(
        regex=r'^documents/files/(?P<document_file_id>\d+)/submit/$',
        name='document_file_submit', view=DocumentFileSubmitView.as_view()
    ),
    url(
        regex=r'^documents/files/multiple/submit/$',
        name='document_file_multiple_submit',
        view=DocumentFileSubmitView.as_view()
    ),
    url(
        regex=r'^documents/files/drivers/(?P<document_file_driver_id>\d+)/attributes/$',
        name='document_file_driver_file_metadata_list',
        view=DocumentFileDriverEntryFileMetadataListView.as_view()
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
]
