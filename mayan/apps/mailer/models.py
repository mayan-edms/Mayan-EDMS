from __future__ import unicode_literals

import logging

from django.db import models
from django.utils.translation import ugettext_lazy as _

logger = logging.getLogger(__name__)


class LogEntry(models.Model):
    datetime = models.DateTimeField(
        auto_now_add=True, editable=False, verbose_name=_('Date time')
    )
    message = models.TextField(
        blank=True, editable=False, verbose_name=_('Message')
    )

    class Meta:
        get_latest_by = 'datetime'
        ordering = ('-datetime',)
        verbose_name = _('Log entry')
        verbose_name_plural = _('Log entries')
