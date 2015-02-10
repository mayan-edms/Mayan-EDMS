from __future__ import unicode_literals

import logging
import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_gpg.runtime import gpg
from documents.models import DocumentVersion
from documents.runtime import storage_backend

from .managers import DocumentVersionSignatureManager

logger = logging.getLogger(__name__)


class DocumentVersionSignature(models.Model):
    """
    Model that describes a document version signature properties
    """
    document_version = models.ForeignKey(DocumentVersion, verbose_name=_('Document version'), editable=False)
    signature_file = models.FileField(blank=True, null=True, upload_to=lambda instance, filename: unicode(uuid.uuid4()), storage=storage_backend, verbose_name=_('Signature file'), editable=False)
    has_embedded_signature = models.BooleanField(default=False, verbose_name=_('Has embedded signature'), editable=False)

    objects = DocumentVersionSignatureManager()

    def delete_detached_signature_file(self):
        self.signature_file.storage.delete(self.signature_file.path)

    def save(self, *args, **kwargs):
        if not self.pk:
            descriptor = self.document_version.open(raw=True)
            self.has_embedded_signature = gpg.has_embedded_signature(descriptor)
            descriptor.close()
        super(DocumentVersionSignature, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Document version signature')
        verbose_name_plural = _('Document version signatures')
