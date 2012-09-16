from __future__ import absolute_import

import logging
import tempfile
import os

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from django.utils.translation import ugettext_lazy as _

from hkp import KeyServer
import gnupg

from .exceptions import (GPGVerificationError, GPGSigningError,
    GPGDecryptionError, KeyDeleteError, KeyGenerationError,
    KeyFetchingError, KeyDoesNotExist, KeyImportError)
from .icons import (icon_bad_signature, icon_no_signature, icon_signature_error,
    icon_no_public_key, icon_good_signature, icon_valid_signature)

logger = logging.getLogger(__name__)

KEY_TYPES = {
    'pub': _(u'Public'),
    'sec': _(u'Secret'),
}

KEY_CLASS_RSA = 'RSA'
KEY_CLASS_DSA = 'DSA'
KEY_CLASS_ELG = 'ELG-E'

KEY_PRIMARY_CLASSES = (
    ((KEY_CLASS_RSA), _(u'RSA')),
    ((KEY_CLASS_DSA), _(u'DSA')),
)

KEY_SECONDARY_CLASSES = (
    ((KEY_CLASS_RSA), _(u'RSA')),
    ((KEY_CLASS_ELG), _(u'Elgamal')),
)

KEYSERVER_DEFAULT_PORT = 11371

SIGNATURE_STATE_BAD = 'signature bad'
SIGNATURE_STATE_NONE = None
SIGNATURE_STATE_ERROR = 'signature error'
SIGNATURE_STATE_NO_PUBLIC_KEY = 'no public key'
SIGNATURE_STATE_GOOD = 'signature good'
SIGNATURE_STATE_VALID = 'signature valid'

SIGNATURE_STATES = {
    SIGNATURE_STATE_BAD: {
        'text': _(u'Bad signature.'),
        'icon': icon_bad_signature
    },
    SIGNATURE_STATE_NONE: {
        'text': _(u'Document not signed or invalid signature.'),
        'icon': icon_no_signature
    },
    SIGNATURE_STATE_ERROR: {
        'text': _(u'Signature error.'),
        'icon': icon_signature_error
    },
    SIGNATURE_STATE_NO_PUBLIC_KEY: {
        'text': _(u'Document is signed but no public key is available for verification.'),
        'icon': icon_no_public_key
    },
    SIGNATURE_STATE_GOOD: {
        'text': _(u'Document is signed, and signature is good.'),
        'icon': icon_good_signature
    },
    SIGNATURE_STATE_VALID: {
        'text': _(u'Document is signed with a valid signature.'),
        'icon': icon_valid_signature
    },
}


class Key(object):
    @staticmethod
    def get_key_id(fingerprint):
        return fingerprint[-16:]

    @classmethod
    def get_all(cls, gpg, secret=False, exclude=None):
        """
        Return a list of Key objects from the specified GPG instance
        """
        result = []
        keys = gpg.gpg.list_keys(secret=secret)
        if exclude:
            excluded_id = exclude.key_id
        else:
            excluded_id = u''
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
        """
        Return a single instance of a Key object from the specified GPG instance
        """
        if len(key_id) > 16:
            # key_id is a fingerprint
            key_id = Key.get_key_id(key_id)

        keys = gpg.gpg.list_keys(secret=secret)
        key = next((key for key in keys if key['keyid'] == key_id), None)
        if not key:
            if search_keyservers and secret == False:
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
        return u', '.join(self.uids)

    def __str__(self):
        return '%s "%s" (%s)' % (self.key_id, self.user_ids, KEY_TYPES.get(self.type, _(u'unknown')))

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

        self.gpg = gnupg.GPG(**kwargs)

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
            verify = self.gpg.verify_file(signature_file, data_filename=filename)
            signature_file.close()
        else:
            verify = self.gpg.verify_file(input_descriptor)

        logger.debug('verify.status: %s' % getattr(verify, 'status', None))
        if verify:
            logger.debug('verify ok')
            return verify
        elif getattr(verify, 'status', None) == 'no public key':
            # Exception to the rule, to be able to query the keyservers
            if fetch_key:
                try:
                    self.receive_key(verify.key_id)
                    return self.verify_file(input_descriptor, detached_signature, fetch_key=False)
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
        """
        Return a boolean result to specify if a passed file has or not
        an embedded signature
        """
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
        if kwargs.get('passphrase') == u'':
            kwargs.pop('passphrase')

        input_data = self.gpg.gen_key_input(**kwargs)
        key = self.gpg.gen_key(input_data)
        if not key:
            raise KeyGenerationError('Unable to generate key')

        return Key.get(self, key.fingerprint)

    def delete_key(self, key):
        status = self.gpg.delete_keys(key.fingerprint, key.type == 'sec').status
        if status == 'Must delete secret key first':
            self.delete_key(Key.get(self, key.fingerprint, secret=True))
            self.delete_key(key)
        elif status != 'ok':
            raise KeyDeleteError('Unable to delete key')

    def delete_all_keys(self):
        """
        Method for clearing the entire key ring
        """
        # Delete secret keys first
        for key in Key.get_all(self, secret=True):
            self.delete_key(key)

        # Delete public keys
        for key in Key.get_all(self, secret=False):
            self.delete_key(key)

    def receive_key(self, key_id):
        for keyserver in self.keyservers:
            import_result = self.gpg.recv_keys(keyserver, key_id)
            if import_result:
                return Key.get(self, import_result.fingerprints[0], secret=False)

        raise KeyFetchingError

    def query(self, term):
        results = {}
        for keyserver in self.keyservers:
            url = u'http://%s' % keyserver
            server = KeyServer(url)
            try:
                key_list = server.search(term)
                for key in key_list:
                    results[key.keyid] = key
            except:
                pass

        return results.values()

    def import_key(self, key_data):
        import_result = self.gpg.import_keys(key_data)
        logger.debug('import_result: %s' % import_result)

        if import_result:
            return Key.get(self, import_result.fingerprints[0], secret=False)

        raise KeyImportError(import_result.results)
