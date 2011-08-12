try:
    from psycopg2 import OperationalError
except ImportError:
    class OperationalError(Exception):
        pass
        
from django.core.exceptions import ImproperlyConfigured
from django.db import transaction
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.db.utils import DatabaseError
from django.db.models.signals import post_save

from navigation.api import register_links, register_top_menu, register_multi_item_links
from permissions.api import register_permission, set_namespace_title
from documents.models import Document
from main.api import register_tool

from scheduler.api import register_interval_job

from ocr.conf.settings import AUTOMATIC_OCR
from ocr.conf.settings import QUEUE_PROCESSING_INTERVAL
from ocr.models import DocumentQueue, QueueTransformation
from ocr.tasks import task_process_document_queues

#Permissions
PERMISSION_OCR_DOCUMENT = {'namespace': 'ocr', 'name': 'ocr_document', 'label': _(u'Submit document for OCR')}
PERMISSION_OCR_DOCUMENT_DELETE = {'namespace': 'ocr', 'name': 'ocr_document_delete', 'label': _(u'Delete document for OCR queue')}
PERMISSION_OCR_QUEUE_ENABLE_DISABLE = {'namespace': 'ocr', 'name': 'ocr_queue_enable_disable', 'label': _(u'Can enable/disable an OCR queue')}
PERMISSION_OCR_CLEAN_ALL_PAGES = {'namespace': 'ocr', 'name': 'ocr_clean_all_pages', 'label': _(u'Can execute an OCR clean up on all document pages')}
PERMISSION_OCR_QUEUE_EDIT = {'namespace': 'ocr_setup', 'name': 'ocr_queue_edit', 'label': _(u'Can edit an OCR queue properties')}

set_namespace_title('ocr', _(u'OCR'))
register_permission(PERMISSION_OCR_DOCUMENT)
register_permission(PERMISSION_OCR_DOCUMENT_DELETE)
register_permission(PERMISSION_OCR_QUEUE_ENABLE_DISABLE)
register_permission(PERMISSION_OCR_CLEAN_ALL_PAGES)

set_namespace_title('ocr_setup', _(u'OCR Setup'))
register_permission(PERMISSION_OCR_QUEUE_EDIT)

#Links
submit_document = {'text': _('submit to OCR queue'), 'view': 'submit_document', 'args': 'object.id', 'famfam': 'hourglass_add', 'permissions': [PERMISSION_OCR_DOCUMENT]}
re_queue_document = {'text': _('re-queue'), 'view': 're_queue_document', 'args': 'object.id', 'famfam': 'hourglass_add', 'permissions': [PERMISSION_OCR_DOCUMENT]}
re_queue_multiple_document = {'text': _('re-queue'), 'view': 're_queue_multiple_document', 'famfam': 'hourglass_add', 'permissions': [PERMISSION_OCR_DOCUMENT]}
queue_document_delete = {'text': _(u'delete'), 'view': 'queue_document_delete', 'args': 'object.id', 'famfam': 'hourglass_delete', 'permissions': [PERMISSION_OCR_DOCUMENT_DELETE]}
queue_document_multiple_delete = {'text': _(u'delete'), 'view': 'queue_document_multiple_delete', 'famfam': 'hourglass_delete', 'permissions': [PERMISSION_OCR_DOCUMENT_DELETE]}

document_queue_disable = {'text': _(u'stop queue'), 'view': 'document_queue_disable', 'args': 'queue.id', 'famfam': 'control_stop_blue', 'permissions': [PERMISSION_OCR_QUEUE_ENABLE_DISABLE]}
document_queue_enable = {'text': _(u'activate queue'), 'view': 'document_queue_enable', 'args': 'queue.id', 'famfam': 'control_play_blue', 'permissions': [PERMISSION_OCR_QUEUE_ENABLE_DISABLE]}

all_document_ocr_cleanup = {'text': _(u'clean up pages content'), 'view': 'all_document_ocr_cleanup', 'famfam': 'text_strikethrough', 'permissions': [PERMISSION_OCR_CLEAN_ALL_PAGES], 'description': _(u'Runs a language filter to remove common OCR mistakes from document pages content.')}

queue_document_list = {'text': _(u'queue document list'), 'view': 'queue_document_list', 'famfam': 'hourglass', 'permissions': [PERMISSION_OCR_DOCUMENT]}
node_active_list = {'text': _(u'active tasks'), 'view': 'node_active_list', 'famfam': 'server_chart', 'permissions': [PERMISSION_OCR_DOCUMENT]}

setup_queue_transformation_list = {'text': _(u'transformations'), 'view': 'setup_queue_transformation_list', 'args': 'queue.pk', 'famfam': 'shape_move_front'}
setup_queue_transformation_create = {'text': _(u'add transformation'), 'view': 'setup_queue_transformation_create', 'args': 'queue.pk', 'famfam': 'shape_square_add'}
setup_queue_transformation_edit = {'text': _(u'edit'), 'view': 'setup_queue_transformation_edit', 'args': 'transformation.pk', 'famfam': 'shape_square_edit'}
setup_queue_transformation_delete = {'text': _(u'delete'), 'view': 'setup_queue_transformation_delete', 'args': 'transformation.pk', 'famfam': 'shape_square_delete'}

register_links(Document, [submit_document])
register_links(DocumentQueue, [document_queue_disable, document_queue_enable, setup_queue_transformation_list])
register_links(QueueTransformation, [setup_queue_transformation_edit, setup_queue_transformation_delete])

register_multi_item_links(['queue_document_list'], [re_queue_multiple_document, queue_document_multiple_delete])

register_links(['setup_queue_transformation_create', 'setup_queue_transformation_edit', 'setup_queue_transformation_delete', 'document_queue_disable', 'document_queue_enable', 'queue_document_list', 'node_active_list', 'setup_queue_transformation_list'], [queue_document_list, node_active_list], menu_name='secondary_menu')
register_links(['setup_queue_transformation_edit', 'setup_queue_transformation_delete', 'setup_queue_transformation_list', 'setup_queue_transformation_create'], [setup_queue_transformation_create], menu_name='sidebar')

register_tool(all_document_ocr_cleanup, namespace='ocr', title=_(u'OCR'))

#Menus
register_top_menu('ocr', link={'text': _('OCR'), 'famfam': 'hourglass', 'view': 'queue_document_list'}, children_path_regex=[r'^ocr/'])


@transaction.commit_manually
def create_default_queue():
    try:
        default_queue, created = DocumentQueue.objects.get_or_create(name='default')
        if created:
            default_queue.label = ugettext(u'Default')
            default_queue.save()
    except DatabaseError:
        transaction.rollback()
        # Special case for ./manage.py syncdb
    except (OperationalError, ImproperlyConfigured):
        transaction.rollback()
        # Special for DjangoZoom, which executes collectstatic media
        # doing syncdb and creating the database tables
    else:
        transaction.commit()


def document_post_save(sender, instance, **kwargs):
    if kwargs.get('created', False):
        if AUTOMATIC_OCR:
            DocumentQueue.objects.queue_document(instance)

post_save.connect(document_post_save, sender=Document)

create_default_queue()

register_interval_job('task_process_document_queues', _(u'Checks the OCR queue for pending documents.'), task_process_document_queues, seconds=QUEUE_PROCESSING_INTERVAL)
