from __future__ import absolute_import
import logging

from django.db import models
from django.utils.translation import ugettext_lazy as _

from documents.models import DocumentVersion, get_filename_from_uuid

from .managers import DocumentVersionSignatureManager

logger = logging.getLogger(__name__)


class DocumentVersionSignature(models.Model):
    """
    Model that describes a document version signature properties
    """
    document_version = models.ForeignKey(DocumentVersion, verbose_name=_(u'document version'), editable=False)
    signature_file = models.FileField(blank=True, null=True, upload_to=get_filename_from_uuid, verbose_name=_(u'signature file'), editable=False)
    has_embedded_signature = models.BooleanField(default=False, verbose_name=_(u'has embedded signature'), editable=False)

    objects = DocumentVersionSignatureManager()

    def delete_detached_signature_file(self):
        self.signature_file.storage.delete(self.signature_file.path)

    def save(self, *args, **kwargs):
        from django_gpg.runtime import gpg

        if not self.pk:
            descriptor = self.document_version.open(raw=True)
            self.has_embedded_signature = gpg.has_embedded_signature(descriptor)
            descriptor.close()
        super(DocumentVersionSignature, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _(u'document version signature')
        verbose_name_plural = _(u'document version signatures')
