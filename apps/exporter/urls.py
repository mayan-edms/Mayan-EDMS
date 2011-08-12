from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('exporter.views',
    url(r'^export_test/$', 'export_test', (), 'export_test'),
)
