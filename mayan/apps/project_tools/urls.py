from __future__ import unicode_literals

from django.conf.urls import patterns, url

urlpatterns = patterns('project_tools.views',
    url(r'^list/$', 'tools_list', (), 'tools_list'),
)
