from __future__ import absolute_import

import datetime

from unidecode import unidecode
from haystack import indexes

from documents.models import Document

from .models import IndexableObject

'''
    comment = models.TextField(blank=True, verbose_name=_(u'comment'))
    checksum = models.TextField(blank=True, null=True, verbose_name=_(u'checksum'), editable=False)
    page_label = models.CharField(max_length=32, blank=True, null=True, verbose_name=_(u'page label'))
    page_number = models.PositiveIntegerField(default=1, editable=False, verbose_name=_(u'page number'), db_index=True)

# Register the fields that will be searchable
register('document', Document, _(u'document'), [
    {'name': u'document_type__name', 'title': _(u'Document type')},
    {'name': u'documentversion__mimetype', 'title': _(u'MIME type')},
    {'name': u'documentversion__filename', 'title': _(u'Filename')},
    {'name': u'documentmetadata__value', 'title': _(u'Metadata value')},
    {'name': u'documentversion__documentpage__content', 'title': _(u'Content')},
    {'name': u'description', 'title': _(u'Description')},
    {'name': u'tags__name', 'title': _(u'Tags')},
    {'name': u'comments__comment', 'title': _(u'Comments')},
    ]
)
#register(Document, _(u'document'), ['document_type__name', 'file_mimetype', 'documentmetadata__value', 'documentpage__content', 'description', {'field_name':'file_filename', 'comparison':'iexact'}])

'''

class DocumentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Document

    def build_queryset(self, start_date=None, end_date=None):
        print  "DIRTY", IndexableObject.objects.get_dirty_pk_list()
        
        #return self.get_model().objects.filter(date_added__lte=datetime.datetime.now())
        return self.get_model().objects.filter(pk__in=IndexableObject.objects.get_dirty_pk_list())
        #return self.get_model().objects.all()
