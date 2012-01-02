from __future__ import absolute_import
import logging

from django.db import models
from django.utils.translation import ugettext_lazy as _

from documents.models import DocumentVersion, get_filename_from_uuid
from documents.conf.settings import STORAGE_BACKEND

from .managers import DocumentVersionSignatureManager

logger = logging.getLogger(__name__)


class DocumentVersionSignature(models.Model):
    '''
    Model that describes a document version signature properties
    '''
    document_version = models.ForeignKey(DocumentVersion, verbose_name=_(u'document version'), editable=False)
    signature_state = models.CharField(blank=True, null=True, max_length=16, verbose_name=_(u'signature state'), editable=False)
    signature_file = models.FileField(blank=True, null=True, upload_to=get_filename_from_uuid, storage=STORAGE_BACKEND(), verbose_name=_(u'signature file'), editable=False)

    objects = DocumentVersionSignatureManager()

    class Meta:
        verbose_name = _(u'document version signature')
        verbose_name_plural = _(u'document version signatures')
