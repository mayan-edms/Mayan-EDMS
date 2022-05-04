import datetime
from errno import ENOENT
import logging
from stat import S_IFDIR, S_IFREG
from time import time

from fuse import FuseOSError, LoggingMixIn, Operations

from django.core.exceptions import MultipleObjectsReturned
from django.db.models import (
    Case, CharField, Count, F, Func, Transform, Value, When
)
from django.db.models.functions import Concat

from mayan.apps.documents.models import Document

from .literals import (
    MAX_FILE_DESCRIPTOR, MIN_FILE_DESCRIPTOR, FILE_MODE, DIRECTORY_MODE
)
from .runtime import cache

logger = logging.getLogger(name=__name__)


class Trim(Transform):
    function = 'TRIM'
    lookup_name = 'trim'


class MirrorFilesystem(LoggingMixIn, Operations):
    @staticmethod
    def _clean_queryset(queryset, source_field_name, destination_field_name):
        queryset = MirrorFilesystem._clean_queryset_end_of_lines(
            queryset=queryset, source_field_name=source_field_name,
            destination_field_name='_no_newline'
        )

        queryset = MirrorFilesystem._clean_queryset_slashes(
            queryset=queryset, source_field_name='_no_newline'
        )

        return MirrorFilesystem._clean_queryset_duplicates(
            queryset=queryset, destination_field_name=destination_field_name
        )

    @staticmethod
    def _clean_queryset_end_of_lines(
        queryset, source_field_name, destination_field_name='clean_value'
    ):
        # Remove newline carriage returns and the first and last space
        # to make multiline indexes valid directoy names
        return queryset.annotate(
            **{
                destination_field_name: Trim(
                    Func(
                        F(source_field_name), Value('\r\n'), Value(' '),
                        function='replace', output_field=CharField()
                    ),
                )
            }
        )

    @staticmethod
    def _clean_queryset_slashes(
        queryset, source_field_name, destination_field_name='_no_slashes'
    ):
        # This is a conditional expression that is executed only for
        # items in the queryset that contain a slash ('/') in their source
        # field. The slash ('/') character is replaced with an
        # underscore ('_').
        return queryset.annotate(
            **{
                destination_field_name: Case(
                    When(
                        **{
                            '{}__contains'.format(source_field_name): '/',
                            'then': Func(
                                F(source_field_name), Value('/'), Value('_'),
                                function='replace', output_field=CharField()
                            )
                        }
                    ),
                    default=source_field_name
                )
            }
        )

    @staticmethod
    def _clean_queryset_duplicates(
        queryset, source_field_name='_no_slashes',
        destination_field_name='_deduplicated'
    ):
        # Make second queryset of all duplicates
        repeats = queryset.values(source_field_name).annotate(
            repeated_count=Count(source_field_name)
        ).filter(repeated_count__gt=1).values(source_field_name)

        # This is a conditional expression that is executed only for
        # duplicates. The primary key is appended inside a parethesis to
        # the source field.
        return queryset.annotate(
            **{
                destination_field_name: Case(
                    When(
                        **{
                            '{}__in'.format(source_field_name): repeats,
                            'then': Concat(
                                F(source_field_name), Value('('), F('pk'),
                                Value(')'), output_field=CharField()
                            )
                        }
                    ),
                    default=source_field_name
                )
            }
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

        node = self.func_document_container_node()

        if len(parts) > 1 and parts[1] != '':
            path_cache = cache.get_path(path=path)

            if path_cache:
                node_pk = path_cache.get('node_pk')
                if node_pk:
                    if access_only:
                        return True
                    else:
                        return self.func_document_container_node().get_descendants(include_self=True).get(pk=node_pk)

                document_pk = path_cache.get('document_pk')
                if document_pk:
                    if access_only:
                        return True
                    else:
                        return Document.valid.get(pk=document_pk)

            for count, part in enumerate(iterable=parts[1:]):
                try:
                    node_queryset = MirrorFilesystem._clean_queryset(
                        queryset=node.get_descendants(include_self=True),
                        source_field_name=self.node_text_attribute,
                        destination_field_name='value_clean'
                    )
                    node = node_queryset.get(value_clean=part)
                except self.func_document_container_node()._meta.model.DoesNotExist:
                    logger.debug('%s does not exists', part)

                    if directory_only:
                        return None
                    else:
                        try:
                            document = MirrorFilesystem._clean_queryset(
                                queryset=node.get_documents(),
                                source_field_name='label',
                                destination_field_name='label_clean'
                            ).get(label_clean=part)

                            logger.debug(
                                'path %s is a valid file path', path
                            )
                            cache.set_path(path=path, document=document)

                            return document
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

    def __init__(self, func_document_container_node, node_text_attribute):
        self.file_descriptor_count = MIN_FILE_DESCRIPTOR
        self.file_descriptors = {}
        self.func_document_container_node = func_document_container_node
        self.node_text_attribute = node_text_attribute

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

        # st_nlink tracks the number of hard links to a file.
        # Must be 2 for directories and at least 1 for files
        # https://www.gnu.org/software/libc/manual/html_node/Attribute-Meanings.html
        if isinstance(result, Document):
            function_result = {
                'st_mode': (S_IFREG | FILE_MODE),
                'st_ctime': (
                    result.datetime_created.replace(tzinfo=None) - result.datetime_created.utcoffset() - datetime.datetime(1970, 1, 1)
                ).total_seconds(),
                'st_mtime': (
                    result.file_latest.timestamp.replace(tzinfo=None) - result.file_latest.timestamp.utcoffset() - datetime.datetime(1970, 1, 1)
                ).total_seconds(),
                'st_atime': now,
                'st_size': result.file_latest.size or 0,
                'st_nlink': 1
            }
        else:
            function_result = {
                'st_mode': (S_IFDIR | DIRECTORY_MODE), 'st_ctime': now,
                'st_mtime': now, 'st_atime': now, 'st_nlink': 2
            }

        logger.debug('function_result: %s', function_result)
        return function_result

    def open(self, path, flags):
        result = self._path_to_node(path=path, directory_only=False)

        if isinstance(result, Document):
            next_file_descriptor = self._get_next_file_descriptor()
            self.file_descriptors[next_file_descriptor] = result.file_latest.open()
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

        # Serve nodes as directories.
        queryset = MirrorFilesystem._clean_queryset(
            queryset=node.get_children(),
            source_field_name=self.node_text_attribute,
            destination_field_name='value_clean'
        )

        for value in queryset.values_list('value_clean', flat=True):
            yield value

        # Then serve nodes documents as files.
        queryset = MirrorFilesystem._clean_queryset(
            queryset=node.get_documents(), source_field_name='label',
            destination_field_name='label_clean'
        )

        for value in queryset.values_list('label_clean', flat=True):
            yield value

    def release(self, path, fh):
        self.file_descriptors[fh] = None
        del(self.file_descriptors[fh])
