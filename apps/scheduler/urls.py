from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('scheduler.views',
    url(r'^scheduler/list/$', 'scheduler_list', (), 'scheduler_list'),
    url(r'^scheduler/(?P<scheduler_name>\w+)/job/list/$', 'job_list', (), 'job_list'),
)
