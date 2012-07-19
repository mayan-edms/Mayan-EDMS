from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext

from metadata.models import MetadataType, MetadataSet
from document_indexing.models import Index, IndexTemplateNode

bootstrap_options = {}


class BootstrapBase(object):
    name = None
    label = ''
    description = ''

    def __unicode__(self):
        return unicode(self.label)
   

class BootstrapSimple(BootstrapBase):
    name = 'simple'
    label = _(u'Simple')
    description = _(u'A simple setup providing an uploaded date metadata and index plus an alphabetic index based on document filenames.')
    
    def execute(self):
        # Create metadata types
        date = MetadataType.objects.create(name='upload_date', title=ugettext(u'Upload date'), default='current_date()')
        
        # Create a segmented date index
        index = Index.objects.create(name='date_tree', title=ugettext(u'Segmented date index'), enabled=True)
        
        # Create index template
        #node1 = IndexTemplateNode
        

for bootstrap in [BootstrapSimple()]:
    bootstrap_options[bootstrap.name] = bootstrap

"""

class Index(models.Model):
    name = models.CharField(unique=True, max_length=64, verbose_name=_(u'name'), help_text=_(u'Internal name used to reference this index.'))
    title = models.CharField(unique=True, max_length=128, verbose_name=_(u'title'), help_text=_(u'The name that will be visible to users.'))
    enabled = models.BooleanField(default=True, verbose_name=_(u'enabled'), help_text=_(u'Causes this index to be visible and updated when document data changes.'))

    @property
    def template_root(self):
        return self.indextemplatenode_set.get(parent=None)

    @property
    def instance_root(self):
        return self.template_root.indexinstancenode_set.get()

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('index_instance_node_view', [self.instance_root.pk])

    def save(self, *args, **kwargs):
        super(Index, self).save(*args, **kwargs)
        index_template_node_root, created = IndexTemplateNode.objects.get_or_create(parent=None, index=self)

    class Meta:
        verbose_name = _(u'index')
        verbose_name_plural = _(u'indexes')


class IndexTemplateNode(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='index_template_node')
    index = models.ForeignKey(Index, verbose_name=_(u'index'))
    expression = models.CharField(max_length=128, verbose_name=_(u'indexing expression'), help_text=_(u'Enter a python string expression to be evaluated.'))
        # % available_indexing_functions_string)
    enabled = models.BooleanField(default=True, verbose_name=_(u'enabled'), help_text=_(u'Causes this node to be visible and updated when document data changes.'))
    link_documents = models.BooleanField(default=False, verbose_name=_(u'link documents'), help_text=_(u'Check this option to have this node act as a container for documents and not as a parent for further nodes.'))
"""

