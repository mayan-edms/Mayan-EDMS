from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('mailer.views',
    url(r'^(?P<document_id>\d+)/send/link/$', 'send_document_link', (), 'send_document_link'),
)
