from django.utils.module_loading import import_string

from mayan.apps.storage.utils import TemporaryDirectory

from ..classes import SearchBackend
from ..backends.elasticsearch import ElasticSearchBackend
from ..backends.whoosh import WhooshSearchBackend
from ..literals import DEFAULT_SEARCH_BACKEND
from ..settings import setting_backend_arguments


class TestSearchBackend(SearchBackend):
    """
    Test search backend dynamically generated from the default search
    backend. If the default backend is the Whoosh backend, a temporary
    folder will be created to store the search index. The temporary directory
    is automatically deleted by Python when all references are removed.

    This test search backend will only perform instance indexing and
    deindexing when called from a search test. This allows using the backend
    for search tests but avoids the indexing penalty for non search tests.

    It will also automatically insert the test object into the index
    before performing a call to the `search` method.
    """
    _test_backend_initialized = False
    _test_backend_path = None
    _test_class = None

    def __init__(self, *args, **kwargs):
        if self._test_class:
            backend_path = getattr(self._test_class, '_test_search_backend_path', DEFAULT_SEARCH_BACKEND)
        else:
            backend_path = DEFAULT_SEARCH_BACKEND
            SearchBackend._disable()

        if self.__class__._test_backend_path != backend_path:
            self.__class__._test_backend_path = backend_path

            self.__class__._backend_kwargs = setting_backend_arguments.value.copy()
            self.__class__._backend_class = import_string(dotted_path=backend_path)

            if issubclass(self._backend_class, WhooshSearchBackend):
                if not hasattr(self.__class__, '_local_attribute_backend_temporary_directory'):
                    self.__class__._local_attribute_backend_temporary_directory = TemporaryDirectory()

                self.__class__._backend_kwargs['index_path'] = self._local_attribute_backend_temporary_directory.name
            elif issubclass(self._backend_class, ElasticSearchBackend):
                self.__class__._backend_kwargs['indices_namespace'] = 'test'

            self.__class__._test_backend_initialized = False

        self.__class__._backend = self._backend_class(**self.__class__._backend_kwargs)

        if not self.__class__._test_backend_initialized:
            self.__class__._test_backend_initialized = True
            self._backend._initialize()
            SearchBackend._search_field_transformations = {}

        super().__init__(*args, **kwargs)

    def _search(self, *args, **kwargs):
        return self._backend._search(*args, **kwargs)

    def deindex_instance(self, *args, **kwargs):
        if self._test_class:
            return self._backend.deindex_instance(*args, **kwargs)

    def get_status(self, *args, **kwargs):
        return self._backend.get_status(*args, **kwargs)

    def index_instance(self, *args, **kwargs):
        if self._test_class:
            return self._backend.index_instance(*args, **kwargs)

    def index_search_model(self, *args, **kwargs):
        return self._backend.index_search_model(*args, **kwargs)

    def reset(self, *args, **kwargs):
        return self._backend.reset(*args, **kwargs)

    def tear_down(self):
        self.__class__._test_backend_path = None
        return self._backend.tear_down()
