from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('linking.views',
    url(r'^action/$', 'smart_link_action', (), 'smart_link_action'),
    url(r'^document/(?P<document_id>\d+)/smart_link/(?P<smart_link_pk>\d+)/$', 'smart_link_instance_view', (), 'smart_link_instance_view'),
    url(r'^smart/for_document/(?P<document_id>\d+)/$', 'smart_link_instances_for_document', (), 'smart_link_instances_for_document'),
    
    url(r'^setup/list/$', 'document_group_list', (), 'document_group_list'),
    url(r'^setup/create/$', 'document_group_create', (), 'document_group_create'),
    url(r'^setup/(?P<smart_link_pk>\d+)/delete/$', 'document_group_delete', (), 'document_group_delete'),
    url(r'^setup/(?P<smart_link_pk>\d+)/edit/$', 'document_group_edit', (), 'document_group_edit'),
    
    url(r'^setup/(?P<smart_link_pk>\d+)/condition/list/$', 'smart_link_condition_list', (), 'smart_link_condition_list'),
    url(r'^setup/(?P<smart_link_pk>\d+)/condition/create/$', 'smart_link_condition_create', (), 'smart_link_condition_create'),
    url(r'^setup/smart_link/condition/(?P<smart_link_condition_pk>\d+)/edit/$', 'smart_link_condition_edit', (), 'smart_link_condition_edit'),
    url(r'^setup/smart_link/condition/(?P<smart_link_condition_pk>\d+)/delete/$', 'smart_link_condition_delete', (), 'smart_link_condition_delete'),
)
