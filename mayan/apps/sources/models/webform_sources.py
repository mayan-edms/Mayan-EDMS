import logging

from django.db import models
from django.utils.translation import ugettext_lazy as _

from ..classes import SourceUploadedFile
from ..literals import (
    SOURCE_CHOICE_WEB_FORM, SOURCE_INTERACTIVE_UNCOMPRESS_CHOICES
)

from .base import InteractiveSource

__all__ = ('WebFormSource',)
logger = logging.getLogger(name=__name__)


class WebFormSource(InteractiveSource):
    """
    The webform source is an HTML form with a drag and drop window that opens
    a file browser on the user's computer. This Source is interactive, meaning
    users control live what documents they want to upload. This source is
    useful when admins want to allow users to upload any kind of file as
    documents from their own computers such as when each user has their own
    scanner.
    """
    can_compress = True
    is_interactive = True
    source_type = SOURCE_CHOICE_WEB_FORM

    # TODO: unify uncompress as an InteractiveSource field
    uncompress = models.CharField(
        choices=SOURCE_INTERACTIVE_UNCOMPRESS_CHOICES,
        help_text=_('Whether to expand or not compressed archives.'),
        max_length=1, verbose_name=_('Uncompress')
    )

    objects = models.Manager()

    class Meta:
        verbose_name = _('Web form')
        verbose_name_plural = _('Web forms')

    # Default path
    def get_upload_file_object(self, form_data):
        return SourceUploadedFile(source=self, file=form_data['file'])
