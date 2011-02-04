from django.conf.urls.defaults import *
                           

urlpatterns = patterns('dynamic_search.views',
    url(r'^search/$', 'search', (), 'search'),
)
    

