from multiprocessing import Queue

from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.db.utils import DatabaseError

from common.api import register_links, register_menu
from permissions.api import register_permissions

from documents.models import Document

from models import DocumentQueue
from literals import QUEUEDOCUMENT_STATE_PROCESSING, \
    DOCUMENTQUEUE_STATE_STOPPED, QUEUEDOCUMENT_STATE_PENDING

from api import start_queue_watcher

#Permissions
PERMISSION_OCR_DOCUMENT = 'ocr_document'
register_permissions('ocr', [
    {'name':PERMISSION_OCR_DOCUMENT, 'label':_(u'Submit document for OCR')},
])

#Links
submit_document = {'text':_('submit to OCR queue'), 'view':'submit_document', 'args':'object.id', 'famfam':'page_lightning', 'permissions':{'namespace':'ocr', 'permissions':[PERMISSION_OCR_DOCUMENT]}}
register_links(Document, [submit_document], menu_name='sidebar')

#Menus
#register_menu([
#    {'text':_('OCR'), 'view':'ocr_queue', 'links':[
#        ocr_queue
#    ],'famfam':'hourglass','position':5}])


try:
    default_queue, created = DocumentQueue.objects.get_or_create(name='default')
    if created:
        default_queue.label = ugettext(u'Default')
        default_queue.save()

    for queue in DocumentQueue.objects.all():
        queue.state = DOCUMENTQUEUE_STATE_STOPPED
        queue.save()
        start_queue_watcher(queue.name)
        for document in queue.queuedocument_set.filter(state=QUEUEDOCUMENT_STATE_PROCESSING):
            document.state = QUEUEDOCUMENT_STATE_PENDING
            document.save()
except DatabaseError:
    #syncdb
    pass
