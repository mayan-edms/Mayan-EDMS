from shutil import copyfileobj

import sh

from django.utils.translation import ugettext_lazy as _

from mayan.apps.dependencies.exceptions import DependenciesException
from mayan.apps.storage.utils import NamedTemporaryFile

from ..classes import MIMETypeBackend

from .literals import DEFAULT_MIMETYPE_PATH


class MIMETypeBackendPerlFileMIMEInfo(MIMETypeBackend):
    def _init(self, copy_length=None, mimetype_path=None):
        self.mimetype_path = mimetype_path or DEFAULT_MIMETYPE_PATH
        self.copy_length = copy_length

        try:
            self.command_mimetype = sh.Command(path=self.mimetype_path).bake(
                '--magic-only'
            )
        except sh.CommandNotFound:
            raise DependenciesException(
                _('mimetype not installed or not found.')
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

            filename, mime_type = self.command_mimetype(
                temporary_file_object.name
            ).split()

            return (mime_type, 'binary')
