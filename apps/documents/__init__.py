import tempfile

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from common.api import register_links, register_menu, register_model_list_columns
from common.utils import pretty_size

from models import Document
from staging import StagingFile

from documents.conf import settings as documents_settings


document_list = {'text':_(u'documents list'), 'view':'document_list', 'famfam':'page'}
document_create = {'text':_('upload a document'), 'view':'document_create', 'famfam':'page_add'}
document_create_multiple = {'text':_('upload multiple documents'), 'view':'document_create_multiple', 'famfam':'page_add'}
document_create_sibling = {'text':_('upload using same metadata'), 'view':'document_create_sibling', 'args':'object.id', 'famfam':'page_copy'}
document_view = {'text':_('details'), 'view':'document_view', 'args':'object.id', 'famfam':'page'}
document_delete = {'text':_('delete'), 'view':'document_delete', 'args':'object.id', 'famfam':'page_delete'}
document_edit = {'text':_('edit'), 'view':'document_edit', 'args':'object.id', 'famfam':'page_edit'}
document_edit_metadata = {'text':_('edit metadata'), 'view':'document_edit_metadata', 'args':'object.id', 'famfam':'page_edit'}
document_preview = {'text':_('preview'), 'class':'fancybox', 'view':'document_preview', 'args':'object.id', 'famfam':'magnifier'}
document_download = {'text':_('download'), 'view':'document_download', 'args':'object.id', 'famfam':'page_save'}

staging_file_preview = {'text':_('preview'), 'class':'fancybox', 'view':'staging_file_preview', 'args':'object.id', 'famfam':'drive_magnify'}

register_links(Document, [document_view, document_edit, document_edit_metadata, document_delete, document_download], menu_name='sidebar')
register_links(Document, [document_list, document_create, document_create_multiple, document_create_sibling], menu_name='sidebar')
register_links(['document_list', 'document_create', 'document_create_multiple', 'upload_document_with_type', 'upload_multiple_documents_with_type'], [document_list, document_create, document_create_multiple], menu_name='sidebar')

register_links(StagingFile, [staging_file_preview])

register_model_list_columns(Document, [
    #{'name':_(u'mimetype'), 'attribute':'file_mimetype'},
    #{'name':_(u'added'), 'attribute':lambda x: x.date_added.date()},
    #{'name':_(u'file size'), 'attribute':lambda x: pretty_size(x.file.storage.size(x.file.path)) if x.exists() else '-'},
    {'name':_(u'thumbnail'), 'attribute': 
        lambda x: '<a class="fancybox" href="%s"><img src="%s" /></a>' % (reverse('document_preview', args=[x.id]),
            reverse('document_thumbnail', args=[x.id]))
    },
    {'name':_(u'metadata'), 'attribute': 
        lambda x: ', '.join(['%s - %s' %(metadata.metadata_type, metadata.value) for metadata in x.documentmetadata_set.all()])
    },

    ])

register_menu([
    {'text':_('documents'), 'view':'document_list', 'links':[
        document_list
    ],'famfam':'page','position':4}])

TEMPORARY_DIRECTORY = documents_settings.TEMPORARY_DIRECTORY if documents_settings.TEMPORARY_DIRECTORY else tempfile.mkdtemp()

    #','.join([metadata for metadata in document.documentmetadata_set.all()])
    #    initial.append({
    #        'metadata_type':metadata.metadata_type,
    #        'document_type':document.document_type,
    #        'value':metadata.value,
    #    })    
