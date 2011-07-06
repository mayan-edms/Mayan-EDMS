from django.conf.urls.defaults import patterns, url

#from converter.api import QUALITY_HIGH, QUALITY_PRINT

#from documents.conf.settings import PREVIEW_SIZE
#from documents.conf.settings import PRINT_SIZE
#from documents.conf.settings import THUMBNAIL_SIZE
#from documents.conf.settings import DISPLAY_SIZE
#from documents.conf.settings import MULTIPAGE_PREVIEW_SIZE
#from documents.literals import UPLOAD_SOURCE_LOCAL, \
#    UPLOAD_SOURCE_STAGING, UPLOAD_SOURCE_USER_STAGING

urlpatterns = patterns('sources.views',
    #url(r'^upload/local/$', 'upload_document_with_type', {'source': UPLOAD_SOURCE_LOCAL}, 'upload_document_from_local'),
    #url(r'^upload/staging/$', 'upload_document_with_type', {'source': UPLOAD_SOURCE_STAGING}, 'upload_document_from_staging'),
    #url(r'^upload/staging/user/$', 'upload_document_with_type', {'source': UPLOAD_SOURCE_USER_STAGING}, 'upload_document_from_user_staging'),

    url(r'^staging_file/type/(?P<source_type>\w+)/(?P<source_id>\d+)/(?P<staging_file_id>\w+)/preview/$', 'staging_file_preview', (), 'staging_file_preview'),
    url(r'^staging_file/type/(?P<source_type>\w+)/(?P<source_id>\d+)/(?P<staging_file_id>\w+)/delete/$', 'staging_file_delete', (), 'staging_file_delete'),

    url(r'^upload/interactive/(?P<source_type>\w+)/(?P<source_id>\d+)/$', 'upload_interactive', (), 'upload_interactive'),
    url(r'^upload/interactive/$', 'upload_interactive', (), 'upload_interactive'),
)
