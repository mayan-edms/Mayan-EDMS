from django.utils.translation import ugettext_lazy as _

from documents.models import Document
from navigation.api import register_links, register_top_menu, \
    register_model_list_columns, register_multi_item_links, \
    register_sidebar_template
from main.api import register_diagnostic, register_maintenance_links
from permissions.api import register_permission, set_namespace_title
from project_setup.api import register_setup
from hkp import Key as KeyServerKey

from django_gpg.api import Key

PERMISSION_DOCUMENT_VERIFY = {'namespace': 'django_gpg', 'name': 'document_verify', 'label': _(u'Verify document signatures')}
PERMISSION_KEY_VIEW = {'namespace': 'django_gpg', 'name': 'key_view', 'label': _(u'View keys')}
PERMISSION_KEY_DELETE = {'namespace': 'django_gpg', 'name': 'key_delete', 'label': _(u'Delete keys')}
PERMISSION_KEYSERVER_QUERY = {'namespace': 'django_gpg', 'name': 'keyserver_query', 'label': _(u'Query keyservers')}
PERMISSION_KEY_RECEIVE = {'namespace': 'django_gpg', 'name': 'key_receive', 'label': _(u'Import key from keyservers')}
PERMISSION_SIGNATURE_UPLOAD = {'namespace': 'django_gpg', 'name': 'signature_upload', 'label': _(u'Upload detached signatures')}
PERMISSION_SIGNATURE_DOWNLOAD = {'namespace': 'django_gpg', 'name': 'key_receive', 'label': _(u'Download detached signatures')}

# Permission setup
set_namespace_title('django_gpg', _(u'Signatures'))
register_permission(PERMISSION_DOCUMENT_VERIFY)
register_permission(PERMISSION_KEY_VIEW)
register_permission(PERMISSION_KEY_DELETE)
register_permission(PERMISSION_KEYSERVER_QUERY)
register_permission(PERMISSION_KEY_RECEIVE)
register_permission(PERMISSION_SIGNATURE_UPLOAD)
register_permission(PERMISSION_SIGNATURE_DOWNLOAD)

def has_embedded_signature(context):
    return context['object'].signature_state

# Setup views
private_keys = {'text': _(u'private keys'), 'view': 'key_private_list', 'args': 'object.pk', 'famfam': 'key', 'icon': 'key.png', 'permissions': [PERMISSION_KEY_VIEW]}
public_keys = {'text': _(u'public keys'), 'view': 'key_public_list', 'args': 'object.pk', 'famfam': 'key', 'icon': 'key.png', 'permissions': [PERMISSION_KEY_VIEW]}
key_delete = {'text': _(u'delete'), 'view': 'key_delete', 'args': ['object.fingerprint', 'object.type'], 'famfam': 'key_delete', 'permissions': [PERMISSION_KEY_DELETE]}
key_query = {'text': _(u'Query keyservers'), 'view': 'key_query', 'famfam': 'zoom', 'permissions': [PERMISSION_KEYSERVER_QUERY]}
key_receive = {'text': _(u'Import'), 'view': 'key_receive', 'args': 'object.keyid', 'famfam': 'key_add', 'keep_query': True, 'permissions': [PERMISSION_KEY_RECEIVE]}
document_signature_upload = {'text': _(u'Upload signature'), 'view': 'document_signature_upload', 'args': 'object.pk', 'famfam': 'pencil_add', 'permissions': [PERMISSION_SIGNATURE_UPLOAD], 'conditional_disable': has_embedded_signature}
document_signature_download = {'text': _(u'Download signature'), 'view': 'document_signature_download', 'args': 'object.pk', 'famfam': 'disk', 'permissions': [PERMISSION_SIGNATURE_DOWNLOAD], 'conditional_disable': has_embedded_signature}

# Document views
document_verify = {'text': _(u'signatures'), 'view': 'document_verify', 'args': 'object.pk', 'famfam': 'text_signature', 'permissions': [PERMISSION_DOCUMENT_VERIFY]}

register_links(Document, [document_verify], menu_name='form_header')

register_links(['document_verify', 'document_signature_upload', 'document_signature_download'], [document_signature_upload, document_signature_download], menu_name='sidebar')

register_links(['key_delete', 'key_private_list', 'key_public_list', 'key_query'], [private_keys, public_keys, key_query], menu_name='sidebar')

register_links(Key, [key_delete])
register_links(KeyServerKey, [key_receive])

register_setup(private_keys)
register_setup(public_keys)



