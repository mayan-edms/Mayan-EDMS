from __future__ import unicode_literals

from ..models import Index

from .literals import TEST_INDEX_LABEL


class DocumentIndexingTestMixin(object):
    def _create_index(self):
        # Create empty index
        self.index = Index.objects.create(label=TEST_INDEX_LABEL)

        # Add our document type to the new index
        self.index.document_types.add(self.document_type)
