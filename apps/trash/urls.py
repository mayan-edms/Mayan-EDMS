from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('trash.views',
    url(r'^list/$', 'trash_can_list', (), 'trash_can_list'),
    url(r'^trash_can/(?P<trash_can_pk>\d+)/items/$', 'trash_can_items', (), 'trash_can_items'),
    url(r'^trash_can/item/(?P<trash_can_item_pk>\d+)/restore/$', 'trash_can_item_restore', (), 'trash_can_item_restore'),
    url(r'^trash_can/item/(?P<trash_can_item_pk>\d+)/delete/$', 'trash_can_item_delete', (), 'trash_can_item_delete'),
)
