from django.db import models
from django.utils.translation import ugettext_lazy as _

from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey

from documents.models import Document

from document_indexing.conf.settings import AVAILABLE_INDEXING_FUNCTIONS

available_indexing_functions_string = (_(u'Available functions: %s') % u','.join([u'%s()' % name for name, function in AVAILABLE_INDEXING_FUNCTIONS.items()])) if AVAILABLE_INDEXING_FUNCTIONS else u''


class Index(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='index_meta_class')
    expression = models.CharField(max_length=128, verbose_name=_(u'indexing expression'), help_text=_(u'Enter a python string expression to be evaluated.'))
        # % available_indexing_functions_string)
    enabled = models.BooleanField(default=True, verbose_name=_(u'enabled'))
    link_documents = models.BooleanField(default=False, verbose_name=_(u'link documents'))
    
    def __unicode__(self):
        return self.expression if not self.link_documents else u'%s/[document]' % self.expression

    class Meta:
        verbose_name = _(u'index')
        verbose_name_plural = _(u'indexes')


class IndexInstance(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='index_meta_instance')
    index = models.ForeignKey(Index, verbose_name=_(u'index'))
    value = models.CharField(max_length=128, blank=True, verbose_name=_(u'value'))
    documents = models.ManyToManyField(Document, verbose_name=_(u'documents'))
    
    def __unicode__(self):
        return self.value

    @models.permalink
    def get_absolute_url(self):
        return ('index_instance_list', [self.pk])

    def get_document_list_display(self):
        return u', '.join([d.file_filename for d in self.documents.all()])

    class Meta:
        verbose_name = _(u'index instance')
        verbose_name_plural = _(u'indexes instances')

'''
class DocumentRenameCount(models.Model):
    index = models.ForeignKey(IndexInstance, verbose_name=_(u'index instance'))
    document = models.ForeignKey(Document, verbose_name=_(u'document'))
    count = models.PositiveIntegerField(blank=True, verbose_name=(u'count'))

    def __unicode__(self):
        return self.value

    class Meta:
        verbose_name = _(u'document rename count')
        verbose_name_plural = _(u'documents rename count')
'''
