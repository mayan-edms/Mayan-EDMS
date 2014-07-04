from django.conf.urls import patterns, url

urlpatterns = patterns('main.views',
    url(r'^$', 'home', (), 'home'),
    url(r'^maintenance_menu/$', 'maintenance_menu', (), 'maintenance_menu'),
    url(r'^diagnostics/$', 'diagnostics_view', (), 'diagnostics'),
)
