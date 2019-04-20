from __future__ import unicode_literals

from ..models import Index

from .literals import TEST_INDEX_LABEL


class DocumentIndexingTestMixin(object):
    def _create_test_index(self, rebuild=False):
        # Create empty index
        self.test_index = Index.objects.create(label=TEST_INDEX_LABEL)

        # Add our document type to the new index
        self.test_index.document_types.add(self.test_document_type)

        # Rebuild indexes
        if rebuild:
            Index.objects.rebuild()
