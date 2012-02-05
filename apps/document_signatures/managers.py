import logging

from django.db import models

from django_gpg.runtime import gpg
from django_gpg.exceptions import GPGVerificationError

logger = logging.getLogger(__name__)


class DocumentVersionSignatureManager(models.Manager):
    def get_document_signature(self, document):
        document_signature, created = self.model.objects.get_or_create(
            document_version=document.latest_version,
        )

        return document_signature

    def add_detached_signature(self, document, detached_signature):
        document_signature = self.get_document_signature(document)

        if document_signature.has_embedded_signature:
            raise Exception('document already has an embedded signature')
        else:
            if document_signature.signature_file:
                logger.debug('Existing detached signature')
                document_signature.delete_detached_signature()
                document_signature.signature_file = None
                document_signature.save()

            document_signature.signature_file = detached_signature
            document_signature.save()

    def has_detached_signature(self, document):
        document_signature = self.get_document_signature(document)

        if document_signature.signature_file:
            return True
        else:
            return False

    def has_embedded_signature(self, document):
        logger.debug('document: %s' % document)

        document_signature = self.get_document_signature(document)

        return document_signature.has_embedded_signature

    def detached_signature(self, document):
        document_signature = self.get_document_signature(document)

        return document_signature.signature_file.storage.open(document_signature.signature_file.path)

    def verify_signature(self, document):
        if self.has_detached_signature(document):
            logger.debug('has detached signature')
            args = (document.open(raw=True), self.detached_signature(document))
        else:
            args = (document.open(raw=True),)

        try:
            return gpg.verify_file(*args, fetch_key=True)
        except GPGVerificationError:
            return None
