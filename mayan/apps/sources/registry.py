from __future__ import absolute_import

from django.conf.urls import url

from .cleanup import cleanup


cleanup_functions = [cleanup]

#version_0_api_services = [
#    #{'urlpattern': url(r'^staging_file/(?P<pk>[0-9]+)/image/$', APIStagingSourceView.as_view(), name='staging-file-image'), 'description': 'Return a base64 image of the staging file', 'url': 'staging_file/<staging file ID>/image/?page=<page number>&zoom=<zoom percent>&rotate=<rotation degrees>'},
#    {'urlpattern': url(r'^staging_folder/(?P<pk>[0-9]+)/$', APIStagingSourceView.as_view(), name='staging-source-list'), 'description': '', 'url': 'staging_file/<staging file ID>/image/?page=<page number>&zoom=<zoom percent>&rotate=<rotation degrees>'},
#]

