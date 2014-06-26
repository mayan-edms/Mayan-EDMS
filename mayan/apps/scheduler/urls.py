from django.conf.urls import patterns, url

urlpatterns = patterns('scheduler.views',
    url(r'^list/$', 'job_list', (), 'job_list'),
)
