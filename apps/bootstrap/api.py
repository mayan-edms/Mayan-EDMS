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
        upload_date = MetadataType.objects.create(name='upload_date', title=ugettext(u'Upload date'), default='current_date()')
        
        # Create a segmented date index
        index = Index.objects.create(name='date_tree', title=ugettext(u'Segmented date index'), enabled=True)
        template_root = index.template_root
        
        # Create index template
        node1 = IndexTemplateNode.objects.create(parent=template_root, index=index, expression='metadata.upload_date[0:4]', enabled=True, link_documents=False)
        node2 = IndexTemplateNode.objects.create(parent=node1, index=index, expression='metadata.upload_date[5:7]', enabled=True, link_documents=False)
        node3 = IndexTemplateNode.objects.create(parent=node2, index=index, expression='metadata.upload_date[8:10]', enabled=True, link_documents=True)
        

for bootstrap in [BootstrapSimple()]:
    bootstrap_options[bootstrap.name] = bootstrap
