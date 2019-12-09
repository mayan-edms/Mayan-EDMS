from __future__ import unicode_literals

import logging
import os

from django.core.files import File
from django.db import models

from mayan.apps.django_gpg.exceptions import DecryptionError
from mayan.apps.django_gpg.models import Key
from mayan.apps.documents.models import DocumentVersion
from mayan.apps.storage.utils import mkstemp

logger = logging.getLogger(__name__)


class DetachedSignatureManager(models.Manager):
    def sign_document_version(
        self, document_version, key, passphrase=None, user=None
    ):
        temporary_file_object, temporary_filename = mkstemp()

        try:
            with document_version.open() as file_object:
                key.sign_file(
                    binary=True, detached=True, file_object=file_object,
                    output=temporary_filename, passphrase=passphrase
                )
        except Exception:
            raise
        else:
            return self.create(
                document_version=document_version,
                signature_file=File(temporary_file_object)
            )
        finally:
            os.unlink(temporary_filename)


class EmbeddedSignatureManager(models.Manager):
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
            with open(temporary_filename, mode='rb') as file_object:
                new_version = document_version.document.new_version(
                    file_object=file_object, _user=user
                )
            # This is a potential race condition but we have not way
            # to access the final signature at this point.
            signature = self.filter(document_version=new_version).first()
            return signature or self.none()
        finally:
            os.unlink(temporary_filename)

    def unsigned_document_versions(self):
        return DocumentVersion.objects.exclude(
            pk__in=self.values('document_version')
        )
