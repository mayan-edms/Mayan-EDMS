from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('backups.views',
    url(r'^backup/$', 'backup_view', (), 'backup_view'),
)
