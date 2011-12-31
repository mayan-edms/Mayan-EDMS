from __future__ import absolute_import

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO   

from django.utils.translation import ugettext_lazy as _

from documents.models import Document, DocumentVersion
from navigation.api import register_links, register_top_menu, \
    register_model_list_columns, register_multi_item_links, \
    register_sidebar_template
from django_gpg.runtime import gpg
from django_gpg.exceptions import GPGDecryptionError    
#from main.api import register_diagnostic, register_maintenance_links

from .models import DocumentVersionSignature
from .permissions import (
    PERMISSION_DOCUMENT_VERIFY, 
    PERMISSION_SIGNATURE_UPLOAD,
    PERMISSION_SIGNATURE_DOWNLOAD
    )


def has_embedded_signature(context):
    return DocumentVersionSignature.objects.has_embedded_signature(context['object'])
    
def doesnt_have_detached_signature(context):
    return DocumentVersionSignature.objects.has_detached_signature(context['object']) == False

def document_pre_open_hook(descriptor):
    try:
        result = gpg.decrypt_file(descriptor)
        # gpg return a string, turn it into a file like object
        return StringIO(result.data)
    except GPGDecryptionError:
        # At least return the original raw content
        return descriptor

document_signature_upload = {'text': _(u'upload signature'), 'view': 'document_signature_upload', 'args': 'object.pk', 'famfam': 'pencil_add', 'permissions': [PERMISSION_SIGNATURE_UPLOAD], 'conditional_disable': has_embedded_signature}
document_signature_download = {'text': _(u'download signature'), 'view': 'document_signature_download', 'args': 'object.pk', 'famfam': 'disk', 'permissions': [PERMISSION_SIGNATURE_DOWNLOAD], 'conditional_disable': doesnt_have_detached_signature}
document_verify = {'text': _(u'signatures'), 'view': 'document_verify', 'args': 'object.pk', 'famfam': 'text_signature', 'permissions': [PERMISSION_DOCUMENT_VERIFY]}

register_links(Document, [document_verify], menu_name='form_header')
register_links(['document_verify', 'document_signature_upload', 'document_signature_download'], [document_signature_upload, document_signature_download], menu_name='sidebar')


DocumentVersion.register_pre_open_hook(1, document_pre_open_hook)
