from __future__ import unicode_literals

import logging

from django.db import models

from django_gpg.exceptions import GPGVerificationError
from django_gpg.runtime import gpg

logger = logging.getLogger(__name__)


class DocumentVersionSignatureManager(models.Manager):
    def get_document_signature(self, document_version):
        document_signature, created = self.model.objects.get_or_create(
            document_version=document_version,
        )

        return document_signature

    def add_detached_signature(self, document_version, detached_signature):
        document_signature = self.get_document_signature(
            document_version=document_version
        )

        if document_signature.has_embedded_signature:
            raise Exception(
                'Document version already has an embedded signature'
            )
        else:
            if document_signature.signature_file:
                logger.debug('Existing detached signature')
                document_signature.delete_detached_signature_file()
                document_signature.signature_file = None
                document_signature.save()

            document_signature.signature_file = detached_signature
            document_signature.save()

    def has_detached_signature(self, document_version):
        try:
            document_signature = self.get_document_signature(
                document_version=document_version
            )
        except ValueError:
            return False
        else:
            if document_signature.signature_file:
                return True
            else:
                return False

    def has_embedded_signature(self, document_version):
        logger.debug('document_version: %s', document_version)

        try:
            document_signature = self.get_document_signature(
                document_version=document_version
            )
        except ValueError:
            return False
        else:
            return document_signature.has_embedded_signature

    def detached_signature(self, document_version):
        document_signature = self.get_document_signature(
            document_version=document_version
        )

        return document_signature.signature_file.storage.open(
            document_signature.signature_file.name
        )

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
            return gpg.verify_file(*args, fetch_key=False)
        except GPGVerificationError:
            return None
        finally:
            document_version_descriptor.close()
            if detached_signature:
                detached_signature.close()

    def clear_detached_signature(self, document_version):
        document_signature = self.get_document_signature(
            document_version=document_version
        )
        if not document_signature.signature_file:
            raise Exception('document doesn\'t have a detached signature')

        document_signature.delete_detached_signature_file()
        document_signature.signature_file = None
        document_signature.save()
