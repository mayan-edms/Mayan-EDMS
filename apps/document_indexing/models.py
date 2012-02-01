from __future__ import absolute_import

from django.db import models
from django.utils.translation import ugettext_lazy as _

from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey

from documents.models import Document

from .conf.settings import AVAILABLE_INDEXING_FUNCTIONS

available_indexing_functions_string = (_(u'Available functions: %s') % u','.join([u'%s()' % name for name, function in AVAILABLE_INDEXING_FUNCTIONS.items()])) if AVAILABLE_INDEXING_FUNCTIONS else u''


class Index(models.Model):
    name = models.CharField(unique=True, max_length=64, verbose_name=_(u'name'), help_text=_(u'Internal name used to reference this index.'))
    title = models.CharField(unique=True, max_length=128, verbose_name=_(u'title'))
    enabled = models.BooleanField(default=True, verbose_name=_(u'enabled'))

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _(u'index')
        verbose_name_plural = _(u'indexes')


class IndexTemplateNode(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='index_template_node')
    index = models.ForeignKey(Index, verbose_name=_(u'index'))
    expression = models.CharField(max_length=128, verbose_name=_(u'indexing expression'), help_text=_(u'Enter a python string expression to be evaluated.'))
        # % available_indexing_functions_string)
    enabled = models.BooleanField(default=True, verbose_name=_(u'enabled'))
    link_documents = models.BooleanField(default=False, verbose_name=_(u'link documents'))

    def __unicode__(self):
        return self.expression if not self.link_documents else u'%s/[document]' % self.expression

    #@models.permalink
    #def get_absolute_url(self):
    #    return ('index_instance_list', [self.pk])

    #def get_document_list_display(self):
    #    return u', '.join([d.file_filename for d in self.documents.all()])

    class Meta:
        verbose_name = _(u'index template node')
        verbose_name_plural = _(u'indexes template nodes')
    

class IndexInstanceNode(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='index_instance_node')
    index_template_node = models.ForeignKey(IndexTemplateNode, verbose_name=_(u'index template node'))
    value = models.CharField(max_length=128, blank=True, verbose_name=_(u'value'))
    documents = models.ManyToManyField(Document, verbose_name=_(u'documents'))

    def __unicode__(self):
        return self.value

    @models.permalink
    def get_absolute_url(self):
        return ('index_instance_list', [self.pk])

    #def get_document_list_display(self):
    #    return u', '.join([d.file_filename for d in self.documents.all()])

    class Meta:
        verbose_name = _(u'index instance node')
        verbose_name_plural = _(u'indexes instance nodes')


class DocumentRenameCount(models.Model):
    index_instance_node = models.ForeignKey(IndexInstanceNode, verbose_name=_(u'index instance'))
    document = models.ForeignKey(Document, verbose_name=_(u'document'))
    suffix = models.PositiveIntegerField(blank=True, verbose_name=(u'suffix'))

    def __unicode__(self):
        return u'%s - %s - %s' % (self.index_instance_node, self.document, self.suffix or u'0')

    class Meta:
        verbose_name = _(u'document rename count')
        verbose_name_plural = _(u'documents rename count')
