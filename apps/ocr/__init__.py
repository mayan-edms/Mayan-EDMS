from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.db.utils import DatabaseError
from django.db.models.signals import post_save
from django.core.urlresolvers import reverse

from navigation.api import register_links, register_menu, register_multi_item_links
from permissions.api import register_permissions
from documents.models import Document
from main.api import register_tool

from ocr.conf.settings import AUTOMATIC_OCR
from ocr.models import DocumentQueue
from ocr.urls import urlpatterns

#Permissions
PERMISSION_OCR_DOCUMENT = 'ocr_document'
PERMISSION_OCR_DOCUMENT_DELETE = 'ocr_document_delete'
PERMISSION_OCR_QUEUE_ENABLE_DISABLE = 'ocr_queue_enable_disable'
PERMISSION_OCR_CLEAN_ALL_PAGES = 'ocr_clean_all_pages'

register_permissions('ocr', [
    {'name': PERMISSION_OCR_DOCUMENT, 'label': _(u'Submit document for OCR')},
    {'name': PERMISSION_OCR_DOCUMENT_DELETE, 'label': _(u'Delete document for OCR queue')},
    {'name': PERMISSION_OCR_QUEUE_ENABLE_DISABLE, 'label': _(u'Can enable/disable an OCR queue')},
    {'name': PERMISSION_OCR_CLEAN_ALL_PAGES, 'label': _(u'Can execute an OCR clean up on all document pages')},
])

#Links
submit_document = {'text': _('submit to OCR queue'), 'view': 'submit_document', 'args': 'object.id', 'famfam': 'hourglass_add', 'permissions': {'namespace': 'ocr', 'permissions': [PERMISSION_OCR_DOCUMENT]}}
re_queue_document = {'text': _('re-queue'), 'view': 're_queue_document', 'args': 'object.id', 'famfam': 'hourglass_add', 'permissions': {'namespace': 'ocr', 'permissions': [PERMISSION_OCR_DOCUMENT]}}
re_queue_multiple_document = {'text': _('re-queue'), 'view': 're_queue_multiple_document', 'famfam': 'hourglass_add', 'permissions': {'namespace': 'ocr', 'permissions': [PERMISSION_OCR_DOCUMENT]}}
queue_document_delete = {'text': _(u'delete'), 'view': 'queue_document_delete', 'args': 'object.id', 'famfam': 'hourglass_delete', 'permissions': {'namespace': 'ocr', 'permissions': [PERMISSION_OCR_DOCUMENT_DELETE]}}
queue_document_multiple_delete = {'text': _(u'delete'), 'view': 'queue_document_multiple_delete', 'famfam': 'hourglass_delete', 'permissions': {'namespace': 'ocr', 'permissions': [PERMISSION_OCR_DOCUMENT_DELETE]}}

document_queue_disable = {'text': _(u'stop queue'), 'view': 'document_queue_disable', 'args': 'object.id', 'famfam': 'control_stop_blue', 'permissions': {'namespace': 'ocr', 'permissions': [PERMISSION_OCR_QUEUE_ENABLE_DISABLE]}}
document_queue_enable = {'text': _(u'activate queue'), 'view': 'document_queue_enable', 'args': 'object.id', 'famfam': 'control_play_blue', 'permissions': {'namespace': 'ocr', 'permissions': [PERMISSION_OCR_QUEUE_ENABLE_DISABLE]}}

all_document_ocr_cleanup = {'text': _(u'clean up pages content'), 'view': 'all_document_ocr_cleanup', 'famfam': 'text_strikethrough', 'permissions': {'namespace': 'ocr', 'permissions': [PERMISSION_OCR_CLEAN_ALL_PAGES]}, 'description': _(u'Runs a language filter to remove common OCR mistakes from document pages content.')}

queue_document_list = {'text': _(u'queue document list'), 'view': 'queue_document_list', 'famfam': 'hourglass', 'permissions': {'namespace': 'ocr', 'permissions': [PERMISSION_OCR_DOCUMENT]}}
node_active_list = {'text': _(u'active tasks'), 'view': 'node_active_list', 'famfam': 'server_chart', 'permissions': {'namespace': 'ocr', 'permissions': [PERMISSION_OCR_DOCUMENT]}}

register_links(Document, [submit_document])
register_links(DocumentQueue, [document_queue_disable, document_queue_enable])

register_multi_item_links(['queue_document_list'], [re_queue_multiple_document, queue_document_multiple_delete])

register_tool(all_document_ocr_cleanup, namespace='ocr', title=_(u'OCR'))

#Menus
register_menu([
    {'text': _('OCR'), 'view': 'queue_document_list', 'links':[
        queue_document_list, node_active_list
    ], 'famfam': 'hourglass', 'position': 5}])


try:
    default_queue, created = DocumentQueue.objects.get_or_create(name='default')
    if created:
        default_queue.label = ugettext(u'Default')
        default_queue.save()
except DatabaseError:
    #syncdb
    pass


def document_post_save(sender, instance, **kwargs):
    if kwargs.get('created', False):
        if AUTOMATIC_OCR:
            DocumentQueue.objects.queue_document(instance)

post_save.connect(document_post_save, sender=Document)
