import logging

from django.db import models

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
                document_signature.delete_detached_signature_file()
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
        from django_gpg.runtime import gpg

        document_descriptor = document.open(raw=True)
        detached_signature = None
        if self.has_detached_signature(document):
            logger.debug('has detached signature')
            detached_signature = self.detached_signature(document)
            args = (document_descriptor, detached_signature)
        else:
            args = (document_descriptor,)

        try:
            return gpg.verify_file(*args, fetch_key=True)
        except GPGVerificationError:
            return None
        finally:
            document_descriptor.close()
            if detached_signature:
                detached_signature.close()

    def clear_detached_signature(self, document):
        document_signature = self.get_document_signature(document)
        if not document_signature.signature_file:
            raise Exception('document doesn\'t have a detached signature')

        document_signature.delete_detached_signature_file()
        document_signature.signature_file = None
        document_signature.save()
