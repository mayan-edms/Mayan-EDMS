from datetime import date


class GPGBackend(object):
    def __init__(self, **kwargs):
        self.kwargs = kwargs


class KeyStub(object):
    def __init__(self, raw):
        self.fingerprint = raw['keyid']
        self.key_type = raw['type']
        self.date = date.fromtimestamp(int(raw['date']))
        if raw['expires']:
            self.expires = date.fromtimestamp(int(raw['expires']))
        else:
            self.expires = None
        self.length = raw['length']
        self.user_id = raw['uids']

    @property
    def key_id(self):
        return self.fingerprint[-8:]


class SignatureVerification(object):
    def __init__(self, raw):
        self.user_id = raw['username']
        self.status = raw['status']
        self.key_id = raw['key_id']
        self.pubkey_fingerprint = raw['pubkey_fingerprint']
        self.date = date.fromtimestamp(int(raw['timestamp']))
        if raw['expire_timestamp']:
            self.expires = date.fromtimestamp(int(raw['expire_timestamp']))
        else:
            self.expires = None
        self.trust_text = raw['trust_text']
        self.valid = raw['valid']
        self.stderr = raw['stderr']
        self.fingerprint = raw['fingerprint']
        self.signature_id = raw['signature_id']
        self.trust_level = raw['trust_level']
