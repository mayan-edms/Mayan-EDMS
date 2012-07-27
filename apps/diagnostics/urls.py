from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('diagnostics.views',
    url(r'^$', 'diagnostics_view', (), 'diagnostics'),
)
