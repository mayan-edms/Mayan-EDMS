import json
import logging
from pathlib import Path

import sh

from django.utils.translation import ugettext_lazy as _

from mayan.apps.storage.utils import fs_cleanup, mkdtemp

from ..literals import DEFAULT_EXIF_PATH
from ..classes import FileMetadataDriver
from ..settings import setting_drivers_arguments

logger = logging.getLogger(name=__name__)


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

    def _process(self, document_file):
        if self.command_exiftool:
            temporary_folder = mkdtemp()
            path_temporary_file = Path(temporary_folder, document_file.document.label)

            try:
                with path_temporary_file.open(mode='xb') as temporary_fileobject:
                    document_file.save_to_file(file_object=temporary_fileobject)
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
            except Exception as exception:
                logger.error(
                    'Error processing document file: %s; %s',
                    document_file, exception, exc_info=True
                )
                raise
            finally:
                fs_cleanup(filename=str(path_temporary_file))
        else:
            logger.warning(
                'EXIFTool binary not found, not processing document '
                'file: %s', document_file
            )

    def read_settings(self):
        self.exiftool_path = setting_drivers_arguments.value.get(
            'exif_driver', {}
        ).get('exiftool_path', DEFAULT_EXIF_PATH)


EXIFToolDriver.register(mimetypes=('*',))
