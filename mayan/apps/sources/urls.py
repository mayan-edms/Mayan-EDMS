from django.conf.urls import url

from .api_views import APISourceActionView, APISourceListView, APISourceView
from .views.document_file_views import DocumentFileUploadInteractiveView
from .views.document_views import DocumentUploadInteractiveView
from .views.source_views import (
    SourceActionView, SourceBackendSelectionView, SourceCreateView,
    SourceDeleteView, SourceEditView, SourceListView, SourceTestView
)
from .wizards import DocumentCreateWizard

urlpatterns = [
    # Document create views

    url(
        regex=r'^documents/create/from/local/multiple/$',
        name='document_create_multiple', view=DocumentCreateWizard.as_view()
    ),
    url(
        regex=r'^documents/upload/new/interactive/(?P<source_id>\d+)/$',
        name='document_upload_interactive',
        view=DocumentUploadInteractiveView.as_view()
    ),
    url(
        regex=r'^documents/upload/new/interactive/$',
        name='document_upload_interactive',
        view=DocumentUploadInteractiveView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>\d+)/files/upload/interactive/(?P<source_id>\d+)/$',
        name='document_file_upload',
        view=DocumentFileUploadInteractiveView.as_view()
    ),
    url(
        regex=r'^documents/(?P<document_id>\d+)/files/upload/interactive/$',
        name='document_file_upload',
        view=DocumentFileUploadInteractiveView.as_view()
    ),

    # Setup views

    url(
        regex=r'^sources/$', name='source_list',
        view=SourceListView.as_view()
    ),
    url(
        regex=r'^sources/backend/selection/$',
        name='source_backend_selection',
        view=SourceBackendSelectionView.as_view()
    ),
    url(
        regex=r'^sources/(?P<backend_path>[a-zA-Z0-9_.]+)/create/$',
        name='source_create', view=SourceCreateView.as_view()
    ),
    url(
        regex=r'^sources/(?P<source_id>\d+)/actions/(?P<action_name>[a-zA-Z0-9_.]+)/$',
        name='source_action', view=SourceActionView.as_view()
    ),
    url(
        regex=r'^sources/(?P<source_id>\d+)/delete/$',
        name='source_delete', view=SourceDeleteView.as_view()
    ),
    url(
        regex=r'^sources/(?P<source_id>\d+)/edit/$', name='source_edit',
        view=SourceEditView.as_view()
    ),
    url(
        regex=r'^sources/(?P<source_id>\d+)/test/$',
        name='source_test', view=SourceTestView.as_view()
    ),
]

api_urls = [
    url(
        regex=r'^sources/$', name='source-list',
        view=APISourceListView.as_view()
    ),
    url(
        regex=r'^sources/(?P<source_id>[0-9]+)/$',
        name='source-detail', view=APISourceView.as_view()
    ),
    url(
        regex=r'^sources/(?P<source_id>[0-9]+)/actions/(?P<action_name>[a-zA-Z0-9_.]+)/$',
        name='source-action', view=APISourceActionView.as_view()
    )
]
