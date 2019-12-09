from __future__ import unicode_literals

import json
import logging

import sh

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
                try:
                    result = self.command_exiftool(temporary_fileobject.name)
                except sh.ErrorReturnCode_1 as exception:
                    result = json.loads(s=exception.stdout)[0]
                    if result.get('Error', '') == 'Unknown file type':
                        # Not a fatal error
                        return result
                else:
                    return json.loads(s=result.stdout)[0]
            finally:
                temporary_fileobject.close()
        else:
            logger.warning(
                'EXIFTool binary not found, not processing document '
                'version: %s', document_version
            )

    def read_settings(self):
        self.exiftool_path = setting_drivers_arguments.value.get(
            'exif_driver', {}
        ).get('exiftool_path', DEFAULT_EXIF_PATH)


EXIFToolDriver.register(mimetypes=('*',))
