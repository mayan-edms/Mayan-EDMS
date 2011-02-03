from django.conf.urls.defaults import *


urlpatterns = patterns('main.views',
    url(r'^$', 'home', (), 'home'),
)
