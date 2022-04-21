from django.http import Http404
from django.utils.encoding import force_text

from .classes import SearchModel
from .literals import SEARCH_MODEL_NAME_KWARG


class SearchModelAPIViewMixin:
    def get_search_model_name(self):
        search_model_name = self.kwargs.get(
            SEARCH_MODEL_NAME_KWARG, self.request.GET.get(
                '_{}'.format(SEARCH_MODEL_NAME_KWARG), self.request.POST.get(
                    '_{}'.format(SEARCH_MODEL_NAME_KWARG)
                )
            )
        )

        if search_model_name:
            search_model_name = search_model_name.lower()

        return search_model_name

    def get_search_model(self):
        try:
            return SearchModel.get(name=self.get_search_model_name())
        except KeyError as exception:
            raise Http404(force_text(s=exception))
