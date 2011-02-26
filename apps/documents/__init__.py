import tempfile

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from common.api import register_links, register_menu, \
    register_model_list_columns
from common.utils import pretty_size

from permissions.api import register_permissions

from models import Document, DocumentPage, DocumentPageTransformation
from staging import StagingFile

from common.conf import settings as common_settings

from conf.settings import ENABLE_SINGLE_DOCUMENT_UPLOAD

PERMISSION_DOCUMENT_CREATE = 'document_create'
PERMISSION_DOCUMENT_PROPERTIES_EDIT = 'document_properties_edit'
PERMISSION_DOCUMENT_METADATA_EDIT = 'document_metadata_edit'
PERMISSION_DOCUMENT_VIEW = 'document_view'
PERMISSION_DOCUMENT_DELETE = 'document_delete'
PERMISSION_DOCUMENT_DOWNLOAD = 'document_download'
PERMISSION_DOCUMENT_TRANSFORM = 'document_transform'
PERMISSION_DOCUMENT_TOOLS = 'document_tools'

register_permissions('documents', [
    {'name':PERMISSION_DOCUMENT_CREATE, 'label':_(u'Create document')},
    {'name':PERMISSION_DOCUMENT_PROPERTIES_EDIT, 'label':_(u'Edit document properties')},
    {'name':PERMISSION_DOCUMENT_METADATA_EDIT, 'label':_(u'Edit document metadata')},
    {'name':PERMISSION_DOCUMENT_VIEW, 'label':_(u'View document')},
    {'name':PERMISSION_DOCUMENT_DELETE, 'label':_(u'Delete document')},
    {'name':PERMISSION_DOCUMENT_DOWNLOAD, 'label':_(u'Download document')},
    {'name':PERMISSION_DOCUMENT_TRANSFORM, 'label':_(u'Transform document')},
    {'name':PERMISSION_DOCUMENT_TOOLS, 'label':_(u'Execute document modifying tools')},
])

document_list = {'text':_(u'documents list'), 'view':'document_list', 'famfam':'page', 'permissions':{'namespace':'documents', 'permissions':[PERMISSION_DOCUMENT_VIEW]}}
document_create = {'text':_('upload a new document'), 'view':'document_create', 'famfam':'page_add', 'permissions':{'namespace':'documents', 'permissions':[PERMISSION_DOCUMENT_CREATE]}}
document_create_multiple = {'text':_('upload multiple new documents'), 'view':'document_create_multiple', 'famfam':'page_add', 'permissions':{'namespace':'documents', 'permissions':[PERMISSION_DOCUMENT_CREATE]}}
document_create_sibling = {'text':_('upload new document using same metadata'), 'view':'document_create_sibling', 'args':'object.id', 'famfam':'page_copy', 'permissions':{'namespace':'documents', 'permissions':[PERMISSION_DOCUMENT_CREATE]}}
document_view = {'text':_('details'), 'view':'document_view', 'args':'object.id', 'famfam':'page', 'permissions':{'namespace':'documents', 'permissions':[PERMISSION_DOCUMENT_VIEW]}}
document_delete = {'text':_('delete'), 'view':'document_delete', 'args':'object.id', 'famfam':'page_delete', 'permissions':{'namespace':'documents', 'permissions':[PERMISSION_DOCUMENT_DELETE]}}
document_edit = {'text':_('edit'), 'view':'document_edit', 'args':'object.id', 'famfam':'page_edit', 'permissions':{'namespace':'documents', 'permissions':[PERMISSION_DOCUMENT_PROPERTIES_EDIT]}}
document_edit_metadata = {'text':_('edit metadata'), 'view':'document_edit_metadata', 'args':'object.id', 'famfam':'page_edit', 'permissions':{'namespace':'documents', 'permissions':[PERMISSION_DOCUMENT_METADATA_EDIT]}}
document_preview = {'text':_('preview'), 'class':'fancybox', 'view':'document_preview', 'args':'object.id', 'famfam':'magnifier', 'permissions':{'namespace':'documents', 'permissions':[PERMISSION_DOCUMENT_VIEW]}}
document_download = {'text':_('download'), 'view':'document_download', 'args':'object.id', 'famfam':'page_save', 'permissions':{'namespace':'documents', 'permissions':[PERMISSION_DOCUMENT_DOWNLOAD]}}
document_find_duplicates = {'text':_('find duplicates'), 'view':'document_find_duplicates', 'args':'object.id', 'famfam':'page_refresh', 'permissions':{'namespace':'documents', 'permissions':[PERMISSION_DOCUMENT_VIEW]}}
document_find_all_duplicates = {'text':_('find all duplicates'), 'view':'document_find_all_duplicates', 'famfam':'page_refresh', 'permissions':{'namespace':'documents', 'permissions':[PERMISSION_DOCUMENT_VIEW]}}

document_page_transformation_create = {'text':_('create new transformation'), 'view':'document_page_transformation_create', 'args':'object.id', 'famfam':'pencil_add', 'permissions':{'namespace':'documents', 'permissions':[PERMISSION_DOCUMENT_TRANSFORM]}}
document_page_transformation_edit = {'text':_('edit'), 'view':'document_page_transformation_edit', 'args':'object.id', 'famfam':'pencil_go', 'permissions':{'namespace':'documents', 'permissions':[PERMISSION_DOCUMENT_TRANSFORM]}}
document_page_transformation_delete = {'text':_('delete'), 'view':'document_page_transformation_delete', 'args':'object.id', 'famfam':'pencil_delete', 'permissions':{'namespace':'documents', 'permissions':[PERMISSION_DOCUMENT_TRANSFORM]}}
document_page_transformation_go_back = {'text':_('return to document'), 'view':'document_view', 'args':'object.document_page.document.id', 'famfam':'page_go', 'permissions':{'namespace':'documents', 'permissions':[PERMISSION_DOCUMENT_VIEW]}}

document_page_go_back = {'text':_('return to document'), 'view':'document_view', 'args':'object.document.id', 'famfam':'page_go', 'permissions':{'namespace':'documents', 'permissions':[PERMISSION_DOCUMENT_VIEW]}}

staging_file_preview = {'text':_('preview'), 'class':'fancybox-noscaling', 'view':'staging_file_preview', 'args':'object.id', 'famfam':'drive_magnify'}
staging_file_delete = {'text':_('delete'), 'view':'staging_file_delete', 'args':'object.id', 'famfam':'drive_delete'}

register_links(Document, [document_view, document_edit, document_edit_metadata, document_delete, document_download, document_find_duplicates], menu_name='sidebar')
register_links(Document, [document_list, document_create, document_create_multiple, document_create_sibling], menu_name='sidebar')

if ENABLE_SINGLE_DOCUMENT_UPLOAD:
    register_links(['document_list', 'document_create', 'document_create_multiple', 'upload_document_with_type', 'upload_multiple_documents_with_type'], [document_list, document_create, document_create_multiple], menu_name='sidebar')
else:
    register_links(['document_list', 'document_create', 'document_create_multiple', 'upload_document_with_type', 'upload_multiple_documents_with_type'], [document_list, document_create_multiple], menu_name='sidebar')

register_links(DocumentPage, [document_page_go_back], menu_name='sidebar')

register_links(DocumentPageTransformation, [document_page_transformation_edit, document_page_transformation_delete])
register_links(DocumentPageTransformation, [document_page_transformation_go_back], menu_name='sidebar')
register_links(['document_page_view', 'document_page_transformation_edit', 'document_page_transformation_delete', 'document_page_transformation_create'], [document_page_transformation_create], menu_name='sidebar')

register_links(StagingFile, [staging_file_preview, staging_file_delete])

register_model_list_columns(Document, [
    {'name':_(u'thumbnail'), 'attribute': 
        lambda x: '<a class="fancybox" href="%s"><img src="%s" /></a>' % (reverse('document_preview', args=[x.id]),
            reverse('document_thumbnail', args=[x.id]))
    },
    {'name':_(u'metadata'), 'attribute': 
        lambda x: ', '.join(['%s - %s' %(metadata.metadata_type, metadata.value) for metadata in x.documentmetadata_set.all()])
    },

    ])

if ENABLE_SINGLE_DOCUMENT_UPLOAD:
    register_menu([
        {'text':_('documents'), 'view':'document_create', 'links':[
            document_create, document_create_multiple, document_list
        ],'famfam':'page','position':1}])
else:
    register_menu([
        {'text':_('documents'), 'view':'document_create_multiple', 'links':[
            document_create_multiple, document_list
        ],'famfam':'page','position':1}])

TEMPORARY_DIRECTORY = common_settings.TEMPORARY_DIRECTORY if common_settings.TEMPORARY_DIRECTORY else tempfile.mkdtemp()
