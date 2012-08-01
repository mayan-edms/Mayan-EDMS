from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('job_processor.views',
    url(r'^node/(?P<node_pk>\d+)/workers/$', 'node_workers', (), 'node_workers'),
    url(r'^queue/list/$', 'job_queues', (), 'job_queues'),
    url(r'^queue/(?P<job_queue_pk>\d+)/items/pending/$', 'job_queue_items', {'pending_jobs': True}, 'job_queue_items_pending'),
    url(r'^queue/(?P<job_queue_pk>\d+)/items/error/$', 'job_queue_items', {'error_jobs' :True}, 'job_queue_items_error'),
    url(r'^queue/(?P<job_queue_pk>\d+)/items/active/$', 'job_queue_items', {'active_jobs' :True}, 'job_queue_items_active'),
    url(r'^config/edit/$', 'job_queue_config_edit', (), 'job_queue_config_edit'),
)
