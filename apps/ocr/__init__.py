from django.utils.translation import ugettext_lazy as _

from common.api import register_links, register_menu
from permissions.api import register_permissions

from documents.models import Document

PERMISSION_OCR_DOCUMENT = 'ocr_document'

register_permissions('ocr', [
    {'name':PERMISSION_OCR_DOCUMENT, 'label':_(u'Submit document for OCR')},
])

submit_document = {'text':_('submit to OCR queue'), 'view':'submit_document', 'args':'object.id', 'famfam':'page_lightning', 'permissions':{'namespace':'ocr', 'permissions':[PERMISSION_OCR_DOCUMENT]}}

register_links(Document, [submit_document], menu_name='sidebar')

#register_menu([
#    {'text':_('OCR'), 'view':'ocr_queue', 'links':[
#        ocr_queue
#    ],'famfam':'hourglass','position':5}])
