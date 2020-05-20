import logging
import os

from django.core.files import File
from django.db import models

from mayan.apps.django_gpg.exceptions import DecryptionError
from mayan.apps.django_gpg.models import Key
from mayan.apps.documents.models import DocumentVersion
from mayan.apps.storage.utils import NamedTemporaryFile, mkstemp

logger = logging.getLogger(name=__name__)


class DetachedSignatureManager(models.Manager):
    def sign_document_version(
        self, document_version, key, passphrase=None, user=None
    ):
        with NamedTemporaryFile() as temporary_file_object:
            with document_version.open() as file_object:
                key.sign_file(
                    binary=True, detached=True, file_object=file_object,
                    output=temporary_file_object.name,
                    passphrase=passphrase
                )
            temporary_file_object.seek(0)
            return self.create(
                document_version=document_version,
                signature_file=File(temporary_file_object)
            )


class EmbeddedSignatureManager(models.Manager):
    def open_signed(self, document_version, file_object):
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

    def sign_document_version(
        self, document_version, key, passphrase=None, user=None
    ):
        temporary_file_object, temporary_filename = mkstemp()

        try:
            with document_version.open() as file_object:
                key.sign_file(
                    binary=True, file_object=file_object,
                    output=temporary_filename, passphrase=passphrase
                )
        except Exception:
            raise
        else:
            # The result of key.sign_file does not contain the signtarure ID.
            # Verify the signed file to obtain the signature ID.
            with open(temporary_filename, mode='rb') as file_object:
                result = Key.objects.verify_file(
                    file_object=file_object
                )

            with open(temporary_filename, mode='rb') as file_object:
                document_version.document.new_version(
                    file_object=file_object, _user=user
                )
            return self.get(signature_id=result.signature_id)
        finally:
            os.unlink(temporary_filename)

    def unsigned_document_versions(self):
        return DocumentVersion.objects.exclude(
            pk__in=self.values('document_version')
        )
