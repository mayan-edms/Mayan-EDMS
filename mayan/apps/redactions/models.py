from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.converter.models import Transformation


class Redaction(Transformation):
    class Meta:
        proxy = True
        verbose_name = _('Redaction')
        verbose_name_plural = _('Redactions')
