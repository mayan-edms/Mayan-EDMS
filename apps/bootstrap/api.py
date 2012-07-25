from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext

from metadata.models import MetadataType, MetadataSet
from document_indexing.models import Index, IndexTemplateNode
from documents.models import DocumentType, DocumentTypeFilename

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


class BootstrapPermit(BootstrapBase):
    name = 'permits'
    label = _(u'Permits')
    description = _(u'A setup for handling permits and related documents.')
    
    def execute(self):
        # Create document types
        form = DocumentType.objects.create(name=ugettext(u'Form'))
        DocumentTypeFilename.objects.create(document_type=form, filename=ugettext(u'Building construction form'))
        DocumentTypeFilename.objects.create(document_type=form, filename=ugettext(u'Building usage form'))

        blueprint = DocumentType.objects.create(name=ugettext(u'Blueprint'))
        DocumentTypeFilename.objects.create(document_type=blueprint, filename=ugettext(u'Floorplan'))
        DocumentTypeFilename.objects.create(document_type=blueprint, filename=ugettext(u'Plot plan'))
       
        # Create metadata types
        date = MetadataType.objects.create(name='date', title=ugettext(u'Date'), default='current_date()')
        client = MetadataType.objects.create(name='client', title=ugettext(u'Client'))
        permit = MetadataType.objects.create(name='permit', title=ugettext(u'Permit number'))
        project = MetadataType.objects.create(name='project', title=ugettext(u'Project'))
        user = MetadataType.objects.create(name='user', title=ugettext(u'User'), lookup='sorted([user.get_full_name() or user for user in User.objects.all() if user.is_active])')
        
        # Create a segmented date index
        index = Index.objects.create(name='main_index', title=ugettext(u'Permit index'), enabled=True)
        
        # Create index template
        per_permit = IndexTemplateNode.objects.create(parent=index.template_root, index=index, expression='\'%s\'' % ugettext(u'Per permit'), enabled=True, link_documents=False)
        per_permit_child = IndexTemplateNode.objects.create(parent=per_permit, index=index, expression='metadata.permit', enabled=True, link_documents=True)

        per_project = IndexTemplateNode.objects.create(parent=index.template_root, index=index, expression='\'%s\'' % ugettext(u'Per project'), enabled=True, link_documents=False)
        per_project_child = IndexTemplateNode.objects.create(parent=per_project, index=index, expression='metadata.project', enabled=True, link_documents=False)
        per_permit = IndexTemplateNode.objects.create(parent=per_project_child, index=index, expression='\'%s\'' % ugettext(u'Per permit'), enabled=True, link_documents=False)
        per_permit_child = IndexTemplateNode.objects.create(parent=per_permit, index=index, expression='metadata.permit', enabled=True, link_documents=True)

        per_date = IndexTemplateNode.objects.create(parent=index.template_root, index=index, expression='\'%s\'' % ugettext(u'Per date'), enabled=True, link_documents=False)
        per_date_child = IndexTemplateNode.objects.create(parent=per_date, index=index, expression='metadata.date', enabled=True, link_documents=True)

        per_user = IndexTemplateNode.objects.create(parent=index.template_root, index=index, expression='\'%s\'' % ugettext(u'Per user'), enabled=True, link_documents=False)
        per_user_child = IndexTemplateNode.objects.create(parent=per_user, index=index, expression='metadata.user', enabled=True, link_documents=True)

        per_client = IndexTemplateNode.objects.create(parent=index.template_root, index=index, expression='\'%s\'' % ugettext(u'Per client'), enabled=True, link_documents=False)
        per_client_child = IndexTemplateNode.objects.create(parent=per_client, index=index, expression='metadata.client', enabled=True, link_documents=True)
       

for bootstrap in [BootstrapSimple(), BootstrapPermit()]:
    bootstrap_options[bootstrap.name] = bootstrap
