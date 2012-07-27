from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('maintenance.views',
    url(r'^$', 'maintenance_menu', (), 'maintenance_menu'),
)
