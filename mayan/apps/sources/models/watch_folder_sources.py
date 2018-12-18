from __future__ import unicode_literals

import logging

from pathlib2 import Path

from django.db import models
from django.utils.translation import ugettext_lazy as _

from ..literals import SOURCE_CHOICE_WATCH, SOURCE_UNCOMPRESS_CHOICE_Y

from .base import IntervalBaseModel

__all__ = ('WatchFolderSource',)
logger = logging.getLogger(__name__)


class WatchFolderSource(IntervalBaseModel):
    """
    The watch folder is another non-interactive source that like the email
    source, works by periodically checking and processing documents. This
    source instead of using an email account, monitors a filesystem folder.
    Administrators can define watch folders, examples /home/mayan/watch_bills
    or /home/mayan/watch_invoices and users just need to copy the documents
    they want to upload as a bill or invoice to the respective filesystem
    folder. Mayan will periodically scan these filesystem locations and
    upload the files as documents, deleting them if configured.
    """
    source_type = SOURCE_CHOICE_WATCH

    folder_path = models.CharField(
        help_text=_('Server side filesystem path to scan for files.'),
        max_length=255, verbose_name=_('Folder path')
    )
    include_subdirectories = models.BooleanField(
        help_text=_(
            'If checked, not only will the folder path be scanned for files '
            'but also its subdirectories.'
        ),
        verbose_name=_('Include subdirectories?')
    )

    objects = models.Manager()

    class Meta:
        verbose_name = _('Watch folder')
        verbose_name_plural = _('Watch folders')

    def check_source(self, test=False):
        path = Path(self.folder_path)

        if self.include_subdirectories:
            iterator = path.rglob('*')
        else:
            iterator = path.glob('*')

        for entry in iterator:
            if entry.is_file() or entry.is_symlink():
                with entry.open(mode='rb') as file_object:
                    self.handle_upload(
                        file_object=file_object,
                        expand=(self.uncompress == SOURCE_UNCOMPRESS_CHOICE_Y),
                        label=entry.name
                    )
                    if not test:
                        entry.unlink()
