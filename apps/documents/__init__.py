from django.utils.translation import ugettext_lazy as _

from common.api import register_links, register_menu

document_list = {'text':_(u'documents'), 'view':'document_list', 'famfam':'page'}
document_create = {'text':_('create document'), 'view':'document_create', 'famfam':'page_add'}

register_menu([
    {'text':_('documents'), 'view':'document_list', 'links':[
        document_list, document_create
    ],'famfam':'page','position':4}])

