import logging
import os

from django.db import models
from django.utils.translation import ugettext_lazy as _

from ..classes import SourceUploadedFile, StagingFile
from ..literals import (
    SOURCE_CHOICE_STAGING, SOURCE_INTERACTIVE_UNCOMPRESS_CHOICES
)

from .base import InteractiveSource

__all__ = ('StagingFolderSource',)
logger = logging.getLogger(name=__name__)


class StagingFolderSource(InteractiveSource):
    """
    The Staging folder source is interactive but instead of displaying an
    HTML form (like the Webform source) that allows users to freely choose a
    file from their computers, shows a list of files from a filesystem folder.
    When creating staging folders administrators choose a folder in the same
    machine where Mayan is installed. This folder is then used as the
    destination location of networked scanners or multifunctional copiers.
    The scenario for staging folders is as follows: An user walks up to the
    networked copier, scan several papers documents, returns to their
    computer, open Mayan, select to upload a new document but choose the
    previously defined staging folder source, now they see the list of
    documents with a small preview and can proceed to process one by one and
    convert the scanned files into Mayan EDMS documents. Staging folders are
    useful when many users share a few networked scanners.
    """
    can_compress = True
    is_interactive = True
    source_type = SOURCE_CHOICE_STAGING

    folder_path = models.CharField(
        max_length=255, help_text=_('Server side filesystem path.'),
        verbose_name=_('Folder path')
    )
    preview_width = models.IntegerField(
        help_text=_('Width value to be passed to the converter backend.'),
        verbose_name=_('Preview width')
    )
    preview_height = models.IntegerField(
        blank=True, null=True,
        help_text=_('Height value to be passed to the converter backend.'),
        verbose_name=_('Preview height')
    )
    uncompress = models.CharField(
        choices=SOURCE_INTERACTIVE_UNCOMPRESS_CHOICES, max_length=1,
        help_text=_('Whether to expand or not compressed archives.'),
        verbose_name=_('Uncompress')
    )
    delete_after_upload = models.BooleanField(
        default=True,
        help_text=_(
            'Delete the file after is has been successfully uploaded.'
        ),
        verbose_name=_('Delete after upload')
    )

    objects = models.Manager()

    class Meta:
        verbose_name = _('Staging folder')
        verbose_name_plural = _('Staging folders')

    def clean_up_upload_file(self, upload_file_object):
        if self.delete_after_upload:
            try:
                upload_file_object.extra_data.delete()
            except Exception as exception:
                logger.error(
                    'Error deleting staging file: %s; %s',
                    upload_file_object, exception, exc_info=True
                )
                raise

    def get_file(self, *args, **kwargs):
        return StagingFile(staging_folder=self, *args, **kwargs)

    def get_files(self):
        try:
            for entry in sorted([os.path.normcase(f) for f in os.listdir(self.folder_path) if os.path.isfile(os.path.join(self.folder_path, f))]):
                yield self.get_file(filename=entry)
        except OSError as exception:
            logger.error(
                'Unable get list of staging files from source: %s; %s',
                self, exception
            )
            raise

    def get_upload_file_object(self, form_data):
        staging_file = self.get_file(
            encoded_filename=form_data['staging_file_id']
        )
        return SourceUploadedFile(
            source=self, file=staging_file.as_file(), extra_data=staging_file
        )
