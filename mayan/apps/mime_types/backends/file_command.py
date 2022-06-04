from shutil import copyfileobj

import sh

from django.utils.translation import ugettext_lazy as _

from mayan.apps.dependencies.exceptions import DependenciesException
from mayan.apps.storage.utils import NamedTemporaryFile

from ..classes import MIMETypeBackend

from .literals import DEFAULT_FILE_PATH


class MIMETypeBackendFileCommand(MIMETypeBackend):
    def _init(self, copy_length=None, file_path=None):
        self.file_path = file_path or DEFAULT_FILE_PATH
        self.copy_length = copy_length

        try:
            self.command_file = sh.Command(path=self.file_path).bake(
                brief=True, mime_type=True
            )
        except sh.CommandNotFound:
            raise DependenciesException(
                _('file command not installed or not found.')
            )

    def _get_mime_type(self, file_object, mime_type_only):
        with NamedTemporaryFile() as temporary_file_object:
            file_object.seek(0)
            copyfileobj(
                fsrc=file_object, fdst=temporary_file_object,
                length=self.copy_length
            )
            file_object.seek(0)
            temporary_file_object.seek(0)

            output = self.command_file(
                temporary_file_object.name, mime_encoding=not mime_type_only
            ).split(';')

            file_mime_type = output[0]

            if mime_type_only:
                file_mime_encoding = 'binary'
            else:
                # Remove the ' charset=' string from the output.
                file_mime_encoding = output[1].split(' charset=')[1]

            # Remove trailing newline.
            file_mime_type = file_mime_type.split('\n')[0]
            file_mime_encoding = file_mime_encoding.split('\n')[0]

            return (file_mime_type, file_mime_encoding)
