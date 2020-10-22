import logging
import uuid

from django.db import models
from django.urls import reverse
from django.utils.encoding import force_text, python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from model_utils.managers import InheritanceManager

from mayan.apps.django_gpg.exceptions import VerificationError
from mayan.apps.django_gpg.models import Key
from mayan.apps.documents.models import DocumentVersion
from mayan.apps.storage.classes import DefinedStorageLazy

from .literals import STORAGE_NAME_DOCUMENT_SIGNATURES_DETACHED_SIGNATURE
from .managers import DetachedSignatureManager, EmbeddedSignatureManager

logger = logging.getLogger(name=__name__)


def upload_to(*args, **kwargs):
    return force_text(s=uuid.uuid4())


@python_2_unicode_compatible
class SignatureBaseModel(models.Model):
    """
    Fields:
    * key_id - Key Identifier - This is what identifies uniquely a key. Not
    two keys in the world have the same Key ID. The Key ID is also used to
    locate a key in the key servers: http://pgp.mit.edu
    * signature_id - Signature ID - Every time a key is used to sign something
    it will generate a unique signature ID. No two signature IDs are the same,
    even when using the same key.
    """
    document_version = models.ForeignKey(
        editable=False, on_delete=models.CASCADE, related_name='signatures',
        to=DocumentVersion, verbose_name=_('Document version')
    )
    # Basic fields
    date = models.DateField(
        blank=True, editable=False, null=True, verbose_name=_('Date signed')
    )
    key_id = models.CharField(
        help_text=_('ID of the key that will be used to sign the document.'),
        max_length=40, verbose_name=_('Key ID')
    )
    # With proper key
    signature_id = models.CharField(
        blank=True, editable=False, null=True, max_length=64,
        verbose_name=_('Signature ID')
    )
    public_key_fingerprint = models.CharField(
        blank=True, editable=False, null=True, max_length=40,
        verbose_name=_('Public key fingerprint')
    )

    objects = InheritanceManager()

    class Meta:
        ordering = ('pk',)
        verbose_name = _('Document version signature')
        verbose_name_plural = _('Document version signatures')

    def __str__(self):
        return self.signature_id or '{} - {}'.format(self.date, self.key_id)

    def get_absolute_url(self):
        return reverse(
            viewname='signatures:document_version_signature_details',
            kwargs={'signature_id': self.pk}
        )

    def get_key_id(self):
        if self.public_key_fingerprint:
            return self.public_key_fingerprint[-16:]
        else:
            return self.key_id

    def get_signature_type_display(self):
        if self.is_detached:
            return _('Detached')
        else:
            return _('Embedded')

    @property
    def is_detached(self):
        return hasattr(self, 'signature_file')

    @property
    def is_embedded(self):
        return not hasattr(self, 'signature_file')


class EmbeddedSignature(SignatureBaseModel):
    objects = EmbeddedSignatureManager()

    class Meta:
        verbose_name = _('Document version embedded signature')
        verbose_name_plural = _('Document version embedded signatures')

    def save(self, *args, **kwargs):
        logger.debug(msg='checking for embedded signature')

        if self.pk:
            raw = True
        else:
            raw = False

        with self.document_version.open(raw=raw) as file_object:
            try:
                verify_result = Key.objects.verify_file(
                    file_object=file_object
                )
            except VerificationError as exception:
                # Not signed
                logger.debug(
                    'embedded signature verification error; %s', exception
                )
            else:
                self.date = verify_result.date
                self.key_id = verify_result.key_id
                self.signature_id = verify_result.signature_id
                self.public_key_fingerprint = verify_result.pubkey_fingerprint

                super(EmbeddedSignature, self).save(*args, **kwargs)


@python_2_unicode_compatible
class DetachedSignature(SignatureBaseModel):
    signature_file = models.FileField(
        blank=True, help_text=_(
            'Signature file previously generated.'
        ), null=True, storage=DefinedStorageLazy(
            name=STORAGE_NAME_DOCUMENT_SIGNATURES_DETACHED_SIGNATURE
        ), upload_to=upload_to, verbose_name=_('Signature file')
    )

    objects = DetachedSignatureManager()

    class Meta:
        verbose_name = _('Document version detached signature')
        verbose_name_plural = _('Document version detached signatures')

    def __str__(self):
        return '{}-{}'.format(self.document_version, _('signature'))

    def delete(self, *args, **kwargs):
        if self.signature_file.name:
            self.signature_file.storage.delete(name=self.signature_file.name)
        super(DetachedSignature, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        with self.document_version.open() as file_object:
            try:
                verify_result = Key.objects.verify_file(
                    file_object=file_object, signature_file=self.signature_file
                )
            except VerificationError as exception:
                # Not signed
                logger.debug(
                    'detached signature verification error; %s', exception
                )
            else:
                self.signature_file.seek(0)

                self.date = verify_result.date
                self.key_id = verify_result.key_id
                self.signature_id = verify_result.signature_id
                self.public_key_fingerprint = verify_result.pubkey_fingerprint

        return super(DetachedSignature, self).save(*args, **kwargs)
