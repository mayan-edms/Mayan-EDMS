from __future__ import unicode_literals

import logging
import os

from django.core.files import File
from django.db import models
from django.utils.encoding import force_text
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
        help_text=_('Server side filesystem path.'), max_length=255,
        verbose_name=_('Folder path')
    )

    objects = models.Manager()

    class Meta:
        verbose_name = _('Watch folder')
        verbose_name_plural = _('Watch folders')

    def check_source(self):
        # Force self.folder_path to unicode to avoid os.listdir returning
        # str for non-latin filenames, gh-issue #163
        for file_name in os.listdir(force_text(self.folder_path)):
            full_path = os.path.join(self.folder_path, file_name)
            if os.path.isfile(full_path):
                with File(file=open(full_path, mode='rb')) as file_object:
                    self.handle_upload(
                        file_object=file_object,
                        expand=(self.uncompress == SOURCE_UNCOMPRESS_CHOICE_Y),
                        label=file_name
                    )
                    os.unlink(full_path)
