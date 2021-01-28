from datetime import datetime

from django.utils.module_loading import import_string
from django.utils.timezone import make_aware

from .settings import (
    setting_gpg_backend, setting_gpg_backend_arguments
)


class GPGBackend:
    @staticmethod
    def get_instance():
        return import_string(dotted_path=setting_gpg_backend.value)(
            **setting_gpg_backend_arguments.value
        )

    def __init__(self, **kwargs):
        self.kwargs = kwargs


class KeyStub:
    def __init__(self, raw):
        self.fingerprint = raw['keyid']
        self.key_type = raw['type']
        self.date = make_aware(
            value=datetime.fromtimestamp(int(raw['date']))
        )
        if raw['expires']:
            self.expires = make_aware(
                value=datetime.fromtimestamp(int(raw['expires']))
            )
        else:
            self.expires = None
        self.length = raw['length']
        self.user_id = raw['uids']

    @property
    def key_id(self):
        return self.fingerprint[-8:]


class SignatureVerification:
    def __init__(self, raw):
        self.user_id = raw['username']
        self.status = raw['status']
        self.key_id = raw['key_id']
        self.pubkey_fingerprint = raw['pubkey_fingerprint']

        # Invalid signatures do not have a timestamp attribute
        if raw['timestamp']:
            self.date_time = make_aware(
                value=datetime.fromtimestamp(int(raw['timestamp']))
            )

        if raw['expire_timestamp']:
            self.expires = make_aware(
                value=datetime.fromtimestamp(int(raw['expire_timestamp']))
            )
        else:
            self.expires = None
        self.trust_text = raw['trust_text']
        self.valid = raw['valid']
        self.stderr = raw['stderr']
        self.fingerprint = raw['fingerprint']
        self.signature_id = raw['signature_id']
        self.trust_level = raw['trust_level']
