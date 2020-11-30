from django.conf.urls import url

from .views import (
    DocumentDuplicatesListView, DuplicatedDocumentListView,
    ScanDuplicatedDocuments
)

urlpatterns = [
    url(
        regex=r'^documents/duplicated/$',
        name='duplicated_document_list',
        view=DuplicatedDocumentListView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>\d+)/duplicates/$',
        name='document_duplicates_list',
        view=DocumentDuplicatesListView.as_view()
    ),
    url(
        regex=r'^tools/documents/duplicated/scan/$',
        name='duplicated_document_scan',
        view=ScanDuplicatedDocuments.as_view()
    ),
]

api_urls = []
