from __future__ import absolute_import, unicode_literals

import io
import logging
import os
import shutil

import gnupg

from django.db import models

from common.utils import mkdtemp, mkstemp
from organizations.managers import CurrentOrganizationManager

from .classes import KeyStub, SignatureVerification
from .exceptions import (
    DecryptionError, KeyDoesNotExist, KeyFetchingError, VerificationError
)
from .literals import KEY_TYPE_PUBLIC, KEY_TYPE_SECRET
from .settings import setting_gpg_path, setting_keyserver

logger = logging.getLogger(__name__)


class KeyManager(models.Manager):
    def decrypt_file(self, file_object, all_keys=False, key_fingerprint=None, key_id=None):
        temporary_directory = mkdtemp()

        os.chmod(temporary_directory, 0x1C0)

        gpg = gnupg.GPG(
            gnupghome=temporary_directory, gpgbinary=setting_gpg_path.value
        )

        # Preload keys
        if all_keys:
            logger.debug('preloading all keys')
            for key in self.all():
                gpg.import_keys(key_data=key.key_data)
        elif key_fingerprint:
            logger.debug('preloading key fingerprint: %s', key_fingerprint)
            try:
                key = self.get(fingerprint=key_fingerprint)
            except self.model.DoesNotExist:
                logger.debug('key fingerprint %s not found', key_fingerprint)
                shutil.rmtree(temporary_directory)
                raise KeyDoesNotExist(
                    'Specified key for verification not found'
                )
            else:
                gpg.import_keys(key_data=key.key_data)
        elif key_id:
            logger.debug('preloading key id: %s', key_id)
            try:
                key = self.get(fingerprint__endswith=key_id)
            except self.model.DoesNotExist:
                logger.debug('key id %s not found', key_id)
            else:
                gpg.import_keys(key_data=key.key_data)
                logger.debug('key id %s impored', key_id)

        decrypt_result = gpg.decrypt_file(file=file_object)

        shutil.rmtree(temporary_directory)

        logger.debug('decrypt_result.status: %s', decrypt_result.status)

        if not decrypt_result.status or decrypt_result.status == 'no data was provided':
            raise DecryptionError('Unable to decrypt file')

        file_object.close()

        return io.BytesIO(decrypt_result.data)

    def receive_key(self, key_id):
        temporary_directory = mkdtemp()

        os.chmod(temporary_directory, 0x1C0)

        gpg = gnupg.GPG(
            gnupghome=temporary_directory, gpgbinary=setting_gpg_path.value
        )

        import_results = gpg.recv_keys(setting_keyserver.value, key_id)

        if not import_results.count:
            shutil.rmtree(temporary_directory)
            raise KeyFetchingError('No key found')
        else:
            key_data = gpg.export_keys(import_results.fingerprints[0])

            shutil.rmtree(temporary_directory)

            return self.create(key_data=key_data)

    def search(self, query):
        temporary_directory = mkdtemp()

        os.chmod(temporary_directory, 0x1C0)

        gpg = gnupg.GPG(
            gnupghome=temporary_directory, gpgbinary=setting_gpg_path.value
        )

        key_data_list = gpg.search_keys(
            query=query, keyserver=setting_keyserver.value
        )
        shutil.rmtree(temporary_directory)

        result = []
        for key_data in key_data_list:
            result.append(KeyStub(raw=key_data))

        return result

    def public_keys(self):
        return self.filter(key_type=KEY_TYPE_PUBLIC)

    def private_keys(self):
        return self.filter(key_type=KEY_TYPE_SECRET)

    def verify_file(self, file_object, signature_file=None, all_keys=False, key_fingerprint=None, key_id=None):
        temporary_directory = mkdtemp()

        os.chmod(temporary_directory, 0x1C0)

        gpg = gnupg.GPG(
            gnupghome=temporary_directory, gpgbinary=setting_gpg_path.value
        )

        # Preload keys
        if all_keys:
            logger.debug('preloading all keys')
            for key in self.all():
                gpg.import_keys(key_data=key.key_data)
        elif key_fingerprint:
            logger.debug('preloading key fingerprint: %s', key_fingerprint)
            try:
                key = self.get(fingerprint=key_fingerprint)
            except self.model.DoesNotExist:
                logger.debug('key fingerprint %s not found', key_fingerprint)
                shutil.rmtree(temporary_directory)
                raise KeyDoesNotExist(
                    'Specified key for verification not found'
                )
            else:
                gpg.import_keys(key_data=key.key_data)
        elif key_id:
            logger.debug('preloading key id: %s', key_id)
            try:
                key = self.get(fingerprint__endswith=key_id)
            except self.model.DoesNotExist:
                logger.debug('key id %s not found', key_id)
            else:
                gpg.import_keys(key_data=key.key_data)
                logger.debug('key id %s impored', key_id)

        if signature_file:
            # Save the original data and invert the argument order
            # Signature first, file second
            temporary_file_object, temporary_filename = mkstemp()
            os.write(temporary_file_object, file_object.read())
            os.close(temporary_file_object)

            signature_file_buffer = io.BytesIO()
            signature_file_buffer.write(signature_file.read())
            signature_file_buffer.seek(0)
            signature_file.seek(0)
            verify_result = gpg.verify_file(
                file=signature_file_buffer, data_filename=temporary_filename
            )
            signature_file_buffer.close()
            os.unlink(temporary_filename)
        else:
            verify_result = gpg.verify_file(file=file_object)

        logger.debug('verify_result.status: %s', verify_result.status)

        shutil.rmtree(temporary_directory)

        if verify_result:
            # Signed and key present
            logger.debug('signed and key present')
            return SignatureVerification(verify_result.__dict__)
        elif verify_result.status == 'no public key' and not (key_fingerprint or all_keys or key_id):
            # Signed but key not present, retry with key fetch
            logger.debug('no public key')
            file_object.seek(0)
            return self.verify_file(file_object=file_object, signature_file=signature_file, key_id=verify_result.key_id)
        elif verify_result.key_id:
            # Signed, retried and key still not found
            logger.debug('signed, retried and key still not found')
            return SignatureVerification(verify_result.__dict__)
        else:
            logger.debug('file not signed')
            raise VerificationError('File not signed')


class OrganizationKeyManager(KeyManager, CurrentOrganizationManager):
    pass
