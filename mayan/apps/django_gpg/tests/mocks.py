from __future__ import unicode_literals

from .literals import TEST_RECEIVE_KEY, TEST_SEARCH_FINGERPRINT

MOCK_SEARCH_KEYS_RESPONSE = [
    {
        'algo': u'1',
        'date': u'1311475606',
        'expires': u'1643601600',
        'keyid': u'607138F1AECC5A5CA31CB7715F3F7F75D210724D',
        'length': u'2048',
        'type': u'pub',
        'uids': [u'Roberto Rosario <roberto.rosario.gonzalez@gmail.com>']
    }
]


def mock_recv_keys(self, keyserver, *keyids):
    class ImportResult(object):
        count = 1
        fingerprints = [TEST_SEARCH_FINGERPRINT]

    self.import_keys(TEST_RECEIVE_KEY)

    return ImportResult()
