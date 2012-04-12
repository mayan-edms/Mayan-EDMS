from __future__ import absolute_import

import logging

from haystack import indexes

from documents.models import Document

from .models import IndexableObject

logger = logging.getLogger(__name__)


class DocumentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Document

    def build_queryset(self, start_date=None, end_date=None):
        indexable_list = IndexableObject.objects.get_indexables_pk_list()
        logger.debug('indexable list: %s' % indexable_list)
        return self.get_model().objects.filter(pk__in=indexable_list)
