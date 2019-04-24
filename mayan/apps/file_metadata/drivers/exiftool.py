from __future__ import unicode_literals

import json
import logging

import sh

from django.utils.translation import ugettext_lazy as _

from mayan.apps.storage.utils import fs_cleanup, mkstemp

from ..classes import FileMetadataDriver
from ..settings import setting_drivers_arguments

logger = logging.getLogger(__name__)


class EXIFToolDriver(FileMetadataDriver):
    label = _('EXIF Tool')
    internal_name = 'exiftool'

    def __init__(self, *args, **kwargs):
        try:
            self.command_exiftool = sh.Command(
                setting_drivers_arguments.value['exif_driver']['exiftool_path']
            )
        except sh.CommandNotFound:
            self.command_exiftool = None
        else:
            self.command_exiftool = self.command_exiftool.bake('-j')

    def _process(self, document_version):
        if self.command_exiftool:
            new_file_object, temp_filename = mkstemp()

            try:
                document_version.save_to_file(filepath=temp_filename)
                result = self.command_exiftool(temp_filename)
                return json.loads(s=result.stdout)[0]
            finally:
                fs_cleanup(filename=temp_filename)
        else:
            logger.warning(
                'EXIFTool binary not found, not processing document version: %s',
                document_version
            )


EXIFToolDriver.register(
    mimetypes=(
        'application/msword',
        'application/pdf',
        'application/vnd.oasis.opendocument.text',
        'application/vnd.openxmlformats-officedocument.presentationml.presentation',
        'application/x-bittorrent',
        'application/x-gzip',
        'application/x-rar-compressed',
        'application/x-shockwave-flash',
        'application/zip',
        'application/zip',
        'audio/x-pn-realaudio-plugin',
        'audio/x-wav',
        'image/jpeg',
        'image/png',
        'image/svg+xml',
        'image/tiff',
        'image/x-portable-pixmap',
        'text/html',
        'text/rtf',
        'text/x-sh',
        'video/mp4',
        'video/webm',
        'video/x-flv',
        'video/x-matroska'
    )
)
