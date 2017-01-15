from __future__ import unicode_literals

from django.http import Http404

from .classes import SearchModel


class SearchModelMixin(object):
    def get_search_model(self):
        try:
            return SearchModel.get(self.kwargs['search_model'])
        except KeyError as exception:
            raise Http404(unicode(exception))
