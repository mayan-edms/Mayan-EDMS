from __future__ import unicode_literals

from django.conf.urls import patterns, url

urlpatterns = patterns('project_setup.views',
    url(r'^list/$', 'setup_list', (), 'setup_list'),
)
