from datetime import datetime
import logging

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.timezone import make_aware
from django.utils.translation import ugettext_lazy as _

from mayan.apps.databases.model_mixins import ExtraDataModelMixin
from mayan.apps.events.classes import EventManagerSave
from mayan.apps.events.decorators import method_event

from .classes import GPGBackend
from .events import event_key_created
from .exceptions import NeedPassphrase, PassphraseError
from .literals import (
    ERROR_MSG_BAD_PASSPHRASE, ERROR_MSG_GOOD_PASSPHRASE,
    ERROR_MSG_MISSING_PASSPHRASE, KEY_TYPE_CHOICES, KEY_TYPE_SECRET,
    OUTPUT_MESSAGE_CONTAINS_PRIVATE_KEY
)

from .managers import KeyManager

logger = logging.getLogger(name=__name__)


class Key(ExtraDataModelMixin, models.Model):
    """
    Fields:
    * key_type - Will show private or public, the only two types of keys in
    a public key infrastructure, the kind used in Mayan.
    """
    key_data = models.TextField(
        help_text=_('ASCII armored version of the key.'),
        verbose_name=_('Key data')
    )
    creation_date = models.DateTimeField(
        editable=False, verbose_name=_('Creation date')
    )
    expiration_date = models.DateTimeField(
        blank=True, editable=False, null=True,
        verbose_name=_('Expiration date')
    )
    fingerprint = models.CharField(
        editable=False, max_length=40, unique=True,
        verbose_name=_('Fingerprint')
    )
    length = models.PositiveIntegerField(
        editable=False, verbose_name=_('Length')
    )
    algorithm = models.PositiveIntegerField(
        editable=False, verbose_name=_('Algorithm')
    )
    user_id = models.TextField(editable=False, verbose_name=_('User ID'))
    key_type = models.CharField(
        choices=KEY_TYPE_CHOICES, editable=False, max_length=3,
        verbose_name=_('Type')
    )

    objects = KeyManager()

    class Meta:
        verbose_name = _('Key')
        verbose_name_plural = _('Keys')

    def __str__(self):
        return '{} - {}'.format(self.key_id, self.user_id)

    def clean(self):
        """
        Validate the key before saving.
        """
        import_results = GPGBackend.get_instance().import_key(key_data=self.key_data)

        if not import_results.count:
            raise ValidationError(_('Invalid key data'))

        if Key.objects.filter(fingerprint=import_results.fingerprints[0]).exists():
            raise ValidationError(_('Key already exists.'))

    def get_absolute_url(self):
        return reverse(
            viewname='django_gpg:key_detail', kwargs={'key_id': self.pk}
        )

    @property
    def key_id(self):
        """
        Short form key ID (using the first 8 characters).
        """
        return self.fingerprint[-8:]

    def introspect_key_data(self):
        # Fix the encoding of the key data stream.
        self.key_data = force_text(s=self.key_data)
        import_results, key_info = GPGBackend.get_instance().import_and_list_keys(
            key_data=self.key_data
        )
        logger.debug('key_info: %s', key_info)

        self.algorithm = key_info['algo']
        self.creation_date = make_aware(
            value=datetime.fromtimestamp(int(key_info['date']))
        )
        if key_info['expires']:
            self.expiration_date = make_aware(
                value=datetime.fromtimestamp(
                    int(key_info['expires'])
                )
            )
        self.fingerprint = key_info['fingerprint']
        self.length = int(key_info['length'])
        self.user_id = key_info['uids'][0]
        if OUTPUT_MESSAGE_CONTAINS_PRIVATE_KEY in import_results.results[0]['text']:
            self.key_type = KEY_TYPE_SECRET
        else:
            self.key_type = key_info['type']

    @method_event(
        event_manager_class=EventManagerSave,
        created={
            'event': event_key_created,
            'target': 'self'
        },
    )
    def save(self, *args, **kwargs):
        self.introspect_key_data()
        super().save(*args, **kwargs)

    def sign_file(
        self, file_object, passphrase=None, clearsign=False, detached=False,
        binary=False, output=None
    ):
        """
        Digitally sign a file
        WARNING: using clearsign=True and subsequent decryption corrupts the
        file. Appears to be a problem in python-gnupg or gpg itself.
        https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=55647
        "The problems differ from run to run and file to
        file, and appear to be due to random data being inserted in the
        output data stream."
        """
        file_sign_results = GPGBackend.get_instance().sign_file(
            file_object=file_object, key_data=self.key_data,
            passphrase=passphrase, clearsign=clearsign, detached=detached,
            binary=binary, output=output
        )

        logger.debug('file_sign_results.stderr: %s', file_sign_results.stderr)

        if ERROR_MSG_MISSING_PASSPHRASE in file_sign_results.stderr:
            if ERROR_MSG_GOOD_PASSPHRASE not in file_sign_results.stderr:
                raise NeedPassphrase

        if ERROR_MSG_BAD_PASSPHRASE in file_sign_results.stderr:
            raise PassphraseError

        return file_sign_results
