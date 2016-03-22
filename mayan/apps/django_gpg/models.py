from __future__ import absolute_import, unicode_literals

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from datetime import date
import logging
import os
import shutil
import tempfile

import gnupg

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.core.files import File
from django.core.urlresolvers import reverse
from django.db import models, transaction
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now
from django.utils.translation import ugettext, ugettext_lazy as _

from .settings import setting_gpg_path, setting_keyservers

logger = logging.getLogger(__name__)


class KeyManager(models.Manager):
    def receive_key(self, key_id):
        temporary_directory = tempfile.mkdtemp()

        os.chmod(temporary_directory, 0x1C0)

        gpg = gnupg.GPG(
            gnupghome=temporary_directory, gpgbinary=setting_gpg_path.value
        )

        import_results = gpg.recv_keys(setting_keyservers.value[0], key_id)

        key_data = gpg.export_keys(import_results.fingerprints[0])

        shutil.rmtree(temporary_directory)

        return self.create(data=key_data)

    def search(self, query):
        temporary_directory = tempfile.mkdtemp()

        gpg = gnupg.GPG(
            gnupghome=temporary_directory, gpgbinary=setting_gpg_path.value
        )

        result = gpg.search_keys(query=query, keyserver=setting_keyservers.value[0])
        shutil.rmtree(temporary_directory)

        return result


@python_2_unicode_compatible
class Key(models.Model):
    data = models.TextField(verbose_name=_('Data'))
    key_id = models.CharField(
        max_length=16, unique=True, verbose_name=_('Key ID')
    )
    creation_date = models.DateField(verbose_name=_('Creation date'))
    expiration_date = models.DateField(
        blank=True, null=True, verbose_name=_('Expiration date')
    )
    fingerprint = models.CharField(
        max_length=40, unique=True, verbose_name=_('Fingerprint')
    )
    length = models.PositiveIntegerField(verbose_name=_('Length'))
    algorithm = models.PositiveIntegerField(verbose_name=_('Algorithm'))
    user_id = models.TextField(verbose_name=_('User ID'))
    key_type = models.CharField(max_length=3, verbose_name=_('Type'))

    objects = KeyManager()

    class Meta:
        verbose_name = _('Key')
        verbose_name_plural = _('Keys')

    def save(self, *args, **kwargs):
        temporary_directory = tempfile.mkdtemp()

        logger.debug('temporary_directory: %s', temporary_directory)

        gpg = gnupg.GPG(
            gnupghome=temporary_directory, gpgbinary=setting_gpg_path.value
        )

        import_results = gpg.import_keys(key_data=self.data)

        logger.debug('import_results.results: %s', import_results.results)
        logger.debug('import_results.fingerprints: %s', import_results.fingerprints)

        key_data = gpg.list_keys(keys=import_results.fingerprints[0])[0]

        logger.debug('key_data: %s', key_data)

        shutil.rmtree(temporary_directory)

        self.key_id = key_data['keyid']
        self.algorithm = key_data['algo']
        self.creation_date = date.fromtimestamp(int(key_data['date']))
        if key_data['expires']:
            self.expiration_date = date.fromtimestamp(int(key_data['expires']))
        self.fingerprint = key_data['fingerprint']
        self.length = int(key_data['length'])
        self.user_id = key_data['uids'][0]
        self.key_type = key_data['type']

        super(Key, self).save(*args, **kwargs)

    def __str__(self):
        return self.key_id

    def sign_file(self, file_object, passphrase=None, clearsign=True, detach=False, binary=False):
        output = StringIO()

        temporary_directory = tempfile.mkdtemp()

        gpg = gnupg.GPG(
            gnupghome=temporary_directory, gpgbinary=setting_gpg_path.value
        )

        import_results = gpg.import_keys(key_data=self.data)

