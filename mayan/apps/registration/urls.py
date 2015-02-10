from __future__ import unicode_literals

from django.conf.urls import patterns, url

urlpatterns = patterns('registration.views',
    url(r'^form/$', 'form_view', (), 'form_view'),
)
