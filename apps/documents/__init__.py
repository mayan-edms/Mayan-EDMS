from django.utils.translation import ugettext_lazy as _

from common.api import register_links, register_menu

from models import Document

document_list = {'text':_(u'documents'), 'view':'document_list', 'famfam':'page'}
document_create = {'text':_('create document'), 'view':'document_create', 'famfam':'page_add'}
document_create_multiple = {'text':_('create multiple document'), 'view':'document_create_multiple', 'famfam':'page_add'}

#register_links(Document, [purchase_order_item_update, purchase_order_item_delete, jump_to_template, purchase_order_item_close, purchase_order_item_transfer])
register_links(['document_list', 'document_create', 'upload_document_with_type'], [document_create, document_create_multiple], menu_name='sidebar')



register_menu([
    {'text':_('documents'), 'view':'document_list', 'links':[
        document_list#, document_create
    ],'famfam':'page','position':4}])

