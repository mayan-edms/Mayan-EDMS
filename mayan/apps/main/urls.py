from __future__ import unicode_literals

from django.conf.urls import patterns, url
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.views.generic import RedirectView

urlpatterns = patterns('main.views',
    url(r'^$', 'home', (), 'home'),
    url(r'^maintenance_menu/$', 'maintenance_menu', (), 'maintenance_menu'),
)

urlpatterns += patterns('',
    (r'^favicon\.ico$', RedirectView.as_view(url=static('appearance/images/favicon.ico'))),
)
