from __future__ import absolute_import

import logging
import copy

from haystack import indexes

from documents.models import Document

from .models import IndexableObject

logger = logging.getLogger(__name__)


class DocumentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Document

    def build_queryset(self, start_date=None, end_date=None):
        indexable_query_set = IndexableObject.objects.get_indexables()
        logger.debug('indexable_query_set: %s' % indexable_query_set)
        object_list = copy.copy(self.get_model().objects.filter(pk__in=indexable_query_set.values_list('object_id', flat=True)))
        logger.debug('object_list: %s' % object_list)
        indexable_query_set.delete()
        return object_list
