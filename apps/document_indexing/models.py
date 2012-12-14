from __future__ import absolute_import

from django.db import models
from django.utils.translation import ugettext_lazy as _

from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey

from documents.models import Document, DocumentType

from .managers import IndexManager


class Index(models.Model):
    name = models.CharField(unique=True, max_length=64, verbose_name=_(u'name'), help_text=_(u'Internal name used to reference this index.'))
    title = models.CharField(unique=True, max_length=128, verbose_name=_(u'title'), help_text=_(u'The name that will be visible to users.'))
    enabled = models.BooleanField(default=True, verbose_name=_(u'enabled'), help_text=_(u'Causes this index to be visible and updated when document data changes.'))
    document_types = models.ManyToManyField(DocumentType, verbose_name=_(u'document types'))

    objects = IndexManager()

    @property
    def template_root(self):
        return self.indextemplatenode_set.get(parent=None)

    @property
    def instance_root(self):
        return self.template_root.node_instance

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('index_instance_node_view', [self.instance_root.pk])

    def get_index_document_types(self):
        return self.document_types.all()

    def get_document_types_not_in_index(self):
        return DocumentType.objects.exclude(pk__in=self.get_index_document_types())

    def save(self, *args, **kwargs):
        super(Index, self).save(*args, **kwargs)
        index_template_node_root, created = IndexTemplateNode.objects.get_or_create(parent=None, index=self)

    def natural_key(self):
        return (self.name,)

    def get_document_types_names(self):
        return u', '.join([unicode(document_type) for document_type in self.document_types.all()] or [u'All'])

    def get_instance_node_count(self):
        try:
            return self.instance_root.get_descendant_count()
        except IndexInstanceNode.DoesNotExist:
            return 0

    class Meta:
        verbose_name = _(u'index')
        verbose_name_plural = _(u'indexes')


class IndexTemplateNode(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='index_template_node')
    index = models.ForeignKey(Index, verbose_name=_(u'index'))
    expression = models.CharField(max_length=128, verbose_name=_(u'indexing expression'), help_text=_(u'Enter a python string expression to be evaluated.'))
    enabled = models.BooleanField(default=True, verbose_name=_(u'enabled'), help_text=_(u'Causes this node to be visible and updated when document data changes.'))
    link_documents = models.BooleanField(default=False, verbose_name=_(u'link documents'), help_text=_(u'Check this option to have this node act as a container for documents and not as a parent for further nodes.'))

    def __unicode__(self):
        return self.expression

    @property
    def node_instance(self):
        return self.indexinstancenode_set.get()

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
        return ('index_instance_node_view', [self.pk])

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
