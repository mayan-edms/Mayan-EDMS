from __future__ import absolute_import

import datetime

from unidecode import unidecode
from haystack import indexes

from documents.models import Document

'''
    date_added = models.DateTimeField(verbose_name=_(u'added'), db_index=True, editable=False)
    document = models.ForeignKey(Document, verbose_name=_(u'document'), editable=False)
    major = models.PositiveIntegerField(verbose_name=_(u'mayor'), default=1, editable=False)
    minor = models.PositiveIntegerField(verbose_name=_(u'minor'), default=0, editable=False)
    micro = models.PositiveIntegerField(verbose_name=_(u'micro'), default=0, editable=False)
    release_level = models.PositiveIntegerField(choices=RELEASE_LEVEL_CHOICES, default=RELEASE_LEVEL_FINAL, verbose_name=_(u'release level'), editable=False)
    serial = models.PositiveIntegerField(verbose_name=_(u'serial'), default=0, editable=False)
    timestamp = models.DateTimeField(verbose_name=_(u'timestamp'), editable=False)
    comment = models.TextField(blank=True, verbose_name=_(u'comment'))

    checksum = models.TextField(blank=True, null=True, verbose_name=_(u'checksum'), editable=False)

    page_label = models.CharField(max_length=32, blank=True, null=True, verbose_name=_(u'page label'))
    page_number = models.PositiveIntegerField(default=1, editable=False, verbose_name=_(u'page number'), db_index=True)
'''

class DocumentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    #fractional_filename = indexes.CharField(model_attr='filename')#, boost=1.125)
    cleaned_filename = indexes.CharField(model_attr='filename')#, boost=1.125)

    def get_model(self):
        return Document

    #def index_queryset(self):
    #    """Used when the entire index for model is updated."""
    #    #return self.get_model().objects.filter(date_added__lte=datetime.datetime.now())
    #    return self.get_model().objects.filter(pk__lte=3000)

    #def prepare_cleaned_filename(self, obj):
    #    #print 'CLEAN'
    #    return 'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq'
    #    return unidecode(obj.filename)
    #    #print "1,2: %s - %s" % (obj.filename, after)
    #    #return after
