from __future__ import unicode_literals

from django import apps
from django.utils.translation import ugettext_lazy as _


class ConverterApp(apps.AppConfig):
    name = 'converter'
    verbose_name = _('Converter')
