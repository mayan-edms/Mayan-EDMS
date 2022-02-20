from django.conf.urls import url

from .api_views import (
    APIDocumentDuplicateListView, APIDuplicatedDocumentListView
)
from .views import (
    DuplicateBackendDetailView, DuplicateBackendListView,
    DocumentDuplicateBackendDetailView, DocumentDuplicateBackendListView,
    ScanDuplicatedDocuments
)

urlpatterns = [
    url(
        regex=r'^documents/duplicated/scan/$',
        name='duplicated_document_scan',
        view=ScanDuplicatedDocuments.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>\d+)/backends/$',
        name='document_backend_list',
        view=DocumentDuplicateBackendListView.as_view()
    ),
    url(
        regex=r'^backends/(?P<document_id>\d+)/backends/(?P<backend_id>\d+)/$',
        name='document_backend_detail',
        view=DocumentDuplicateBackendDetailView.as_view()
    ),
    url(
        regex=r'^backends/$', name='backend_list',
        view=DuplicateBackendListView.as_view()
    ),
    url(
        regex=r'^backends/(?P<backend_id>\d+)/$', name='backend_detail',
        view=DuplicateBackendDetailView.as_view()
    )
]

api_urls = [
    url(
        regex=r'^documents/duplicated/$',
        name='duplicateddocument-list',
        view=APIDuplicatedDocumentListView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>[0-9]+)/duplicates/$',
        name='documentduplicate-list',
        view=APIDocumentDuplicateListView.as_view()
    )
]
