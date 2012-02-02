from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('feedback.views',
    url(r'^form/$', 'form_view', (), 'form_view'),
)
