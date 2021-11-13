from django.utils.module_loading import import_string

from mayan.apps.storage.utils import fs_cleanup, mkdtemp

from ..backends.whoosh import WhooshSearchBackend
from ..literals import DEFAULT_SEARCH_BACKEND
from ..settings import setting_backend_arguments

default_search_backend = import_string(dotted_path=DEFAULT_SEARCH_BACKEND)


class TestSearchBackend(default_search_backend):
    def __init__(self, *args, **kwargs):
        self._search_test = kwargs.pop('_search_test', False)

        kwargs = setting_backend_arguments.value.copy()

        if self._search_test:
            if issubclass(default_search_backend, WhooshSearchBackend):
                self._test_index_path = mkdtemp()
                kwargs['index_path'] = self._test_index_path

        super().__init__(*args, **kwargs)

    def _cleanup(self):
        if self._search_test:
            if issubclass(default_search_backend, WhooshSearchBackend):
                fs_cleanup(filename=self._test_index_path)

    def deindex_instance(self, instance):
        if self._search_test:
            super().deindex_instance(instance=instance)

    def index_instance(self, instance):
        if self._search_test:
            super().index_instance(instance=instance)
