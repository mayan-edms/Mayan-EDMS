from multiprocessing import Queue

from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.db.utils import DatabaseError

from common.api import register_links, register_menu
from permissions.api import register_permissions

from documents.models import Document

from models import DocumentQueue, QueueDocument
from literals import QUEUEDOCUMENT_STATE_PROCESSING, \
    QUEUEDOCUMENT_STATE_PENDING, DOCUMENTQUEUE_STATE_STOPPED, \
    DOCUMENTQUEUE_STATE_ACTIVE

#Permissions
PERMISSION_OCR_DOCUMENT = 'ocr_document'
PERMISSION_OCR_DOCUMENT_DELETE = 'ocr_document_delete'

register_permissions('ocr', [
    {'name':PERMISSION_OCR_DOCUMENT, 'label':_(u'Submit document for OCR')},
    {'name':PERMISSION_OCR_DOCUMENT_DELETE, 'label':_(u'Delete document for OCR queue')},
])

#Links
submit_document = {'text':_('submit to OCR queue'), 'view':'submit_document', 'args':'object.id', 'famfam':'hourglass_add', 'permissions':{'namespace':'ocr', 'permissions':[PERMISSION_OCR_DOCUMENT]}}
register_links(Document, [submit_document], menu_name='sidebar')
queue_document_delete = {'text':_(u'delete'), 'view':'queue_document_delete', 'args':'object.id', 'famfam':'hourglass_delete', 'permissions':{'namespace':'ocr', 'permissions':[PERMISSION_OCR_DOCUMENT_DELETE]}}

register_links(QueueDocument, [queue_document_delete])


#Menus
register_menu([
    {'text':_('OCR'), 'view':'queue_document_list', 'links':[
        #ocr_queue
    ],'famfam':'hourglass','position':4}])


try:
    default_queue, created = DocumentQueue.objects.get_or_create(name='default')
    if created:
        default_queue.label = ugettext(u'Default')
        default_queue.save()

    for queue in DocumentQueue.objects.all():
        queue.state = DOCUMENTQUEUE_STATE_ACTIVE
        queue.save()
        for document in queue.queuedocument_set.filter(state=QUEUEDOCUMENT_STATE_PROCESSING):
            document.state = QUEUEDOCUMENT_STATE_PENDING
            document.save()
except DatabaseError:
    #syncdb
    pass
