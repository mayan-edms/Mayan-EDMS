from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('checkouts.views',
    url(r'^list/$', 'checkout_list', (), 'checkout_list'),
    url(r'^(?P<document_pk>\d+)/check/out/$', 'checkout_document', (), 'checkout_document'),
    url(r'^(?P<document_pk>\d+)/check/in/$', 'checkin_document', (), 'checkin_document'),
    url(r'^(?P<document_pk>\d+)/check/info/$', 'checkout_info', (), 'checkout_info'),
)
