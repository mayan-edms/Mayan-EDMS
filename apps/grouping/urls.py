from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('grouping.views',
    url(r'^action/$', 'document_group_action', (), 'document_group_action'),
    url(r'^document/(?P<document_id>\d+)/group/(?P<document_group_id>\d+)/$', 'document_group_view', (), 'document_group_view'),
    url(r'^groups/for_document/(?P<document_id>\d+)/$', 'groups_for_document', (), 'groups_for_document'),
)
