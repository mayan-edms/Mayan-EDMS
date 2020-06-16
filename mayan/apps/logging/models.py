from django.apps import apps
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .classes import ErrorLog as ErrorLogProxy


class ErrorLog(models.Model):
    name = models.CharField(
        max_length=128, verbose_name=_('Internal name')
    )

    class Meta:
        ordering = ('name',)
        verbose_name = _('Error log')
        verbose_name_plural = _('Error logs')

    def __str__(self):
        return str(self.app_label)

    @property
    def app_label(self):
        return self.proxy.app_config

    app_label.fget.short_description = _('App label')

    @property
    def proxy(self):
        return ErrorLogProxy.get(name=self.name)


class ErrorLogPartition(models.Model):
    error_log = models.ForeignKey(
        on_delete=models.CASCADE, related_name='partitions', to=ErrorLog,
        verbose_name=_('Error log')
    )
    name = models.CharField(
        db_index=True, max_length=128, verbose_name=_('Internal name')
    )

    class Meta:
        unique_together = ('error_log', 'name')
        verbose_name = _('Error log partition')
        verbose_name_plural = _('Error log partitions')

    def __str__(self):
        return self.name

    def get_model_instance(self):
        app_label, model_name, object_id = self.name.split('.')
        Model = apps.get_model(
            app_label=app_label, model_name=model_name
        )
        return Model._meta.default_manager.get(pk=object_id)


class ErrorLogPartitionEntry(models.Model):
    error_log_partition = models.ForeignKey(
        on_delete=models.CASCADE, related_name='entries',
        to=ErrorLogPartition, verbose_name=_('Error log partition')
    )
    datetime = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name=_('Date and time')
    )
    text = models.TextField(blank=True, null=True, verbose_name=_('Text'))

    class Meta:
        get_latest_by = 'datetime'
        ordering = ('datetime',)
        verbose_name = _('Error log partition entry')
        verbose_name_plural = _('Error log partition entries')

    def __str__(self):
        return '{} {}'.format(self.datetime, self.text)
