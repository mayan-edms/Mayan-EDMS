from __future__ import unicode_literals

import datetime
from errno import ENOENT
import logging
from optparse import make_option
from stat import S_IFDIR, S_IFREG
from time import time

from fuse import FUSE, FuseOSError, Operations
import pytz

from django.core import management

from djcelery.models import IntervalSchedule, PeriodicTask

from document_indexing.models import Index, IndexInstanceNode
from documents.models import Document

MAX_FILE_DESCRIPTOR = 65535
MIN_FILE_DESCRIPTOR = 0
logger = logging.getLogger(__name__)


class IndexFS(Operations):
    def _path_to_node(self, path, directory_only=True):
        logger.debug('path: %s', path)
        logger.debug('directory_only: %s', directory_only)

        parts = path.split('/')

        logger.debug('parts: %s', parts)

        node = self.index.instance_root

        if len(parts) > 1 and parts[1] != '':
            for part in parts[1:]:
                try:
                    node = node.children.get(value=part)
                except IndexInstanceNode.DoesNotExist:
                    logger.debug('%s does not exists', part)

                    if directory_only:
                        return None
                    else:
                        try:
                            if node.index_template_node.link_documents:
                                result = node.documents.get(label=part)
                                logger.debug('path %s is a valid file path', path)
                                return result
                            else:
                                return None
                        except Document.DoesNotExist:
                            logger.debug('path %s is a file, but is not found', path)
                            return None

        logger.debug('node: %s', node)
        logger.debug('node is root: %s', node.is_root_node())

        return node

    def __init__(self, index_slug):
        self.fd_count = MIN_FILE_DESCRIPTOR
        self.fd = {}
        try:
            self.index = Index.objects.get(slug=index_slug)
        except Index.DoesNotExist:
            print 'Unknown index.'
            exit(1)

    def getattr(self, path, fh=None):
        logger.debug('path: %s, fh: %s', path, fh)

        now = time()
        result = self._path_to_node(path=path, directory_only=False)

        if not result:
            raise FuseOSError(ENOENT)

        if isinstance(result, IndexInstanceNode):
            return {
                'st_mode': (S_IFDIR | 0555), 'st_ctime': now, 'st_mtime': now,
                'st_atime': now, 'st_nlink': 2
            }
        else:
            return {
                'st_mode': (S_IFREG | 0555),
                'st_ctime': (result.date_added.replace(tzinfo=None) - result.date_added.utcoffset() - datetime.datetime(1970, 1, 1)).total_seconds(),
                'st_mtime': (result.latest_version.timestamp.replace(tzinfo=None) - result.latest_version.timestamp.utcoffset() - datetime.datetime(1970, 1, 1)).total_seconds(),
                'st_atime': now,
                'st_size': result.size
            }

    def getxattr(self, path, name, position=0):
        return ''

    def open(self, path, flags):
        result = self._path_to_node(path=path, directory_only=False)

        if isinstance(result, Document):
            self.fd_count += 1
            if self.fd_count > MAX_FILE_DESCRIPTOR:
                self.fb_count = MIN_FILE_DESCRIPTOR
            # TODO: implement _get_next_file_descriptor()
            # TODO: don't provide a file descriptor already in use

            self.fd[self.fd_count] = result.open()
            return self.fd_count
        else:
            raiseFuseOSError(ENOENT)

    def release(self, path, fh):
        self.fd[fh] = None
        del(self.fd[fh])

    def read(self, path, size, offset, fh):
        return self.fd[self.fd_count].read(size)

    def readdir(self, path, fh):
        logger.debug('path: %s', path)

        node = self._path_to_node(path=path, directory_only=True)

        if not node:
            raiseFuseOSError(ENOENT)

        result = ['.', '..']

        for child_node in node.get_children().values_list('value', flat=True):
            if '/' not in child_node:
                result.append(child_node)

        if node.index_template_node.link_documents:
            for document in node.documents.all():
                if '/' not in document.label:
                    result.append(document.label)

        return result


class Command(management.BaseCommand):
    help = 'Mount an index as a FUSE filesystem.'

    option_list = management.BaseCommand.option_list + (
        make_option(
            '--index',
            action='store',
            dest='index',
            help='Index to mirror at the mount point.'
        ),

        make_option(
            '--mountpoint',
            action='store',
            dest='mountpoint',
            help='Filesystem location at which to mount the selected index.'
        ),
    )

    def handle(self, *args, **options):
        fuse = FUSE(operations=IndexFS(index_slug=options['index']), mountpoint=options['mountpoint'], foreground=True)
