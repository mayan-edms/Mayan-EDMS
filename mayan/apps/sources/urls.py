from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .api_views import (
    APIStagingSourceFileView, APIStagingSourceFileImageView,
    APIStagingSourceListView, APIStagingSourceView
)
from .views import UploadInteractiveVersionView, UploadInteractiveView
from .wizards import DocumentCreateWizard

urlpatterns = patterns('sources.views',
    url(r'^staging_file/(?P<staging_folder_pk>\d+)/(?P<encoded_filename>.+)/delete/$', 'staging_file_delete', name='staging_file_delete'),

    url(r'^upload/document/new/interactive/(?P<source_id>\d+)/$', UploadInteractiveView.as_view(), name='upload_interactive'),
    url(r'^upload/document/new/interactive/$', UploadInteractiveView.as_view(), name='upload_interactive'),

    url(r'^upload/document/(?P<document_pk>\d+)/version/interactive/(?P<source_id>\d+)/$', UploadInteractiveVersionView.as_view(), name='upload_version'),
    url(r'^upload/document/(?P<document_pk>\d+)/version/interactive/$', UploadInteractiveVersionView.as_view(), name='upload_version'),

    # Setup views

    url(r'^setup/list/$', 'setup_source_list', (), 'setup_source_list'),
    url(r'^setup/(?P<source_id>\d+)/edit/$', 'setup_source_edit', (), 'setup_source_edit'),
    url(r'^setup/(?P<source_id>\d+)/delete/$', 'setup_source_delete', (), 'setup_source_delete'),
    url(r'^setup/(?P<source_type>\w+)/create/$', 'setup_source_create', (), 'setup_source_create'),

    url(r'^setup/(?P<source_id>\d+)/transformation/list/$', 'setup_source_transformation_list', (), 'setup_source_transformation_list'),
    url(r'^setup/(?P<source_id>\d+)/transformation/create/$', 'setup_source_transformation_create', (), 'setup_source_transformation_create'),
    url(r'^setup/source/transformation/(?P<transformation_id>\d+)/edit/$', 'setup_source_transformation_edit', (), 'setup_source_transformation_edit'),
    url(r'^setup/source/transformation/(?P<transformation_id>\d+)/delete/$', 'setup_source_transformation_delete', (), 'setup_source_transformation_delete'),

    # Document create views

    url(r'^create/from/local/multiple/$', DocumentCreateWizard.as_view(), name='document_create_multiple'),
    url(r'^(?P<document_id>\d+)/create/siblings/$', 'document_create_siblings', (), 'document_create_siblings'),
)

api_urls = patterns('',
    url(r'^staging_folders/file/(?P<staging_folder_pk>[0-9]+)/(?P<encoded_filename>.+)/image/$', APIStagingSourceFileImageView.as_view(), name='stagingfolderfile-image-view'),
    url(r'^staging_folders/file/(?P<staging_folder_pk>[0-9]+)/(?P<encoded_filename>.+)/$', APIStagingSourceFileView.as_view(), name='stagingfolderfile-detail'),
    url(r'^staging_folders/$', APIStagingSourceListView.as_view(), name='stagingfolder-list'),
    url(r'^staging_folders/(?P<pk>[0-9]+)/$', APIStagingSourceView.as_view(), name='stagingfolder-detail')
)
