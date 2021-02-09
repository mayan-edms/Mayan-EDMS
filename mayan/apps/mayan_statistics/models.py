import json

from django.db import models
from django.utils.translation import ugettext_lazy as _


class StatisticResult(models.Model):
    # Translators: 'Slug' refers to the URL valid ID of the statistic
    # More info: https://docs.djangoproject.com/en/1.7/glossary/#term-slug
    slug = models.SlugField(unique=True, verbose_name=_('Slug'))
    datetime = models.DateTimeField(
        auto_now=True, verbose_name=_('Date time')
    )
    serialize_data = models.TextField(blank=True, verbose_name=_('Data'))

    class Meta:
        verbose_name = _('Statistics result')
        verbose_name_plural = _('Statistics results')

    def __str__(self):
        return self.slug

    def get_data(self):
        return json.loads(s=self.serialize_data)

    def store_data(self, data):
        self.serialize_data = json.dumps(obj=data)
        self.save()
