from __future__ import absolute_import, unicode_literals

from datetime import date
import logging
import os
import shutil
import tempfile

import gnupg

from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from .exceptions import NeedPassphrase, PassphraseError
from .literals import (
    ERROR_MSG_NEED_PASSPHRASE, ERROR_MSG_BAD_PASSPHRASE,
    ERROR_MSG_GOOD_PASSPHRASE, KEY_TYPE_CHOICES, KEY_TYPE_SECRET,
    OUTPUT_MESSAGE_CONTAINS_PRIVATE_KEY
)
from .managers import KeyManager
from .settings import setting_gpg_path

logger = logging.getLogger(__name__)


def gpg_command(function):
    temporary_directory = tempfile.mkdtemp()
    os.chmod(temporary_directory, 0x1C0)

    gpg = gnupg.GPG(
        gnupghome=temporary_directory, gpgbinary=setting_gpg_path.value
    )

    result = function(gpg=gpg)

    shutil.rmtree(temporary_directory)

    return result


@python_2_unicode_compatible
class Key(models.Model):
    key_data = models.TextField(
        help_text=_('ASCII armored version of the key.'),
        verbose_name=_('Key data')
    )
    creation_date = models.DateField(
        editable=False, verbose_name=_('Creation date')
    )
    expiration_date = models.DateField(
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

    def clean(self):
        def import_key(gpg):
            return gpg.import_keys(key_data=self.key_data)

        import_results = gpg_command(function=import_key)

        if not import_results.count:
            raise ValidationError(_('Invalid key data'))

        if Key.objects.filter(fingerprint=import_results.fingerprints[0]).exists():
            raise ValidationError(_('Key already exists.'))

    def get_absolute_url(self):
        return reverse('django_gpg:key_detail', args=(self.pk,))

    def save(self, *args, **kwargs):
        temporary_directory = tempfile.mkdtemp()

        os.chmod(temporary_directory, 0x1C0)

        gpg = gnupg.GPG(
            gnupghome=temporary_directory, gpgbinary=setting_gpg_path.value
        )

        import_results = gpg.import_keys(key_data=self.key_data)

        key_info = gpg.list_keys(keys=import_results.fingerprints[0])[0]

        logger.debug('key_info: %s', key_info)

        shutil.rmtree(temporary_directory)

        self.algorithm = key_info['algo']
        self.creation_date = date.fromtimestamp(int(key_info['date']))
        if key_info['expires']:
            self.expiration_date = date.fromtimestamp(int(key_info['expires']))
        self.fingerprint = key_info['fingerprint']
        self.length = int(key_info['length'])
        self.user_id = key_info['uids'][0]
        if OUTPUT_MESSAGE_CONTAINS_PRIVATE_KEY in import_results.results[0]['text']:
            self.key_type = KEY_TYPE_SECRET
        else:
            self.key_type = key_info['type']

        super(Key, self).save(*args, **kwargs)

    def __str__(self):
        return '{} - {}'.format(self.key_id, self.user_id)

    def sign_file(self, file_object, passphrase=None, clearsign=False, detached=False, binary=False, output=None):
        # WARNING: using clearsign=True and subsequent decryption corrupts the
        # file. Appears to be a problem in python-gnupg or gpg itself.
        # https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=55647
        # "The problems differ from run to run and file to
        # file, and appear to be due to random data being inserted in the
        # output data stream."

        temporary_directory = tempfile.mkdtemp()

        os.chmod(temporary_directory, 0x1C0)

        gpg = gnupg.GPG(
            gnupghome=temporary_directory, gpgbinary=setting_gpg_path.value
        )

        import_results = gpg.import_keys(key_data=self.key_data)

        file_sign_results = gpg.sign_file(
            file=file_object, keyid=import_results.fingerprints[0],
            passphrase=passphrase, clearsign=clearsign, detach=detached,
            binary=binary, output=output
        )

        shutil.rmtree(temporary_directory)

        logger.debug('file_sign_results.stderr: %s', file_sign_results.stderr)

        if ERROR_MSG_NEED_PASSPHRASE in file_sign_results.stderr:
            if ERROR_MSG_BAD_PASSPHRASE in file_sign_results.stderr:
                raise PassphraseError
            elif ERROR_MSG_GOOD_PASSPHRASE not in file_sign_results.stderr:
                raise NeedPassphrase

        return file_sign_results

    @property
    def key_id(self):
        return self.fingerprint[-8:]
