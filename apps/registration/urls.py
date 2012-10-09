from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('registration.views',
    url(r'^form/$', 'form_view', (), 'form_view'),
)
