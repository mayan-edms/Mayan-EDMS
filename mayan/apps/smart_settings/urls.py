from __future__ import unicode_literals

from django.conf.urls import patterns, url

urlpatterns = patterns(
    'smart_settings.views',
    url(r'^list/$', 'setting_list', name='setting_list'),
)
