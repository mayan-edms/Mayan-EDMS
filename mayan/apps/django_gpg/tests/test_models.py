import io

import gnupg
import mock

from django.utils.encoding import force_bytes

from mayan.apps.common.tests.base import BaseTestCase
from mayan.apps.storage.utils import TemporaryFile

from ..exceptions import (
    DecryptionError, KeyDoesNotExist, NeedPassphrase, PassphraseError,
    VerificationError
)
from ..models import Key

from .literals import (
    MOCK_SEARCH_KEYS_RESPONSE, TEST_DETACHED_SIGNATURE, TEST_FILE,
    TEST_KEY_PRIVATE_DATA, TEST_KEY_PRIVATE_FINGERPRINT,
    TEST_KEY_PRIVATE_PASSPHRASE, TEST_SEARCH_FINGERPRINT, TEST_SEARCH_UID,
    TEST_SIGNED_FILE, TEST_SIGNED_FILE_CONTENT
)
from .mocks import mock_recv_keys


class KeyTestCase(BaseTestCase):
    def test_key_instance_creation(self):
        # Creating a Key instance is analogous to importing a key
        key = Key.objects.create(key_data=TEST_KEY_PRIVATE_DATA)

        self.assertEqual(key.fingerprint, TEST_KEY_PRIVATE_FINGERPRINT)

    @mock.patch.object(gnupg.GPG, 'search_keys', autospec=True)
    def test_key_search(self, search_keys):
        search_keys.return_value = MOCK_SEARCH_KEYS_RESPONSE

        search_results = Key.objects.search(query=TEST_SEARCH_UID)

        self.assertTrue(
            TEST_SEARCH_FINGERPRINT in [
                key_stub.fingerprint for key_stub in search_results
            ]
        )

    @mock.patch.object(gnupg.GPG, 'recv_keys', autospec=True)
    def test_key_receive(self, recv_keys):
        recv_keys.side_effect = mock_recv_keys

        Key.objects.receive_key(key_id=TEST_SEARCH_FINGERPRINT)

        self.assertEqual(Key.objects.all().count(), 1)
        self.assertEqual(
            Key.objects.first().fingerprint, TEST_SEARCH_FINGERPRINT
        )

    def test_cleartext_file_verification(self):
        cleartext_file = TemporaryFile()
        cleartext_file.write(b'test')
        cleartext_file.seek(0)

        with self.assertRaises(expected_exception=VerificationError):
            Key.objects.verify_file(file_object=cleartext_file)

        cleartext_file.close()

    def test_embedded_verification_no_key(self):
        with open(TEST_SIGNED_FILE, mode='rb') as signed_file:
            result = Key.objects.verify_file(signed_file)

        self.assertTrue(result.key_id in TEST_KEY_PRIVATE_FINGERPRINT)

    def test_embedded_verification_with_key(self):
        Key.objects.create(key_data=TEST_KEY_PRIVATE_DATA)

        with open(TEST_SIGNED_FILE, mode='rb') as signed_file:
            result = Key.objects.verify_file(signed_file)

        self.assertEqual(result.fingerprint, TEST_KEY_PRIVATE_FINGERPRINT)

    def test_embedded_verification_with_correct_fingerprint(self):
        Key.objects.create(key_data=TEST_KEY_PRIVATE_DATA)

        with open(TEST_SIGNED_FILE, mode='rb') as signed_file:
            result = Key.objects.verify_file(
                signed_file, key_fingerprint=TEST_KEY_PRIVATE_FINGERPRINT
            )

        self.assertTrue(result.valid)
        self.assertEqual(result.fingerprint, TEST_KEY_PRIVATE_FINGERPRINT)

    def test_embedded_verification_with_incorrect_fingerprint(self):
        Key.objects.create(key_data=TEST_KEY_PRIVATE_DATA)

        with open(TEST_SIGNED_FILE, mode='rb') as signed_file:
            with self.assertRaises(expected_exception=KeyDoesNotExist):
                Key.objects.verify_file(signed_file, key_fingerprint='999')

    def test_signed_file_decryption(self):
        Key.objects.create(key_data=TEST_KEY_PRIVATE_DATA)

        with open(TEST_SIGNED_FILE, mode='rb') as signed_file:
            result = Key.objects.decrypt_file(file_object=signed_file)

        self.assertEqual(result.read(), TEST_SIGNED_FILE_CONTENT)

    def test_cleartext_file_decryption(self):
        cleartext_file = TemporaryFile()
        cleartext_file.write(b'test')
        cleartext_file.seek(0)

        with self.assertRaises(expected_exception=DecryptionError):
            Key.objects.decrypt_file(file_object=cleartext_file)

        cleartext_file.close()

    def test_detached_verification_no_key(self):
        with open(TEST_DETACHED_SIGNATURE, mode='rb') as signature_file:
            with open(TEST_FILE, mode='rb') as test_file:
                result = Key.objects.verify_file(
                    file_object=test_file, signature_file=signature_file
                )

        self.assertTrue(result.key_id in TEST_KEY_PRIVATE_FINGERPRINT)

    def test_detached_verification_with_key(self):
        Key.objects.create(key_data=TEST_KEY_PRIVATE_DATA)

        with open(TEST_DETACHED_SIGNATURE, mode='rb') as signature_file:
            with open(TEST_FILE, mode='rb') as test_file:
                result = Key.objects.verify_file(
                    file_object=test_file, signature_file=signature_file
                )

        self.assertTrue(result)
        self.assertEqual(result.fingerprint, TEST_KEY_PRIVATE_FINGERPRINT)

    def test_detached_signing_no_passphrase(self):
        key = Key.objects.create(key_data=TEST_KEY_PRIVATE_DATA)

        with self.assertRaises(expected_exception=NeedPassphrase):
            with open(TEST_FILE, mode='rb') as test_file:
                key.sign_file(
                    file_object=test_file, detached=True,
                )

    def test_detached_signing_bad_passphrase(self):
        key = Key.objects.create(key_data=TEST_KEY_PRIVATE_DATA)

        with self.assertRaises(expected_exception=PassphraseError):
            with open(TEST_FILE, mode='rb') as test_file:
                key.sign_file(
                    file_object=test_file, detached=True,
                    passphrase='bad passphrase'
                )

    def test_detached_signing_with_passphrase(self):
        key = Key.objects.create(key_data=TEST_KEY_PRIVATE_DATA)

        with open(TEST_FILE, mode='rb') as test_file:
            detached_signature = key.sign_file(
                file_object=test_file, detached=True,
                passphrase=TEST_KEY_PRIVATE_PASSPHRASE
            )

        signature_file = io.BytesIO()
        signature_file.write(force_bytes(detached_signature))
        signature_file.seek(0)

        with open(TEST_FILE, mode='rb') as test_file:
            result = Key.objects.verify_file(
                file_object=test_file, signature_file=signature_file
            )

        signature_file.close()
        self.assertTrue(result)
        self.assertEqual(result.fingerprint, TEST_KEY_PRIVATE_FINGERPRINT)

    def test_method_get_absolute_url(self):
        key = Key.objects.create(key_data=TEST_KEY_PRIVATE_DATA)

        self.assertTrue(key.get_absolute_url())
