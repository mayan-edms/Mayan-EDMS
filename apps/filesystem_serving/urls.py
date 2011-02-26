from django.conf.urls.defaults import *

urlpatterns = patterns('filesystem_serving.views',
    url(r'^recreate_all_links/$', 'recreate_all_links', (), 'recreate_all_links'),
)
