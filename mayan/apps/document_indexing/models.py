from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from documents.models import Document, DocumentType

from .managers import IndexManager


class Index(models.Model):
    name = models.CharField(unique=True, max_length=64, verbose_name=_('Name'), help_text=_('Internal name used to reference this index.'))
    # TODO: normalize 'title' to 'label'
    title = models.CharField(unique=True, max_length=128, verbose_name=_('Title'), help_text=_('The name that will be visible to users.'))
    enabled = models.BooleanField(default=True, verbose_name=_('Enabled'), help_text=_('Causes this index to be visible and updated when document data changes.'))
    document_types = models.ManyToManyField(DocumentType, verbose_name=_('Document types'))

    objects = IndexManager()

    @property
    def template_root(self):
        return self.node_templates.get(parent=None)

    @property
    def instance_root(self):
        return self.template_root.node_instance.get()

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('indexing:index_instance_node_view', [self.instance_root.pk])

    def get_document_types_not_in_index(self):
        return DocumentType.objects.exclude(pk__in=self.document_types.all())

    def save(self, *args, **kwargs):
        """Automatically create the root index template node"""
        super(Index, self).save(*args, **kwargs)
        IndexTemplateNode.objects.get_or_create(parent=None, index=self)

    def get_document_types_names(self):
        return ', '.join([unicode(document_type) for document_type in self.document_types.all()] or ['None'])

    def natural_key(self):
        return (self.name,)

    def get_instance_node_count(self):
        try:
            return self.instance_root.get_descendant_count()
        except IndexInstanceNode.DoesNotExist:
            return 0

    class Meta:
        verbose_name = _('Index')
        verbose_name_plural = _('Indexes')


class IndexTemplateNode(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True)
    index = models.ForeignKey(Index, verbose_name=_('Index'), related_name='node_templates')
    expression = models.CharField(max_length=128, verbose_name=_('Indexing expression'), help_text=_('Enter a python string expression to be evaluated.'))
    enabled = models.BooleanField(default=True, verbose_name=_('Enabled'), help_text=_('Causes this node to be visible and updated when document data changes.'))
    link_documents = models.BooleanField(default=False, verbose_name=_('Link documents'), help_text=_('Check this option to have this node act as a container for documents and not as a parent for further nodes.'))

    def __unicode__(self):
        return self.expression

    class Meta:
        verbose_name = _('Index node template')
        verbose_name_plural = _('Indexes node template')


class IndexInstanceNode(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True)
    index_template_node = models.ForeignKey(IndexTemplateNode, related_name='node_instance', verbose_name=_('Index template node'))
    value = models.CharField(max_length=128, blank=True, verbose_name=_('Value'))
    documents = models.ManyToManyField(Document, related_name='node_instances', verbose_name=_('Documents'))

    def __unicode__(self):
        return self.value

    def index(self):
        return self.index_template_node.index

    @models.permalink
    def get_absolute_url(self):
        return ('indexing:index_instance_node_view', [self.pk])

    @property
    def children(self):
        # Convenience method for serializer
        return self.get_children()

    class Meta:
        verbose_name = _('Index node instance')
        verbose_name_plural = _('Indexes node instances')
