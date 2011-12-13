from django.utils.translation import ugettext_lazy as _

#from documents.models import Document
from navigation.api import register_links, register_top_menu, \
    register_model_list_columns, register_multi_item_links, \
    register_sidebar_template
from main.api import register_diagnostic, register_maintenance_links
from permissions.models import PermissionNamespace, Permission
from project_setup.api import register_setup
from hkp import Key as KeyServerKey

from django_gpg.api import Key

django_gpg_namespace = PermissionNamespace('django_gpg', _(u'Signatures'))

PERMISSION_DOCUMENT_VERIFY = Permission.objects.register(django_gpg_namespace, 'document_verify', _(u'Verify document signatures'))
PERMISSION_KEY_VIEW = Permission.objects.register(django_gpg_namespace, 'key_view', _(u'View keys'))
PERMISSION_KEY_DELETE = Permission.objects.register(django_gpg_namespace, 'key_delete', _(u'Delete keys'))
PERMISSION_KEYSERVER_QUERY = Permission.objects.register(django_gpg_namespace, 'keyserver_query', _(u'Query keyservers'))
PERMISSION_KEY_RECEIVE = Permission.objects.register(django_gpg_namespace, 'key_receive', _(u'Import keys from keyservers'))
PERMISSION_SIGNATURE_UPLOAD = Permission.objects.register(django_gpg_namespace, 'signature_upload', _(u'Upload detached signatures'))
PERMISSION_SIGNATURE_DOWNLOAD = Permission.objects.register(django_gpg_namespace, 'signature_download', _(u'Download detached signatures'))

def has_embedded_signature(context):
    return context['object'].signature_state
    
def doesnt_have_detached_signature(context):
    return context['object'].has_detached_signature() == False    

# Setup views
private_keys = {'text': _(u'private keys'), 'view': 'key_private_list', 'args': 'object.pk', 'famfam': 'key', 'icon': 'key.png', 'permissions': [PERMISSION_KEY_VIEW]}
public_keys = {'text': _(u'public keys'), 'view': 'key_public_list', 'args': 'object.pk', 'famfam': 'key', 'icon': 'key.png', 'permissions': [PERMISSION_KEY_VIEW]}
key_delete = {'text': _(u'delete'), 'view': 'key_delete', 'args': ['object.fingerprint', 'object.type'], 'famfam': 'key_delete', 'permissions': [PERMISSION_KEY_DELETE]}
key_query = {'text': _(u'query keyservers'), 'view': 'key_query', 'famfam': 'zoom', 'permissions': [PERMISSION_KEYSERVER_QUERY]}
key_receive = {'text': _(u'import'), 'view': 'key_receive', 'args': 'object.keyid', 'famfam': 'key_add', 'keep_query': True, 'permissions': [PERMISSION_KEY_RECEIVE]}
document_signature_upload = {'text': _(u'upload signature'), 'view': 'document_signature_upload', 'args': 'object.pk', 'famfam': 'pencil_add', 'permissions': [PERMISSION_SIGNATURE_UPLOAD], 'conditional_disable': has_embedded_signature}
document_signature_download = {'text': _(u'download signature'), 'view': 'document_signature_download', 'args': 'object.pk', 'famfam': 'disk', 'permissions': [PERMISSION_SIGNATURE_DOWNLOAD], 'conditional_disable': doesnt_have_detached_signature}
key_setup = {'text': _(u'key management'), 'view': 'key_public_list', 'args': 'object.pk', 'famfam': 'key', 'icon': 'key.png', 'permissions': [PERMISSION_KEY_VIEW]}

# Document views
document_verify = {'text': _(u'signatures'), 'view': 'document_verify', 'args': 'object.pk', 'famfam': 'text_signature', 'permissions': [PERMISSION_DOCUMENT_VERIFY]}

#register_links(Document, [document_verify], menu_name='form_header')

register_links(['document_verify', 'document_signature_upload', 'document_signature_download'], [document_signature_upload, document_signature_download], menu_name='sidebar')

#register_links(['key_delete', 'key_private_list', 'key_public_list', 'key_query'], [private_keys, public_keys, key_query], menu_name='sidebar')
register_links(['key_delete', 'key_public_list', 'key_query'], [public_keys, key_query], menu_name='sidebar')

register_links(Key, [key_delete])
register_links(KeyServerKey, [key_receive])

register_setup(key_setup)
