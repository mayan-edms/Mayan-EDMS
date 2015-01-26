from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from .permissions import (
    PERMISSION_KEY_DELETE, PERMISSION_KEY_RECEIVE, PERMISSION_KEY_VIEW,
    PERMISSION_KEYSERVER_QUERY
)

private_keys = {'text': _('Private keys'), 'view': 'django_gpg:key_private_list', 'args': 'object.pk', 'famfam': 'key', 'icon': 'main/icons/key.png', 'permissions': [PERMISSION_KEY_VIEW]}
public_keys = {'text': _('Public keys'), 'view': 'django_gpg:key_public_list', 'args': 'object.pk', 'famfam': 'key', 'icon': 'main/icons/key.png', 'permissions': [PERMISSION_KEY_VIEW]}
key_delete = {'text': _('Delete'), 'view': 'django_gpg:key_delete', 'args': ['object.fingerprint', 'object.type'], 'famfam': 'key_delete', 'permissions': [PERMISSION_KEY_DELETE]}
key_query = {'text': _('Query keyservers'), 'view': 'django_gpg:key_query', 'famfam': 'zoom', 'permissions': [PERMISSION_KEYSERVER_QUERY]}
key_receive = {'text': _('Import'), 'view': 'django_gpg:key_receive', 'args': 'object.keyid', 'famfam': 'key_add', 'keep_query': True, 'permissions': [PERMISSION_KEY_RECEIVE]}
key_setup = {'text': _('Key management'), 'view': 'django_gpg:key_public_list', 'args': 'object.pk', 'famfam': 'key', 'icon': 'main/icons/key.png', 'permissions': [PERMISSION_KEY_VIEW]}
