from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('scheduler.views',
    url(r'^list/$', 'job_list', (), 'job_list'),
)
