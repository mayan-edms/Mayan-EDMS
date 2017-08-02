from __future__ import unicode_literals

import json
import logging

from django.db import models
from django.utils.encoding import force_text
from django.utils.module_loading import import_string
from django.utils.translation import ugettext_lazy as _

from .handlers import handler_process_signal

logger = logging.getLogger(__name__)


class Quota(models.Model):
    backend_path = models.CharField(
        max_length=255,
        help_text=_('The dotted Python path to the backend class.'),
        verbose_name=_('Backend path')
    )
    backend_data = models.TextField(
        blank=True, verbose_name=_('Backend data')
    )
    enabled = models.BooleanField(default=True, verbose_name=_('Enabled'))
    editable = models.BooleanField(
        default=True, editable=False, verbose_name=_('Editable')
    )

    class Meta:
        verbose_name = _('Quota')
        verbose_name_plural = _('Quotas')

    def __str__(self):
        return force_text(self.backend_label())

    def save(self, *args, **kwargs):
        result = super(Quota, self).save(*args, **kwargs)
        self.update_receiver()
        return result

    def backend_display(self):
        return self.get_backend_instance().display()

    def backend_label(self):
        return self.get_backend_instance().label

    def backend_usage(self):
        return self.get_backend_instance().usage()

    def dispatch_uid(self):
        return 'quote_{}'.format(self.pk)

    def dumps(self, data):
        self.backend_data = json.dumps(data)
        self.save()

    def get_backend_class(self):
        return import_string(self.backend_path)

    def get_backend_instance(self):
        return self.get_backend_class()(**self.loads())

    def loads(self):
        return json.loads(self.backend_data)

    def update_receiver(self):
        backend_instance = self.get_backend_instance()

        if self.enabled:
            backend_instance.signal.disconnect(
                dispatch_uid=self.dispatch_uid(),
                sender=backend_instance.sender
            )
            backend_instance.signal.connect(
                handler_process_signal,
                dispatch_uid=self.dispatch_uid(),
                sender=backend_instance.sender
            )
        else:
            backend_instance.signal.disconnect(
                dispatch_uid=self.dispatch_uid(),
                sender=backend_instance.sender
            )
