from django.conf.urls.defaults import patterns, url

from .views import CustomSearchView

urlpatterns = patterns('dynamic_search.views',
    url(r'^$', CustomSearchView(), (), 'search'),
    url(r'^advanced/$', 'search', {'advanced': True}, 'search_advanced'),
    url(r'^again/$', 'search_again', (), 'search_again'),
    url(r'^results/$', 'results', (), 'results'),
)
