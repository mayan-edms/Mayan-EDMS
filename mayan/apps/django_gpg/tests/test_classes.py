from __future__ import unicode_literals

import shutil

from django.test import TestCase

from ..api import GPG, Key
from ..settings import setting_gpg_path

TEST_GPG_HOME = '/tmp/test_gpg_home'
TEST_KEY_ID = '607138F1AECC5A5CA31CB7715F3F7F75D210724D'
TEST_KEYSERVERS = ['pool.sks-keyservers.net']
TEST_UIDS = 'Roberto Rosario'


class DjangoGPGTestCase(TestCase):
    def setUp(self):
        try:
            shutil.rmtree(TEST_GPG_HOME)
        except OSError:
            pass

        self.gpg = GPG(
            binary_path=setting_gpg_path.value, home=TEST_GPG_HOME,
            keyservers=TEST_KEYSERVERS
        )

    def test_main(self):
        # No private or public keys in the keyring
        self.assertEqual(Key.get_all(self.gpg, secret=True), [])
        self.assertEqual(Key.get_all(self.gpg), [])

        # Test querying the keyservers
        self.assertTrue(
            TEST_KEY_ID in [
                key_stub.key_id for key_stub in self.gpg.query(TEST_UIDS)
            ]
        )

        # Receive a public key from the keyserver
        self.gpg.receive_key(key_id=TEST_KEY_ID[-8:])

        # Check that the received key is indeed in the keyring
        self.assertTrue(
            TEST_KEY_ID[-16:] in [
                key_stub.key_id for key_stub in Key.get_all(self.gpg)
            ]
        )
