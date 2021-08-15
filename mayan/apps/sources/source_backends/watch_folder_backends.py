import logging
from pathlib import Path

from django.core.files import File
from django.utils.translation import ugettext_lazy as _

from mayan.apps.storage.models import SharedUploadedFile

from ..classes import SourceBackend
from ..exceptions import SourceException

from .literals import SOURCE_INTERVAL_UNCOMPRESS_CHOICES
from .mixins import (
    SourceBackendCompressedMixin, SourceBackendPeriodicMixin, SourceBaseMixin
)

__all__ = ('SourceBackendWatchFolder',)
logger = logging.getLogger(name=__name__)


class SourceBackendWatchFolder(
    SourceBackendCompressedMixin, SourceBackendPeriodicMixin,
    SourceBaseMixin, SourceBackend
):
    field_order = ('folder_path', 'include_subdirectories',)
    fields = {
        'folder_path': {
            'class': 'django.forms.CharField',
            'default': '',
            'help_text': _(
                'Server side filesystem path.'
            ),
            'kwargs': {
                'max_length': 255,
            },
            'label': _('Folder path'),
            'required': True
        },
        'include_subdirectories': {
            'class': 'django.forms.BooleanField',
            'default': '',
            'help_text': _(
                'If checked, not only will the folder path be scanned for '
                'files but also its subdirectories.'
            ),
            'label': _('Include subdirectories?'),
            'required': False
        },
    }
    label = _('Watch folder')
    uncompress_choices = SOURCE_INTERVAL_UNCOMPRESS_CHOICES

    def get_shared_uploaded_files(self):
        dry_run = self.process_kwargs.get('dry_run', False)

        path = Path(self.kwargs['folder_path'])

        # Force testing the path and raise errors for the log.
        path.lstat()
        if not path.is_dir():
            raise SourceException('Path {} is not a directory.'.format(path))

        if self.kwargs['include_subdirectories']:
            iterator = path.rglob(pattern='*')
        else:
            iterator = path.glob(pattern='*')

        for entry in iterator:
            if entry.is_file() or entry.is_symlink():
                with entry.open(mode='rb+') as file_object:
                    shared_uploaded_file = SharedUploadedFile.objects.create(
                        file=File(file=file_object), filename=entry.name
                    )
                    if not dry_run:
                        entry.unlink()

                    return (shared_uploaded_file,)
