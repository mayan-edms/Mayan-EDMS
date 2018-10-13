from __future__ import print_function, unicode_literals

import datetime
from errno import ENOENT
import logging
from stat import S_IFDIR, S_IFREG
from time import time

from fuse import FuseOSError, Operations

from django.core.exceptions import MultipleObjectsReturned
from django.db.models import Count, F, Func, Transform, Value

from document_indexing.models import Index, IndexInstanceNode
from documents.models import Document

from .literals import (
    MAX_FILE_DESCRIPTOR, MIN_FILE_DESCRIPTOR, FILE_MODE, DIRECTORY_MODE
)
from .runtime import cache


logger = logging.getLogger(__name__)


class Trim(Transform):
    function = 'TRIM'
    lookup_name = 'trim'


class IndexFilesystem(Operations):
    @staticmethod
    def _clean_queryset(queryset):
        # Remove newline carriage returns and the first and last space
        # to make multiline indexes
        # valid directoy names
        return queryset.annotate(
            clean_value=Trim(
                Func(
                    F('value'), Value('\r\n'), Value(' '), function='replace'
                ),
            )
        )

    def _get_next_file_descriptor(self):
        while(True):
            self.file_descriptor_count += 1
            if self.file_descriptor_count > MAX_FILE_DESCRIPTOR:
                self.file_descriptor_count = MIN_FILE_DESCRIPTOR

            try:
                if not self.file_descriptors[self.file_descriptor_count]:
                    return self.file_descriptor_count
            except KeyError:
                return self.file_descriptor_count

    def _path_to_node(self, path, access_only=False, directory_only=True):
        logger.debug('path: %s', path)
        logger.debug('directory_only: %s', directory_only)

        parts = path.split('/')

        logger.debug('parts: %s', parts)

        node = self.index.instance_root

        if len(parts) > 1 and parts[1] != '':
            path_cache = cache.get_path(path=path)

            if path_cache:
                node_pk = path_cache.get('node_pk')
                if node_pk:
                    if access_only:
                        return True
                    else:
                        return IndexInstanceNode.objects.get(pk=node_pk)

                document_pk = path_cache.get('document_pk')
                if document_pk:
                    if access_only:
                        return True
                    else:
                        return Document.objects.get(
                            is_stub=False, pk=document_pk
                        )

            for count, part in enumerate(parts[1:]):
                try:
                    node = IndexFilesystem._clean_queryset(node.get_children()).get(clean_value=part)
                except IndexInstanceNode.DoesNotExist:
                    logger.debug('%s does not exists', part)

                    if directory_only:
                        return None
                    else:
                        try:
                            if node.index_template_node.link_documents:
                                document = node.documents.get(
                                    is_stub=False, label=part
                                )
                                logger.debug(
                                    'path %s is a valid file path', path
                                )
                                cache.set_path(path=path, document=document)

                                return document
                            else:
                                return None
                        except Document.DoesNotExist:
                            logger.debug(
                                'path %s is a file, but is not found', path
                            )
                            return None
                        except MultipleObjectsReturned:
                            return None
                except MultipleObjectsReturned:
                    return None

            cache.set_path(path=path, node=node)

        logger.debug('node: %s', node)
        logger.debug('node is root: %s', node.is_root_node())

        return node

    def __init__(self, index_slug):
        self.file_descriptor_count = MIN_FILE_DESCRIPTOR
        self.file_descriptors = {}

        try:
            self.index = Index.objects.get(slug=index_slug)
        except Index.DoesNotExist:
            print('Unknown index slug: {}.'.format(index_slug))
            exit(1)

    def access(self, path, fh=None):
        result = self._path_to_node(
            path=path, access_only=True, directory_only=False
        )

        if not result:
            raise FuseOSError(ENOENT)

    def getattr(self, path, fh=None):
        logger.debug('path: %s, fh: %s', path, fh)

        now = time()
        result = self._path_to_node(path=path, directory_only=False)

        if not result:
            raise FuseOSError(ENOENT)

        if isinstance(result, IndexInstanceNode):
            return {
                'st_mode': (S_IFDIR | DIRECTORY_MODE), 'st_ctime': now,
                'st_mtime': now, 'st_atime': now, 'st_nlink': 2
            }
        else:
            return {
                'st_mode': (S_IFREG | FILE_MODE),
                'st_ctime': (
                    result.date_added.replace(tzinfo=None) - result.date_added.utcoffset() - datetime.datetime(1970, 1, 1)
                ).total_seconds(),
                'st_mtime': (
                    result.latest_version.timestamp.replace(tzinfo=None) - result.latest_version.timestamp.utcoffset() - datetime.datetime(1970, 1, 1)
                ).total_seconds(),
                'st_atime': now,
                'st_size': result.size
            }

    def open(self, path, flags):
        result = self._path_to_node(path=path, directory_only=False)

        if isinstance(result, Document):
            next_file_descriptor = self._get_next_file_descriptor()
            self.file_descriptors[next_file_descriptor] = result.open()
            return next_file_descriptor
        else:
            raise FuseOSError(ENOENT)

    def read(self, path, size, offset, fh):
        self.file_descriptors[fh].seek(offset)
        return self.file_descriptors[fh].read(size)

    def readdir(self, path, fh):
        logger.debug('path: %s', path)

        node = self._path_to_node(path=path, directory_only=True)

        if not node:
            raise FuseOSError(ENOENT)

        yield '.'
        yield '..'

        # Index instance nodes to directories
        queryset = IndexFilesystem._clean_queryset(node.get_children()).exclude(
            clean_value__contains='/'
        ).values('clean_value')

        # Find nodes with the same resulting value and remove them
        for duplicate in queryset.order_by().annotate(count_id=Count('id')).filter(count_id__gt=1):
            queryset = queryset.exclude(clean_value=duplicate['clean_value'])

        for value in queryset.values_list('clean_value', flat=True):
            yield value

        # Documents
        if node.index_template_node.link_documents:
            queryset = node.documents.filter(is_stub=False).values('label').exclude(
                label__contains='/'
            )

            # Find duplicated document and remove them
            for duplicate in queryset.order_by().annotate(count_id=Count('id')).filter(count_id__gt=1):
                queryset = queryset.exclude(label=duplicate['label'])

            for document_label in queryset.values_list('label', flat=True):
                yield document_label

    def release(self, path, fh):
        self.file_descriptors[fh] = None
        del(self.file_descriptors[fh])
