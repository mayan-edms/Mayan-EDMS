from __future__ import absolute_import, unicode_literals


class KeyStub(object):
    def __init__(self, raw):
        self.key_id = raw['keyid']
        self.key_type = raw['type']
        self.date = raw['date']
        self.expires = raw['expires']
        self.length = raw['length']
        self.uids = raw['uids']
