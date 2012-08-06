from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('diagnostics.views',
    url(r'^$', 'diagnostic_list', (), 'diagnostic_list'),
    url(r'^execute/(?P<diagnostic_tool_id>\w+)/$', 'diagnostic_execute', (), 'diagnostic_execute'),
)
