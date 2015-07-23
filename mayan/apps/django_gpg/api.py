from __future__ import unicode_literals

import logging
import os
import tempfile

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

import gnupg

from django.utils.translation import ugettext_lazy as _

from .exceptions import *  # NOQA
from .literals import KEY_TYPES

logger = logging.getLogger(__name__)


class KeyStub(object):
    def __init__(self, raw):
        self.key_id = raw['keyid']
        self.key_type = raw['type']
        self.date = raw['date']
        self.expires = raw['expires']
        self.length = raw['length']
        self.uids = raw['uids']


class Key(object):
    @staticmethod
    def get_key_id(fingerprint):
        return fingerprint[-16:]

    @classmethod
    def get_all(cls, gpg, secret=False, exclude=None):
        result = []
        keys = gpg.gpg.list_keys(secret=secret)
        if exclude:
            excluded_id = exclude.key_id
        else:
            excluded_id = ''
        for key in keys:
            if not key['keyid'] in excluded_id:
                key_instance = Key(
                    fingerprint=key['fingerprint'],
                    uids=key['uids'],
                    type=key['type'],
                    data=gpg.gpg.export_keys([key['keyid']], secret=secret)
                )
                result.append(key_instance)

        return result

    @classmethod
    def get(cls, gpg, key_id, secret=False, search_keyservers=False):
        if len(key_id) > 16:
            # key_id is a fingerprint
            key_id = Key.get_key_id(key_id)

        keys = gpg.gpg.list_keys(secret=secret)
        key = next((key for key in keys if key['keyid'] == key_id), None)
        if not key:
            if search_keyservers and secret is False:
                try:
                    gpg.receive_key(key_id)
                    return Key(gpg, key_id)
                except KeyFetchingError:
                    raise KeyDoesNotExist
            else:
                raise KeyDoesNotExist

        key_instance = Key(
            fingerprint=key['fingerprint'],
            uids=key['uids'],
            type=key['type'],
            data=gpg.gpg.export_keys([key['keyid']], secret=secret)
        )

        return key_instance

    def __init__(self, fingerprint, uids, type, data):
        self.fingerprint = fingerprint
        self.uids = uids
        self.type = type
        self.data = data

    @property
    def key_id(self):
        return Key.get_key_id(self.fingerprint)

    @property
    def user_ids(self):
        return ', '.join(self.uids)

    def __str__(self):
        return '%s "%s" (%s)' % (
            self.key_id, self.user_ids, KEY_TYPES.get(self.type, _('Unknown'))
        )

    def __unicode__(self):
        return unicode(self.__str__())

    def __repr__(self):
        return self.__unicode__()


class GPG(object):
    @staticmethod
    def get_descriptor(file_input):
        try:
            # Is it a file like object?
            file_input.seek(0)
        except AttributeError:
            # If not, try open it.
            return open(file_input, 'rb')
        else:
            return file_input

    def __init__(self, binary_path=None, home=None, keyring=None, keyservers=None):
        kwargs = {}
        if binary_path:
            kwargs['gpgbinary'] = binary_path

        if home:
            kwargs['gnupghome'] = home

        if keyring:
            kwargs['keyring'] = keyring

        self.keyservers = keyservers

        try:
            self.gpg = gnupg.GPG(**kwargs)
        except OSError as exception:
            raise GPGException(
                'ERROR: GPG initialization error; Make sure the GPG binary is properly installed; %s' % exception
            )
        except Exception as exception:
            raise GPGException(
                'ERROR: GPG initialization error; %s' % exception
            )

    def verify_file(self, file_input, detached_signature=None, fetch_key=False):
        """
        Verify the signature of a file.
        """

        input_descriptor = GPG.get_descriptor(file_input)

        if detached_signature:
            # Save the original data and invert the argument order
            # Signature first, file second
            file_descriptor, filename = tempfile.mkstemp(prefix='django_gpg')
            os.write(file_descriptor, input_descriptor.read())
            os.close(file_descriptor)

            detached_signature = GPG.get_descriptor(detached_signature)
            signature_file = StringIO()
            signature_file.write(detached_signature.read())
            signature_file.seek(0)
            verify = self.gpg.verify_file(
                signature_file, data_filename=filename
            )
            signature_file.close()
        else:
            verify = self.gpg.verify_file(input_descriptor)

        logger.debug('verify.status: %s', getattr(verify, 'status', None))
        if verify:
            logger.debug('verify ok')
            return verify
        elif getattr(verify, 'status', None) == 'no public key':
            # Exception to the rule, to be able to query the keyservers
            if fetch_key:
                try:
                    self.receive_key(verify.key_id)
                    return self.verify_file(
                        input_descriptor, detached_signature, fetch_key=False
                    )
                except KeyFetchingError:
                    return verify
            else:
                return verify
        else:
            logger.debug('No verify')
            raise GPGVerificationError()

    def verify(self, data):
        # TODO: try to merge with verify_file
        verify = self.gpg.verify(data)

        if verify:
            return verify
        else:
            raise GPGVerificationError(verify.status)

    def sign_file(self, file_input, key=None, destination=None, key_id=None, passphrase=None, clearsign=False):
        """
        Signs a filename, storing the signature and the original file
        in the destination filename provided (the destination file is
        overrided if it already exists), if no destination file name is
        provided the signature is returned.
        """

        kwargs = {}
        kwargs['clearsign'] = clearsign

        if key_id:
            kwargs['keyid'] = key_id

        if key:
            kwargs['keyid'] = key.key_id

        if passphrase:
            kwargs['passphrase'] = passphrase

        input_descriptor = GPG.get_descriptor(file_input)

        if destination:
            output_descriptor = open(destination, 'wb')

        signed_data = self.gpg.sign_file(input_descriptor, **kwargs)
        if not signed_data.fingerprint:
            raise GPGSigningError('Unable to sign file')

        if destination:
            output_descriptor.write(signed_data.data)

        input_descriptor.close()

        if destination:
            output_descriptor.close()

        if not destination:
            return signed_data

    def has_embedded_signature(self, *args, **kwargs):
        try:
            self.decrypt_file(*args, **kwargs)
        except GPGDecryptionError:
            return False
        else:
            return True

    def decrypt_file(self, file_input, close_descriptor=True):
        input_descriptor = GPG.get_descriptor(file_input)

        result = self.gpg.decrypt_file(input_descriptor)
        if close_descriptor:
            input_descriptor.close()

        if not result.status:
            raise GPGDecryptionError('Unable to decrypt file')

        return result

    def create_key(self, *args, **kwargs):
        if kwargs.get('passphrase') == '':
            kwargs.pop('passphrase')

        input_data = self.gpg.gen_key_input(**kwargs)
        key = self.gpg.gen_key(input_data)
        if not key:
            raise KeyGenerationError('Unable to generate key')

        return Key.get(self, key.fingerprint)

    def delete_key(self, key):
        status = self.gpg.delete_keys(
            key.fingerprint, key.type == 'sec'
        ).status
        if status == 'Must delete secret key first':
            self.delete_key(Key.get(self, key.fingerprint, secret=True))
            self.delete_key(key)
        elif status != 'ok':
            raise KeyDeleteError('Unable to delete key')

    def receive_key(self, key_id):
        for keyserver in self.keyservers:
            import_result = self.gpg.recv_keys(keyserver, key_id)
            if import_result:
                return Key.get(
                    self, import_result.fingerprints[0], secret=False
                )

        raise KeyFetchingError

    def query(self, term):
        results = {}
        for keyserver in self.keyservers:
            for key_data in self.gpg.search_keys(query=term, keyserver=keyserver):
                results[key_data['keyid']] = KeyStub(raw=key_data)

        return results.values()

    def import_key(self, key_data):
        import_result = self.gpg.import_keys(key_data)
        logger.debug('import_result: %s', import_result)

        if import_result:
            return Key.get(self, import_result.fingerprints[0], secret=False)

        raise KeyImportError(import_result.results)
