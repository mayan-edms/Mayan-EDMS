from __future__ import absolute_import

import datetime

from unidecode import unidecode
from haystack import indexes

from .models import Document

'''
    uuid = models.CharField(max_length=48, blank=True, editable=False)
    document_type = models.ForeignKey(DocumentType, verbose_name=_(u'document type'), null=True, blank=True)
    description = models.TextField(blank=True, null=True, verbose_name=_(u'description'))
    date_added = models.DateTimeField(verbose_name=_(u'added'), db_index=True, editable=False)
    document = models.ForeignKey(Document, verbose_name=_(u'document'), editable=False)
    major = models.PositiveIntegerField(verbose_name=_(u'mayor'), default=1, editable=False)
    minor = models.PositiveIntegerField(verbose_name=_(u'minor'), default=0, editable=False)
    micro = models.PositiveIntegerField(verbose_name=_(u'micro'), default=0, editable=False)
    release_level = models.PositiveIntegerField(choices=RELEASE_LEVEL_CHOICES, default=RELEASE_LEVEL_FINAL, verbose_name=_(u'release level'), editable=False)
    serial = models.PositiveIntegerField(verbose_name=_(u'serial'), default=0, editable=False)
    timestamp = models.DateTimeField(verbose_name=_(u'timestamp'), editable=False)
    comment = models.TextField(blank=True, verbose_name=_(u'comment'))

    # File related fields
    file = models.FileField(upload_to=get_filename_from_uuid, storage=STORAGE_BACKEND(), verbose_name=_(u'file'))
    mimetype = models.CharField(max_length=64, default='', editable=False)
    encoding = models.CharField(max_length=64, default='', editable=False)
    filename = models.CharField(max_length=255, default=u'', editable=False, db_index=True)
    checksum = models.TextField(blank=True, null=True, verbose_name=_(u'checksum'), editable=False)

class DocumentPage(models.Model):
    """
    Model that describes a document version page including it's content
    """
    document_version = models.ForeignKey(DocumentVersion, verbose_name=_(u'document version'))
    content = models.TextField(blank=True, null=True, verbose_name=_(u'content'))
    page_label = models.CharField(max_length=32, blank=True, null=True, verbose_name=_(u'page label'))
    page_number = models.PositiveIntegerField(default=1, editable=False, verbose_name=_(u'page number'), db_index=True)


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
'''

class DocumentIndex(indexes.SearchIndex, indexes.Indexable):
    # Content
    text = indexes.CharField(document=True, use_template=True)
    # filename
    filename = indexes.CharField(model_attr='filename', boost=1.125)
    cleaned_filename = indexes.CharField(model_attr='filename', boost=1.125)
    # description
    #description = indexes.CharField(null=True, model_attr='description')
    # tags
    #tags = indexes.CharField(null=True, model_attr='tags')
    
    
    #date_added = indexes.DateTimeField(model_attr='date_added')

    def get_model(self):
        return Document

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        #return self.get_model().objects.filter(date_added__lte=datetime.datetime.now())
        return self.get_model().objects.filter(pk__lte=300)

    def prepare_cleaned_filename(self, obj):
        #print 'CLEAN'
        return unidecode(obj.filename)
        #print "1,2: %s - %s" % (obj.filename, after)
        #return after
