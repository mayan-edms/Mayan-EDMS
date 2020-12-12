DEFAULT_SEARCH_BACKEND = 'mayan.apps.dynamic_search.backends.django.DjangoSearchBackend'
DEFAULT_SEARCH_BACKEND_ARGUMENTS = {}
DEFAULT_SEARCH_DISABLE_SIMPLE_SEARCH = False
DEFAULT_SEARCH_RESULTS_LIMIT = 100

# Duplicated to keep API compatible until version 4.0
# Merge these two literals and mixins on version 4.0
SEARCH_MODEL_NAME_API_KWARG = 'search_model'
SEARCH_MODEL_NAME_KWARG = 'search_model_name'
TASK_RETRY_DELAY = 5
