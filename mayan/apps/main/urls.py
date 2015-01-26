from __future__ import unicode_literals

from django.conf.urls import patterns, url
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.views.generic import RedirectView

urlpatterns = patterns('main.views',
    url(r'^$', 'home', (), 'home'),
    url(r'^maintenance_menu/$', 'maintenance_menu', (), 'maintenance_menu'),
    url(r'^diagnostics/$', 'diagnostics_view', (), 'diagnostics'),
)

urlpatterns += patterns('',
    (r'^favicon\.ico$', RedirectView.as_view(url=static('main/images/favicon.ico'))),
)
