from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from documents.models import Document
from navigation.api import register_links, register_top_menu, \
    register_model_list_columns, register_multi_item_links, \
    register_sidebar_template
from main.api import register_diagnostic, register_maintenance_links
from permissions.api import register_permission, set_namespace_title
#from project_setup.api import register_setup

#from django_gpg.api import Key

PERMISSION_DOCUMENT_VERIFY = {'namespace': 'document_signatures', 'name': 'document_verify', 'label': _(u'Verify document signatures')}
PERMISSION_SIGNATURE_UPLOAD = {'namespace': 'document_signatures', 'name': 'signature_upload', 'label': _(u'Upload detached signatures')}
PERMISSION_SIGNATURE_DOWNLOAD = {'namespace': 'document_signatures', 'name': 'key_receive', 'label': _(u'Download detached signatures')}

# Permission setup
set_namespace_title('document_signatures', _(u'Document signatures'))
register_permission(PERMISSION_DOCUMENT_VERIFY)
register_permission(PERMISSION_SIGNATURE_UPLOAD)
register_permission(PERMISSION_SIGNATURE_DOWNLOAD)

def has_embedded_signature(context):
    return context['object'].signature_state
    
def doesnt_have_detached_signature(context):
    return context['object'].has_detached_signature() == False    

document_signature_upload = {'text': _(u'upload signature'), 'view': 'document_signature_upload', 'args': 'object.pk', 'famfam': 'pencil_add', 'permissions': [PERMISSION_SIGNATURE_UPLOAD], 'conditional_disable': has_embedded_signature}
document_signature_download = {'text': _(u'download signature'), 'view': 'document_signature_download', 'args': 'object.pk', 'famfam': 'disk', 'permissions': [PERMISSION_SIGNATURE_DOWNLOAD], 'conditional_disable': doesnt_have_detached_signature}
document_verify = {'text': _(u'signatures'), 'view': 'document_verify', 'args': 'object.pk', 'famfam': 'text_signature', 'permissions': [PERMISSION_DOCUMENT_VERIFY]}

register_links(Document, [document_verify], menu_name='form_header')

register_links(['document_verify', 'document_signature_upload', 'document_signature_download'], [document_signature_upload, document_signature_download], menu_name='sidebar')
