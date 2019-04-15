from __future__ import unicode_literals

from django.conf.urls import url

from .api_views import (
    APIStagingSourceFileView, APIStagingSourceFileImageView,
    APIStagingSourceListView, APIStagingSourceView
)
from .views import (
    SetupSourceCheckView, SetupSourceCreateView, SetupSourceDeleteView,
    SetupSourceEditView, SetupSourceListView, SourceLogListView,
    StagingFileDeleteView, UploadInteractiveVersionView, UploadInteractiveView
)
from .wizards import DocumentCreateWizard

urlpatterns = [
    url(
        regex=r'^staging_file/(?P<pk>\d+)/(?P<encoded_filename>.+)/delete/$',
        view=StagingFileDeleteView.as_view(), name='staging_file_delete'
    ),
    url(
        regex=r'^upload/document/new/interactive/(?P<source_id>\d+)/$',
        view=UploadInteractiveView.as_view(), name='upload_interactive'
    ),
    url(
        regex=r'^upload/document/new/interactive/$',
        view=UploadInteractiveView.as_view(), name='upload_interactive'
    ),
    url(
        regex=r'^upload/document/(?P<document_pk>\d+)/version/interactive/(?P<source_id>\d+)/$',
        view=UploadInteractiveVersionView.as_view(), name='upload_version'
    ),
    url(
        regex=r'^upload/document/(?P<document_pk>\d+)/version/interactive/$',
        view=UploadInteractiveVersionView.as_view(), name='upload_version'
    ),

    # Setup views

    url(
        regex=r'^setup/list/$', view=SetupSourceListView.as_view(),
        name='setup_source_list'
    ),
    url(
        regex=r'^setup/(?P<pk>\d+)/edit/$', view=SetupSourceEditView.as_view(),
        name='setup_source_edit'
    ),
    url(
        regex=r'^setup/(?P<pk>\d+)/logs/$', view=SourceLogListView.as_view(),
        name='setup_source_logs'
    ),
    url(
        regex=r'^setup/(?P<pk>\d+)/delete/$',
        view=SetupSourceDeleteView.as_view(), name='setup_source_delete'
    ),
    url(
        regex=r'^setup/(?P<source_type>\w+)/create/$',
        view=SetupSourceCreateView.as_view(), name='setup_source_create'
    ),
    url(
        regex=r'^setup/(?P<pk>\d+)/check/$',
        view=SetupSourceCheckView.as_view(), name='setup_source_check'
    ),

    # Document create views

    url(
        regex=r'^create/from/local/multiple/$',
        view=DocumentCreateWizard.as_view(), name='document_create_multiple'
    ),
]

api_urls = [
    url(
        regex=r'^staging_folders/file/(?P<staging_folder_pk>[0-9]+)/(?P<encoded_filename>.+)/image/$',
        view=APIStagingSourceFileImageView.as_view(),
        name='stagingfolderfile-image-view'
    ),
    url(
        regex=r'^staging_folders/file/(?P<staging_folder_pk>[0-9]+)/(?P<encoded_filename>.+)/$',
        view=APIStagingSourceFileView.as_view(), name='stagingfolderfile-detail'
    ),
    url(
        regex=r'^staging_folders/$', view=APIStagingSourceListView.as_view(),
        name='stagingfolder-list'
    ),
    url(
        regex=r'^staging_folders/(?P<pk>[0-9]+)/$',
        view=APIStagingSourceView.as_view(), name='stagingfolder-detail'
    )
]
