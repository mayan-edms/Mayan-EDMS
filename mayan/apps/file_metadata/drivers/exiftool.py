from __future__ import unicode_literals

import json
import logging

import sh
import yaml

try:
    from yaml import CSafeLoader as SafeLoader
except ImportError:
    from yaml import SafeLoader

from django.utils.translation import ugettext_lazy as _

from mayan.apps.storage.utils import NamedTemporaryFile

from ..literals import DEFAULT_EXIF_PATH
from ..classes import FileMetadataDriver
from ..settings import setting_drivers_arguments

logger = logging.getLogger(__name__)


class EXIFToolDriver(FileMetadataDriver):
    label = _('EXIF Tool')
    internal_name = 'exiftool'

    def __init__(self, *args, **kwargs):
        auto_initialize = kwargs.pop('auto_initialize', True)

        self.read_settings()

        if auto_initialize:
            try:
                self.command_exiftool = sh.Command(path=self.exiftool_path)
            except sh.CommandNotFound:
                self.command_exiftool = None
            else:
                self.command_exiftool = self.command_exiftool.bake('-j')

    def _process(self, document_version):
        if self.command_exiftool:
            temporary_fileobject = NamedTemporaryFile()

            try:
                document_version.save_to_file(file_object=temporary_fileobject)
                temporary_fileobject.seek(0)
                result = self.command_exiftool(temporary_fileobject.name)
                return json.loads(s=result.stdout)[0]
            finally:
                temporary_fileobject.close()
        else:
            logger.warning(
                'EXIFTool binary not found, not processing document '
                'version: %s', document_version
            )

    def read_settings(self):
        driver_arguments = yaml.load(
            stream=setting_drivers_arguments.value, Loader=SafeLoader
        )

        self.exiftool_path = driver_arguments.get(
            'exif_driver', {}
        ).get('exiftool_path', DEFAULT_EXIF_PATH)


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
