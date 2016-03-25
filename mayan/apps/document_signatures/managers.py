from __future__ import unicode_literals

import logging

from django.db import models

from django_gpg.exceptions import DecryptionError, VerificationError
from django_gpg.models import Key

logger = logging.getLogger(__name__)


class DetachedSignatureManager(models.Manager):
    def upload_signature(self, document_version, signature_file):
        with document_version.open() as file_object:
            try:
                verify_result = Key.objects.verify_file(
                    file_object=file_object, signature_file=signature_file
                )
            except VerificationError:
                # Not signed
                pass
            else:
                instance = self.create(
                    document_version=document_version,
                    date=verify_result.date,
                    key_id=verify_result.key_id,
                    signature_id=verify_result.signature_id,
                    public_key_fingerprint=verify_result.pubkey_fingerprint,
                )


class EmbeddedSignatureManager(models.Manager):
    def check_signature(self, document_version):
        logger.debug('checking for embedded signature')

        with document_version.open() as file_object:
            try:
                verify_result = Key.objects.verify_file(file_object=file_object)
            except VerificationError:
                # Not signed
                pass
            else:
                instance = self.create(
                    document_version=document_version,
                    date=verify_result.date,
                    key_id=verify_result.key_id,
                    signature_id=verify_result.signature_id,
                    public_key_fingerprint=verify_result.pubkey_fingerprint,
                )

    def open_signed(self, file_object, document_version):
        for signature in self.filter(document_version=document_version):
            try:
                return self.open_signed(
                    file_object=Key.objects.decrypt_file(
                        file_object=file_object
                    ), document_version=document_version
                )
            except DecryptionError:
                file_object.seek(0)
                return file_object
        else:
            return file_object

    """
    def verify_signature(self, document_version):
        document_version_descriptor = document_version.open(raw=True)
        detached_signature = None
        if self.has_detached_signature(document_version=document_version):
            logger.debug('has detached signature')
            detached_signature = self.detached_signature(
                document_version=document_version
            )
            args = (document_version_descriptor, detached_signature)
        else:
            args = (document_version_descriptor,)

        try:
            return Key.objects.verify_file(*args)
        except VerificationError:
            return None
        finally:
            document_version_descriptor.close()
            if detached_signature:
                detached_signature.close()
    """
