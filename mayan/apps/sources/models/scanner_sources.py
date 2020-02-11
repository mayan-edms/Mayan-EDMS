from __future__ import unicode_literals

import logging
import subprocess

from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from mayan.apps.storage.utils import TemporaryFile

from ..classes import PseudoFile, SourceUploadedFile
from ..exceptions import SourceException
from ..literals import (
    SCANNER_ADF_MODE_CHOICES, SCANNER_MODE_CHOICES, SCANNER_MODE_COLOR,
    SCANNER_SOURCE_CHOICES, SOURCE_CHOICE_SANE_SCANNER,
)
from ..settings import setting_scanimage_path

from .base import InteractiveSource

__all__ = ('SaneScanner',)
logger = logging.getLogger(__name__)


class SaneScanner(InteractiveSource):
    can_compress = False
    is_interactive = True
    source_type = SOURCE_CHOICE_SANE_SCANNER

    device_name = models.CharField(
        max_length=255,
        help_text=_('Device name as returned by the SANE backend.'),
        verbose_name=_('Device name')
    )
    mode = models.CharField(
        blank=True, choices=SCANNER_MODE_CHOICES, default=SCANNER_MODE_COLOR,
        help_text=_(
            'Selects the scan mode (e.g., lineart, monochrome, or color). '
            'If this option is not supported by your scanner, leave it blank.'
        ), max_length=16, verbose_name=_('Mode')
    )
    resolution = models.PositiveIntegerField(
        blank=True, null=True, help_text=_(
            'Sets the resolution of the scanned image in DPI (dots per inch). '
            'Typical value is 200. If this option is not supported by your '
            'scanner, leave it blank.'
        ), verbose_name=_('Resolution')
    )
    source = models.CharField(
        blank=True, choices=SCANNER_SOURCE_CHOICES, help_text=_(
            'Selects the scan source (such as a document-feeder). If this '
            'option is not supported by your scanner, leave it blank.'
        ), max_length=32, null=True, verbose_name=_('Paper source')
    )
    adf_mode = models.CharField(
        blank=True, choices=SCANNER_ADF_MODE_CHOICES,
        help_text=_(
            'Selects the document feeder mode (simplex/duplex). If this '
            'option is not supported by your scanner, leave it blank.'
        ), max_length=16, verbose_name=_('ADF mode')
    )

    objects = models.Manager()

    class Meta:
        verbose_name = _('SANE Scanner')
        verbose_name_plural = _('SANE Scanners')

    def clean_up_upload_file(self, upload_file_object):
        pass

    def execute_command(self, arguments):
        command_line = [
            setting_scanimage_path.value
        ]
        command_line.extend(arguments)

        with TemporaryFile() as stderr_file_object:
            stdout_file_object = TemporaryFile()

            try:
                logger.debug('Scan command line: %s', command_line)
                subprocess.check_call(
                    command_line, stdout=stdout_file_object,
                    stderr=stderr_file_object
                )
            except subprocess.CalledProcessError:
                stderr_file_object.seek(0)
                error_message = stderr_file_object.read()
                logger.error(
                    'Exception while executing scanning command for source:%s ; %s', self,
                    error_message
                )

                message = _(
                    'Error while executing scanning command '
                    '"%(command_line)s"; %(error_message)s'
                ) % {
                    'command_line': ' '.join(command_line),
                    'error_message': error_message
                }
                self.logs.create(message=message)
                raise SourceException(message)
            else:
                stdout_file_object.seek(0)
                return stdout_file_object

    def get_upload_file_object(self, form_data):
        arguments = [
            '-d', self.device_name, '--format', 'tiff',
        ]

        if self.resolution:
            arguments.extend(
                ['--resolution', '{}'.format(self.resolution)]
            )

        if self.mode:
            arguments.extend(
                ['--mode', self.mode]
            )

        if self.source:
            arguments.extend(
                ['--source', self.source]
            )

        if self.adf_mode:
            arguments.extend(
                ['--adf-mode', self.adf_mode]
            )

        file_object = self.execute_command(arguments=arguments)

        return SourceUploadedFile(
            source=self, file=PseudoFile(
                file=file_object, name='scan {}'.format(now())
            )
        )
