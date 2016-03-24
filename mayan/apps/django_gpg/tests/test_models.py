from __future__ import unicode_literals

import tempfile

from django.test import TestCase

from ..exceptions import DecryptionError, KeyDoesNotExist, VerificationError
from ..models import Key

from .literals import (
    TEST_DETACHED_SIGNATURE, TEST_FILE, TEST_KEY_DATA, TEST_KEY_FINGERPRINT,
    TEST_SEARCH_FINGERPRINT, TEST_SEARCH_UID, TEST_SIGNED_FILE,
    TEST_SIGNED_FILE_CONTENT
)


class KeyTestCase(TestCase):
    def test_key_instance_creation(self):
        # Creating a Key instance is analogous to importing a key
        key = Key.objects.create(key_data=TEST_KEY_DATA)

        self.assertEqual(key.fingerprint, TEST_KEY_FINGERPRINT)

    def test_key_search(self):
        search_results = Key.objects.search(query=TEST_SEARCH_UID)

        self.assertTrue(
            TEST_SEARCH_FINGERPRINT in [
                key_stub.fingerprint for key_stub in search_results
            ]
        )

    def test_key_receive(self):
        Key.objects.receive_key(key_id=TEST_SEARCH_FINGERPRINT)

        self.assertEqual(Key.objects.all().count(), 1)
        self.assertEqual(Key.objects.first().fingerprint, TEST_SEARCH_FINGERPRINT)

    def test_embedded_verification_no_key(self):
        with open(TEST_SIGNED_FILE) as signed_file:
            with self.assertRaises(KeyDoesNotExist):
                Key.objects.verify_file(signed_file)

    def test_embedded_verification_with_key(self):
        Key.objects.create(key_data=TEST_KEY_DATA)

        with open(TEST_SIGNED_FILE) as signed_file:
            result = Key.objects.verify_file(signed_file)

        self.assertTrue(result.valid)
        self.assertEqual(result.fingerprint, TEST_KEY_FINGERPRINT)

    def test_embedded_verification_with_correct_fingerprint(self):
        Key.objects.create(key_data=TEST_KEY_DATA)

        with open(TEST_SIGNED_FILE) as signed_file:
            result = Key.objects.verify_file(signed_file, key_fingerprint=TEST_KEY_FINGERPRINT)

        self.assertTrue(result.valid)
        self.assertEqual(result.fingerprint, TEST_KEY_FINGERPRINT)

    def test_embedded_verification_with_incorrect_fingerprint(self):
        Key.objects.create(key_data=TEST_KEY_DATA)

        with open(TEST_SIGNED_FILE) as signed_file:
            with self.assertRaises(KeyDoesNotExist):
                Key.objects.verify_file(signed_file, key_fingerprint='999')

    def test_signed_file_decryption(self):
        Key.objects.create(key_data=TEST_KEY_DATA)

        with open(TEST_SIGNED_FILE) as signed_file:
            result = Key.objects.decrypt_file(file_object=signed_file)

        self.assertEqual(result, TEST_SIGNED_FILE_CONTENT)

    def test_cleartext_file_decryption(self):
        cleartext_file = tempfile.TemporaryFile()
        cleartext_file.write('test')
        cleartext_file.seek(0)

        with self.assertRaises(DecryptionError):
            Key.objects.decrypt_file(file_object=cleartext_file)

        cleartext_file.close()

    def test_detached_verification_no_key(self):
        with open(TEST_DETACHED_SIGNATURE) as signature_file:
            with open(TEST_FILE) as test_file:
                with self.assertRaises(KeyDoesNotExist):
                    Key.objects.verify_file(file_object=test_file, signature_file=signature_file)

    def test_detached_verification_with_key(self):
        Key.objects.create(key_data=TEST_KEY_DATA)

        with open(TEST_DETACHED_SIGNATURE) as signature_file:
            with open(TEST_FILE) as test_file:
                result = Key.objects.verify_file(file_object=test_file, signature_file=signature_file)

        self.assertTrue(result)
        self.assertEqual(result.fingerprint, TEST_KEY_FINGERPRINT)
