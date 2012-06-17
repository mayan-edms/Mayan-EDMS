from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('installation.views',
    url(r'^details/$', 'installation_details', (), 'installation_details'),
)
