from django.utils.translation import ugettext_lazy as _

from common.api import register_links, register_menu

from documents.models import Document


submit_document = {'text':_('submit to OCR queue'), 'view':'submit_document', 'args':'object.id', 'famfam':'page_lightning'}

register_links(Document, [submit_document], menu_name='sidebar')

#register_menu([
#    {'text':_('OCR'), 'view':'ocr_queue', 'links':[
#        ocr_queue
#    ],'famfam':'hourglass','position':5}])
