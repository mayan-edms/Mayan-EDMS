import hashlib

from django.core.cache import caches
from django.utils.encoding import force_bytes

from .settings import (
    setting_document_lookup_cache_timeout, setting_node_lookup_cache_timeout
)


class IndexFilesystemCache:
    @staticmethod
    def get_key_hash(key):
        return hashlib.sha256(force_bytes(s=key)).hexdigest()

    @staticmethod
    def get_document_key(document):
        return IndexFilesystemCache.get_key_hash(
            key='document_pk_{}'.format(document.pk)
        )

    @staticmethod
    def get_node_key(node):
        return IndexFilesystemCache.get_key_hash(
            key='node_pk_{}'.format(node.pk)
        )

    @staticmethod
    def get_path_key(path):
        return IndexFilesystemCache.get_key_hash(
            key='path_{}'.format(path)
        )

    def __init__(self, name='default'):
        self.cache = caches[name]

    def clear_node(self, node):
        node_key = IndexFilesystemCache.get_node_key(node=node)
        path_cache = self.cache.get(key=node_key)
        if path_cache:
            path = path_cache.get('path')
            if path:
                self.clean_path(path=path)

        self.cache.delete(key=node_key)

    def clear_document(self, document):
        document_key = IndexFilesystemCache.get_document_key(document=document)
        path_cache = self.cache.get(key=document_key)
        if path_cache:
            path = path_cache.get('path')
            if path:
                self.clean_path(path=path)

        self.cache.delete(key=document_key)

    def clean_path(self, path):
        self.cache.delete(
            key=IndexFilesystemCache.get_path_key(path=path)
        )

    def get_path(self, path):
        return self.cache.get(
            key=IndexFilesystemCache.get_path_key(path=path)
        )

    def set_path(self, path, document=None, node=None):
        # Must provide a document_pk or a node_pk
        # Not both
        # Providing both is also not correct

        if document:
            self.cache.set(
                key=IndexFilesystemCache.get_path_key(path=path),
                value={'document_pk': document.pk},
                timeout=setting_document_lookup_cache_timeout.value
            )
            self.cache.set(
                key=IndexFilesystemCache.get_document_key(document=document),
                value={'path': path},
                timeout=setting_document_lookup_cache_timeout.value
            )
        elif node:
            self.cache.set(
                key=IndexFilesystemCache.get_path_key(path=path),
                value={'node_pk': node.pk},
                timeout=setting_node_lookup_cache_timeout.value
            )
            self.cache.set(
                key=IndexFilesystemCache.get_node_key(node=node),
                value={'path': path},
                timeout=setting_node_lookup_cache_timeout.value
            )
