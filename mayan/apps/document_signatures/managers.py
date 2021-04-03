import logging
import os

from django.core.files import File
from django.db import models

from mayan.apps.django_gpg.exceptions import DecryptionError
from mayan.apps.django_gpg.models import Key
from mayan.apps.documents.models import DocumentFile
from mayan.apps.storage.utils import NamedTemporaryFile, mkstemp

from .events import (
    event_detached_signature_created,
    event_embedded_signature_created
)


logger = logging.getLogger(name=__name__)


class DetachedSignatureManager(models.Manager):
    def sign_document_file(
        self, document_file, key, passphrase=None, user=None
    ):
        with NamedTemporaryFile() as temporary_file_object:
            with document_file.open() as file_object:
                key.sign_file(
                    binary=True, detached=True, file_object=file_object,
                    output=temporary_file_object.name,
                    passphrase=passphrase
                )
            temporary_file_object.seek(0)

            instance = self.model(
                document_file=document_file,
                signature_file=File(file=temporary_file_object)
            )
            instance._event_ignore = True
            instance.save()
            event_detached_signature_created.commit(
                action_object=instance, actor=user, target=document_file
            )
            return instance


class EmbeddedSignatureManager(models.Manager):
    def open_signed(self, document_file, file_object):
        for signature in self.filter(document_file=document_file):
            try:
                return self.open_signed(
                    file_object=Key.objects.decrypt_file(
                        file_object=file_object
                    ), document_file=document_file
                )
            except DecryptionError:
                file_object.seek(0)
                return file_object
        else:
            return file_object

    def sign_document_file(
        self, document_file, key, passphrase=None, user=None
    ):
        temporary_file_object, temporary_filename = mkstemp()

        try:
            with document_file.open() as file_object:
                key.sign_file(
                    binary=True, file_object=file_object,
                    output=temporary_filename, passphrase=passphrase
                )
        except Exception:
            raise
        else:
            # The result of key.sign_file does not contain the signtarure ID.
            # Verify the signed file to obtain the signature ID.
            with open(file=temporary_filename, mode='rb') as file_object:
                result = Key.objects.verify_file(
                    file_object=file_object
                )

            with open(file=temporary_filename, mode='rb') as file_object:
                document_file.document.file_new(
                    file_object=file_object, _user=user
                )
            instance = self.get(signature_id=result.signature_id)
            event_embedded_signature_created.commit(
                action_object=instance, actor=user, target=document_file
            )
            return instance
        finally:
            os.unlink(temporary_filename)

    def unsigned_document_files(self):
        return DocumentFile.objects.exclude(
            pk__in=self.values('document_file')
        )
