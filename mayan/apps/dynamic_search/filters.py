import logging
import operator

from django.conf import settings

from rest_framework.filters import BaseFilterBackend

from .classes import SearchBackend, SearchModel
from .exceptions import DynamicSearchException
from .literals import QUERY_PARAMETER_ANY_FIELD
from .utils import get_match_all_value

logger = logging.getLogger(name=__name__)


class RESTAPISearchFilter(BaseFilterBackend):
    def get_search_model(self, queryset):
        try:
            model = queryset.model
        except AttributeError:
            return
        else:
            try:
                return SearchModel.get_for_model(instance=model)
            except KeyError:
                return

    def filter_queryset(self, request, queryset, view):
        if not getattr(view, 'search_disable_list_filtering', False):
            search_model = self.get_search_model(queryset=queryset)
            if search_model:
                query_dict = request.GET.dict().copy()
                query_dict.update(request.POST.dict())

                global_and_search = get_match_all_value(
                    value=query_dict.get('_match_all')
                )

                search_model_fields = list(
                    map(
                        operator.itemgetter(0),
                        search_model.get_fields_simple_list()
                    )
                )

                search_model_fields.append(QUERY_PARAMETER_ANY_FIELD)

                valid_search_models_query_dict_keys = set(
                    query_dict.keys()
                ).intersection(
                    set(search_model_fields)
                )

                query_dict_cleaned = {
                    key: query_dict[key] for key in valid_search_models_query_dict_keys
                }

                if query_dict_cleaned:
                    try:
                        search_queryset = SearchBackend.get_instance().search(
                            global_and_search=global_and_search,
                            search_model=search_model,
                            query=query_dict_cleaned, user=request.user
                        )
                    except DynamicSearchException as exception:
                        if settings.DEBUG or settings.TESTING:
                            raise

                        logger.error(
                            'Error performing REST API list search filtering; %s',
                            exception
                        )
                        return search_model.model._meta.default_manager.none()
                    else:
                        return queryset.filter(pk__in=search_queryset)
                else:
                    return queryset
            else:
                return queryset
        else:
            return queryset
