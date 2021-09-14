from ...source_backends.literals import SOURCE_UNCOMPRESS_CHOICE_NEVER
from ...source_backends.web_form_backends import SourceBackendWebForm

from .base_mixins import SourceTestMixin


class WebFormSourceTestMixin(SourceTestMixin):
    _create_source_method = '_create_test_web_form_source'

    def _create_test_web_form_source(self, extra_data=None):
        backend_data = {'uncompress': SOURCE_UNCOMPRESS_CHOICE_NEVER}

        if extra_data:
            backend_data.update(extra_data)

        self._create_test_source(
            backend_path=SourceBackendWebForm.get_class_path(),
            backend_data=backend_data
        )
