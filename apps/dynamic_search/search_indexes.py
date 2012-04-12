from __future__ import absolute_import

import datetime
import logging

from unidecode import unidecode
from haystack import indexes

from documents.models import Document

from .models import IndexableObject

logger = logging.getLogger(__name__)

'''
    comment = models.TextField(blank=True, verbose_name=_(u'comment'))
    checksum = models.TextField(blank=True, null=True, verbose_name=_(u'checksum'), editable=False)
    page_label = models.CharField(max_length=32, blank=True, null=True, verbose_name=_(u'page label'))
    page_number = models.PositiveIntegerField(default=1, editable=False, verbose_name=_(u'page number'), db_index=True)

    {'name': u'documentversion__documentpage__content', 'title': _(u'Content')},
    {'name': u'description', 'title': _(u'Description')},

'''

class DocumentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Document

    def build_queryset(self, start_date=None, end_date=None):
        indexable_list = IndexableObject.objects.get_indexables_pk_list()
        logger.debug('indexable list: %s' % indexable_list)
        return self.get_model().objects.filter(pk__in=indexable_list)
