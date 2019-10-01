from __future__ import unicode_literals

from ..literals import SOURCE_CHOICE_WEB_FORM
from ..models import WebFormSource

from .literals import TEST_SOURCE_LABEL, TEST_SOURCE_UNCOMPRESS_N


class SourceTestMixin(object):
    def _create_test_source(self):
        self.test_source = WebFormSource.objects.create(
            enabled=True, label=TEST_SOURCE_LABEL,
            uncompress=TEST_SOURCE_UNCOMPRESS_N
        )


class SourceViewTestMixin(object):
    def _request_setup_source_list_view(self):
        return self.get(viewname='sources:setup_source_list')

    def _request_setup_source_create_view(self):
        return self.post(
            kwargs={'source_type': SOURCE_CHOICE_WEB_FORM},
            viewname='sources:setup_source_create', data={
                'enabled': True, 'label': TEST_SOURCE_LABEL,
                'uncompress': TEST_SOURCE_UNCOMPRESS_N
            }
        )

    def _request_setup_source_delete_view(self):
        return self.post(
            viewname='sources:setup_source_delete',
            kwargs={'pk': self.test_source.pk}
        )
