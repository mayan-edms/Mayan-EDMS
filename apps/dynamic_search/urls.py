from django.conf.urls.defaults import patterns, url

from haystack.forms import SearchForm

from .views import CustomSearchView

urlpatterns = patterns('dynamic_search.views',
    url(r'^$', CustomSearchView(form_class=SearchForm), (), 'search'),
    url(r'^advanced/$', 'search', {'advanced': True}, 'search_advanced'),
    url(r'^again/$', 'search_again', (), 'search_again'),
    url(r'^results/$', 'results', (), 'results'),
)
