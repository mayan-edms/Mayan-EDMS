from django.utils.translation import ugettext_lazy as _

from .permissions import (PERMISSION_KEY_DELETE, PERMISSION_KEY_RECEIVE,
                          PERMISSION_KEY_VIEW, PERMISSION_KEYSERVER_QUERY)

private_keys = {'text': _(u'Private keys'), 'view': 'django_gpg:key_private_list', 'args': 'object.pk', 'famfam': 'key', 'icon': 'key.png', 'permissions': [PERMISSION_KEY_VIEW]}
public_keys = {'text': _(u'Public keys'), 'view': 'django_gpg:key_public_list', 'args': 'object.pk', 'famfam': 'key', 'icon': 'key.png', 'permissions': [PERMISSION_KEY_VIEW]}
key_delete = {'text': _(u'Delete'), 'view': 'django_gpg:key_delete', 'args': ['object.fingerprint', 'object.type'], 'famfam': 'key_delete', 'permissions': [PERMISSION_KEY_DELETE]}
key_query = {'text': _(u'Query keyservers'), 'view': 'django_gpg:key_query', 'famfam': 'zoom', 'permissions': [PERMISSION_KEYSERVER_QUERY]}
key_receive = {'text': _(u'Import'), 'view': 'django_gpg:key_receive', 'args': 'object.keyid', 'famfam': 'key_add', 'keep_query': True, 'permissions': [PERMISSION_KEY_RECEIVE]}
key_setup = {'text': _(u'Key management'), 'view': 'django_gpg:key_public_list', 'args': 'object.pk', 'famfam': 'key', 'icon': 'key.png', 'permissions': [PERMISSION_KEY_VIEW]}
