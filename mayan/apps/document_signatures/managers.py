from __future__ import unicode_literals

import logging

from django.db import models

from django_gpg.exceptions import DecryptionError
from django_gpg.models import Key

logger = logging.getLogger(__name__)


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
