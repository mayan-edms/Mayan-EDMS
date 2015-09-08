from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _


DELETE_STALE_UPLOADS_INTERVAL = 60 * 10  # 10 minutes
TIME_DELTA_UNIT_CHOICES = (
    ('days', _('Days')),
    ('hours', _('Hours')),
    ('minutes', _('Minutes')),
)
UPLOAD_EXPIRATION_INTERVAL = 60 * 60 * 24 * 7  # 7 days
