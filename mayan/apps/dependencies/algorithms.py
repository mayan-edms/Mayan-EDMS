from __future__ import print_function, unicode_literals

import base64
import hashlib

from django.utils.encoding import force_text


class HashAlgorithm(object):
    DEFAULT_BLOCK_SIZE = 65535
    _registry = {}
    hash_factory = None

    @classmethod
    def get(cls, name):
        return cls._registry[name]

    @classmethod
    def register(cls, algorithm_class):
        cls._registry[algorithm_class.name] = algorithm_class

    def __init__(self, file_object, block_size=None):
        self.block_size = block_size or self.DEFAULT_BLOCK_SIZE
        self.file_object = file_object
        self.hash_object = self.hash_factory()

    def calculate(self):
        while (True):
            data = self.file_object.read(self.block_size)
            if not data:
                break

            self.hash_object.update(data)

    def get_digest(self):
        return force_text(self._get_digest())


class SHA1Algorithm(HashAlgorithm):
    hash_factory = hashlib.sha1
    name = 'sha1'

    def _get_digest(self):
        return self.hash_object.hexdigest()


class SHA256Algorithm(HashAlgorithm):
    hash_factory = hashlib.sha256
    name = 'sha256'

    def _get_digest(self):
        return base64.b64encode(
            self.hash_object.digest()
        )


class SHA512Algorithm(SHA256Algorithm):
    hash_factory = hashlib.sha512
    name = 'sha512'


HashAlgorithm.register(algorithm_class=SHA1Algorithm)
HashAlgorithm.register(algorithm_class=SHA256Algorithm)
HashAlgorithm.register(algorithm_class=SHA512Algorithm)
