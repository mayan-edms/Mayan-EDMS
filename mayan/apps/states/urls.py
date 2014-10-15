from django.conf.urls import patterns, url


urlpatterns = patterns('states.views',
    # Setup views

    url(r'^setup/document_type/(?P<document_type_id>\d+)/collections/$', 'setup_source_list', name='document_type_collection_list'),

    #url(r'^setup/interactive/(?P<source_type>\w+)/list/$', 'setup_source_list', (), 'setup_source_list'),
    #url(r'^setup/interactive/(?P<source_id>\d+)/edit/$', 'setup_source_edit', (), 'setup_source_edit'),
    #url(r'^setup/interactive/(?P<source_id>\d+)/delete/$', 'setup_source_delete', (), 'setup_source_delete'),
    #url(r'^setup/interactive/(?P<source_type>\w+)/create/$', 'setup_source_create', (), 'setup_source_create'),
    #url(r'^setup/interactive/(?P<source_id>\d+)/transformation/list/$', 'setup_source_transformation_list', (), 'setup_source_transformation_list'),
    #url(r'^setup/interactive/(?P<source_id>\d+)/transformation/create/$', 'setup_source_transformation_create', (), 'setup_source_transformation_create'),
    #url(r'^setup/interactive/source/transformation/(?P<transformation_id>\d+)/edit/$', 'setup_source_transformation_edit', (), 'setup_source_transformation_edit'),
    #url(r'^setup/interactive/source/transformation/(?P<transformation_id>\d+)/delete/$', 'setup_source_transformation_delete', (), 'setup_source_transformation_delete'),

    # Document create views

    #url(r'^create/from/local/multiple/$', DocumentCreateWizard.as_view(), name='document_create_multiple'),
    #url(r'^(?P<document_id>\d+)/create/siblings/$', 'document_create_siblings', (), 'document_create_siblings'),
)
