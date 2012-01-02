from django.utils.translation import ugettext_lazy as _

from navigation.api import register_links, register_top_menu, \
    register_model_list_columns, register_multi_item_links, \
    register_sidebar_template
from main.api import register_diagnostic, register_maintenance_links
from permissions.models import PermissionNamespace, Permission
from project_setup.api import register_setup
from hkp import Key as KeyServerKey

from django_gpg.api import Key

django_gpg_namespace = PermissionNamespace('django_gpg', _(u'Key management'))

PERMISSION_KEY_VIEW = Permission.objects.register(django_gpg_namespace, 'key_view', _(u'View keys'))
PERMISSION_KEY_DELETE = Permission.objects.register(django_gpg_namespace, 'key_delete', _(u'Delete keys'))
PERMISSION_KEYSERVER_QUERY = Permission.objects.register(django_gpg_namespace, 'keyserver_query', _(u'Query keyservers'))
PERMISSION_KEY_RECEIVE = Permission.objects.register(django_gpg_namespace, 'key_receive', _(u'Import keys from keyservers'))

# Setup views
private_keys = {'text': _(u'private keys'), 'view': 'key_private_list', 'args': 'object.pk', 'famfam': 'key', 'icon': 'key.png', 'permissions': [PERMISSION_KEY_VIEW]}
public_keys = {'text': _(u'public keys'), 'view': 'key_public_list', 'args': 'object.pk', 'famfam': 'key', 'icon': 'key.png', 'permissions': [PERMISSION_KEY_VIEW]}
key_delete = {'text': _(u'delete'), 'view': 'key_delete', 'args': ['object.fingerprint', 'object.type'], 'famfam': 'key_delete', 'permissions': [PERMISSION_KEY_DELETE]}
key_query = {'text': _(u'query keyservers'), 'view': 'key_query', 'famfam': 'zoom', 'permissions': [PERMISSION_KEYSERVER_QUERY]}
key_receive = {'text': _(u'import'), 'view': 'key_receive', 'args': 'object.keyid', 'famfam': 'key_add', 'keep_query': True, 'permissions': [PERMISSION_KEY_RECEIVE]}
key_setup = {'text': _(u'key management'), 'view': 'key_public_list', 'args': 'object.pk', 'famfam': 'key', 'icon': 'key.png', 'permissions': [PERMISSION_KEY_VIEW]}

#register_links(['key_delete', 'key_private_list', 'key_public_list', 'key_query'], [private_keys, public_keys, key_query], menu_name='sidebar')
register_links(['key_delete', 'key_public_list', 'key_query'], [public_keys, key_query], menu_name='sidebar')

register_links(Key, [key_delete])
register_links(KeyServerKey, [key_receive])

register_setup(key_setup)
