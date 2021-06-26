import json

from django.db import models
from django.utils.translation import ugettext_lazy as _


# ~ class StoredDashboard(models.Model):
    # ~ name = models.CharField(unique=True, verbose_name=_('Name'))

    # ~ class Meta:
        # ~ verbose_name = _('Stored dashboard')
        # ~ verbose_name_plural = _('Stored dashboards')

    # ~ def __str__(self):
        # ~ return self.name



class DashboardWidgetData(models.Model):
    dashboard_name = models.CharField(verbose_name=_('Dashboard name'))
    name = models.CharField(verbose_name=_('Name'))
    datetime_updated = models.DateTimeField(
        auto_now=True, verbose_name=_('Date time updated')
    )
    serialized_data = models.TextField(
        blank=True, verbose_name=_('Serialized data')
    )

    class Meta:
        unique_together = ('dashboard_name', 'name')
        verbose_name = _('Dashboard widget data')
        verbose_name_plural = _('Dashboard widget data')

    def __str__(self):
        return '{}-{}'.format(self.dashboard_name, self.name)

    def get_serialized_data(self):
        return json.loads(s=self.serialized_data or '{}')

    def set_serialized_data(self, obj, save=True):
        self.serialized_data = json.dumps(obj=obj)
        if save:
            self.save(update_fields=('datetime_updated', 'serialized_data'))
