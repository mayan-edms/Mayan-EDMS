from django.utils.translation import ugettext_lazy as _

from common.api import register_links, register_menu

from models import Document

document_list = {'text':_(u'documents list'), 'view':'document_list', 'famfam':'page'}
document_create = {'text':_('upload a document'), 'view':'document_create', 'famfam':'page_add'}
document_create_multiple = {'text':_('upload multiple document'), 'view':'document_create_multiple', 'famfam':'page_add'}
document_view = {'text':_('details'), 'view':'document_view', 'args':'object.id', 'famfam':'page'}
document_delete = {'text':_('delete'), 'view':'document_delete', 'args':'object.id', 'famfam':'page_delete'}
document_edit = {'text':_('edit'), 'view':'document_edit', 'args':'object.id', 'famfam':'page_edit'}

register_links(Document, [document_view, document_edit, document_delete])
register_links(Document, [document_list, document_create, document_create_multiple], menu_name='sidebar')
register_links(['document_list', 'document_create', 'document_create_multiple', 'upload_document_with_type', 'upload_multiple_documents_with_type'], [document_list, document_create, document_create_multiple], menu_name='sidebar')


register_menu([
    {'text':_('documents'), 'view':'document_list', 'links':[
        document_list#, document_create
    ],'famfam':'page','position':4}])

