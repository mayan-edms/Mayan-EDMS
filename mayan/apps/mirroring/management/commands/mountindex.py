from __future__ import unicode_literals

import datetime
import logging

from collections import defaultdict
from errno import ENOENT
from stat import S_IFDIR, S_IFLNK, S_IFREG
from sys import argv, exit
from time import time

from fuse import FUSE, FuseOSError, Operations, LoggingMixIn
import pytz

from django.core import management

from djcelery.models import IntervalSchedule, PeriodicTask

from document_indexing.models import Index, IndexInstanceNode
from documents.models import Document

logger = logging.getLogger(__name__)


class IndexFS(LoggingMixIn, Operations):
    @staticmethod
    def path_to_node(path, index, directory_only=True):
        logger.debug('path: %s', path)
        logger.debug('directory_only: %s', directory_only)

        parts = path.split('/')

        logger.debug('parts: %s', parts)

        directory = index.instance_root

        if len(parts) > 1 and parts[1] != '':
            for part in parts[1:]:
                try:
                    directory = directory.children.get(value=part)
                except IndexInstanceNode.DoesNotExist:
                    logger.debug('%s does not exists', part)

                    if directory_only:
                        return None
                    else:
                        try:
                            result = directory.documents.get(label=part)
                            logger.debug('path %s is a valid file path', path)
                            return result
                        except Document.DoesNotExist:
                            logger.debug('path %s is a file, but is not found', path)
                            return None

        logger.debug('directory: %s', directory)
        #logger.debug('directory children: %s', get_children())
        logger.debug('directory is root: %s', directory.is_root_node())

        return directory

    def __init__(self):
        self.fd_count = 0
        self.fd = {}
        self.index = Index.objects.first()

    def getattr(self, path, fh=None):
        now = time()
        result = IndexFS.path_to_node(path=path, index=self.index, directory_only=False)

        if not result:
            raise FuseOSError(ENOENT)

        if isinstance(result, IndexInstanceNode):
            return {
                'st_mode': (S_IFDIR | 0755), 'st_ctime': now, 'st_mtime': now,
                'st_atime': now, 'st_nlink': 2
            }
        else:
            now = time()

            return {
                'st_mode': S_IFREG | 0755,
                'st_ctime': (result.date_added.replace(tzinfo=None) - result.date_added.utcoffset() - datetime.datetime(1970, 1, 1)).total_seconds(),
                'st_mtime': (result.latest_version.timestamp.replace(tzinfo=None) - result.latest_version.timestamp.utcoffset() - datetime.datetime(1970, 1, 1)).total_seconds(),
                'st_atime': now, 'st_nlink': 1,
                'st_size': result.size
            }

    def getxattr(self, path, name, position=0):
        return ''

    def open(self, path, flags):
        result = IndexFS.path_to_node(path=path, index=self.index, directory_only=False)

        if isinstance(result, Document):
            self.fd_count += 1

            self.fd[self.fd_count] = result.open()
            return self.fd_count
        else:
            raiseFuseOSError(ENOENT)

    def read(self, path, size, offset, fh):
        return self.fd[self.fd_count].read(size)

    def readdir(self, path, fh):
        logger.debug('path: %s', path)

        '''
        parts = path.split('/')

        directory = self.index.instance_root

        if len(parts) > 1 and parts[1] != '':
            for part in parts[1:]:
                try:
                    directory = directory.children.get(value=part)
                except IndexInstanceNode.DoesNotExist:
                    logger.debug('%s does not exists', part)
                    raise FuseOSError(ENOENT)

        logger.debug('directory: %s', directory)
        '''

        directory = IndexFS.path_to_node(path=path, index=self.index, directory_only=True)

        if not directory:
            raiseFuseOSError(ENOENT)

        result = ['.', '..']

        directories = directory.get_children().order_by('value')

        for directory in directories:
            value = directory.value.replace('/', '_')
            result.append(value)

        if directory.index_template_node.link_documents:
            for document in directory.documents.all():
                value = document.label.replace('/', '_')
                result.append(value)

        return result


class Command(management.BaseCommand):
    help = 'Mount an index as a FUSE filesystem.'

    def handle(self, *args, **options):
        fuse = FUSE(IndexFS(), '/tmp/mnt', foreground=True)
