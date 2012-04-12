from django.conf.urls.defaults import patterns, url

from haystack.forms import SearchForm

from .views import CustomSearchView

urlpatterns = patterns('dynamic_search.views',
    url(r'^$', CustomSearchView(form_class=SearchForm), (), 'search'),
)
