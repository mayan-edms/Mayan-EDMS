from __future__ import absolute_import

from django.conf.urls.defaults import patterns, url

from .literals import (SOURCE_CHOICE_WEB_FORM, SOURCE_CHOICE_STAGING,
    SOURCE_CHOICE_WATCH, SOURCE_CHOICE_POP3_EMAIL, SOURCE_CHOICE_IMAP_EMAIL,
    SOURCE_CHOICE_LOCAL_SCANNER)

urlpatterns = patterns('sources.views',
    url(r'^create/from/local/multiple/$', 'document_create', (), 'document_create_multiple'),

    url(r'^staging_file/type/(?P<source_type>\w+)/(?P<source_id>\d+)/(?P<staging_file_id>\w+)/preview/$', 'staging_file_preview', (), 'staging_file_preview'),
    url(r'^staging_file/type/(?P<source_type>\w+)/(?P<source_id>\d+)/(?P<staging_file_id>\w+)/delete/$', 'staging_file_delete', (), 'staging_file_delete'),
    url(r'^staging_file/type/staging_folder/(?P<source_id>\d+)/(?P<staging_file_id>\w+)/thumbnail/$', 'staging_file_thumbnail', (), 'staging_file_thumbnail'),

    url(r'^upload/document/new/interactive/(?P<source_type>\w+)/(?P<source_id>\d+)/$', 'upload_interactive', (), 'upload_interactive'),
    url(r'^upload/document/new/interactive/$', 'upload_interactive', (), 'upload_interactive'),

    url(r'^upload/document/(?P<document_pk>\d+)/version/interactive/(?P<source_type>\w+)/(?P<source_id>\d+)/$', 'upload_interactive', (), 'upload_version'),
    url(r'^upload/document/(?P<document_pk>\d+)/version/interactive/$', 'upload_interactive', (), 'upload_version'),

    #Setup views

    url(r'^setup/interactive/%s/list/$' % SOURCE_CHOICE_WEB_FORM, 'setup_source_list', {'source_type': SOURCE_CHOICE_WEB_FORM}, 'setup_web_form_list'),
    url(r'^setup/interactive/%s/list/$' % SOURCE_CHOICE_STAGING, 'setup_source_list', {'source_type': SOURCE_CHOICE_STAGING}, 'setup_staging_folder_list'),
    url(r'^setup/interactive/%s/list/$' % SOURCE_CHOICE_WATCH, 'setup_source_list', {'source_type': SOURCE_CHOICE_WATCH}, 'setup_watch_folder_list'),
    url(r'^setup/interactive/%s/list/$' % SOURCE_CHOICE_POP3_EMAIL, 'setup_source_list', {'source_type': SOURCE_CHOICE_POP3_EMAIL}, 'setup_pop3_email_list'),
    url(r'^setup/interactive/%s/list/$' % SOURCE_CHOICE_IMAP_EMAIL, 'setup_source_list', {'source_type': SOURCE_CHOICE_IMAP_EMAIL}, 'setup_imap_email_list'),
    url(r'^setup/interactive/%s/list/$' % SOURCE_CHOICE_LOCAL_SCANNER, 'setup_source_list', {'source_type': SOURCE_CHOICE_LOCAL_SCANNER}, 'setup_local_scanner_list'),
    url(r'^setup/interactive/%s/refresh/$' % SOURCE_CHOICE_LOCAL_SCANNER, 'scanners_refresh', (), 'scanners_refresh'),

    url(r'^setup/interactive/(?P<source_type>\w+)/list/$', 'setup_source_list', (), 'setup_source_list'),
    url(r'^setup/interactive/(?P<source_type>\w+)/(?P<source_id>\d+)/edit/$', 'setup_source_edit', (), 'setup_source_edit'),
    url(r'^setup/interactive/(?P<source_type>\w+)/(?P<source_id>\d+)/delete/$', 'setup_source_delete', (), 'setup_source_delete'),
    url(r'^setup/interactive/(?P<source_type>\w+)/create/$', 'setup_source_create', (), 'setup_source_create'),

    url(r'^setup/interactive/(?P<source_type>\w+)/(?P<source_id>\d+)/transformation/list/$', 'setup_source_transformation_list', (), 'setup_source_transformation_list'),
    url(r'^setup/interactive/(?P<source_type>\w+)/(?P<source_id>\d+)/transformation/create/$', 'setup_source_transformation_create', (), 'setup_source_transformation_create'),
    url(r'^setup/interactive/source/transformation/(?P<transformation_id>\d+)/edit/$', 'setup_source_transformation_edit', (), 'setup_source_transformation_edit'),
    url(r'^setup/interactive/source/transformation/(?P<transformation_id>\d+)/delete/$', 'setup_source_transformation_delete', (), 'setup_source_transformation_delete'),

    url(r'^setup/source/(?P<source_type>\w+)/(?P<source_pk>\d+)/log/list/$', 'setup_source_log_list', (), 'setup_source_log_list'),
)
