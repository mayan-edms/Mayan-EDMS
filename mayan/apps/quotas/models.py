import json
import logging

from django.db import models, transaction
from django.utils.encoding import force_text
from django.utils.module_loading import import_string
from django.utils.translation import ugettext_lazy as _

from .classes import NullBackend
from .events import event_quota_created, event_quota_edited

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
    enabled = models.BooleanField(
        default=True, help_text=_(
            'Allow quick disable or enable of the quota.'
        ), verbose_name=_('Enabled')
    )

    class Meta:
        verbose_name = _('Quota')
        verbose_name_plural = _('Quotas')

    def __str__(self):
        return force_text(s=self.backend_label())

    def save(self, *args, **kwargs):
        _user = kwargs.pop('_user', None)

        with transaction.atomic():
            is_new = not self.pk
            super(Quota, self).save(*args, **kwargs)
            if is_new:
                event_quota_created.commit(
                    actor=_user, target=self
                )
            else:
                event_quota_edited.commit(
                    actor=_user, target=self
                )

    def backend_label(self):
        return self.get_backend_instance().label
    backend_label.help_text = _('Driver used for this quota entry.')
    backend_label.short_description = _('Backend')

    def backend_filters(self):
        return self.get_backend_instance().filters()
    backend_filters.short_description = _('Arguments')

    def backend_usage(self):
        return self.get_backend_instance().usage()
    backend_usage.short_description = _('Usage')

    def dumps(self, data):
        self.backend_data = json.dumps(obj=data)
        self.save()

    def get_backend_class(self):
        """
        Retrieves the backend by importing the module and the class.
        """
        try:
            return import_string(dotted_path=self.backend_path)
        except ImportError as exception:
            logger.error(exception)

            return NullBackend

    def get_backend_instance(self):
        try:
            return self.get_backend_class()(**self.loads())
        except Exception as exception:
            logger.error(exception)

            return NullBackend()

    def loads(self):
        return json.loads(s=self.backend_data)
