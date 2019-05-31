from __future__ import unicode_literals

import json
import logging

from django.core import mail
from django.db import models, transaction
from django.template import Context, Template
from django.utils.encoding import force_text, python_2_unicode_compatible
from django.utils.html import strip_tags
from django.utils.module_loading import import_string
from django.utils.translation import ugettext_lazy as _

logger = logging.getLogger(__name__)


@python_2_unicode_compatible
class FieldChoice(models.Model):
    label = models.CharField(max_length=128, verbose_name=_('Label'))
    dotted_path = models.CharField(
        max_length=128, verbose_name=_('Dotted path')
    )

    class Meta:
        ordering = ('label',)
        verbose_name = _('Field choice')
        verbose_name_plural = _('Field choices')

    def __str__(self):
        return self.label


@python_2_unicode_compatible
class FormTemplate(models.Model):
    name = models.CharField(max_length=32, verbose_name=_('Name'))
    label = models.CharField(max_length=128, verbose_name=_('Label'))
    enabled = models.BooleanField(default=True, verbose_name=_('Enabled'))

    class Meta:
        ordering = ('label',)
        verbose_name = _('Form template')
        verbose_name_plural = _('Form templates')

    def __str__(self):
        return self.label

    def get_fields_dictionary(self):
        result = {}

        for field in self.fields.all():
            result[field.name] = {
                'label': field.get_arguments().get('label', self.name),
                'class': field.choice.dotted_path,
                'kwargs': field.get_arguments(),
            }

        return result


class FormTemplateField(models.Model):
    form_template = models.ForeignKey(
        on_delete=models.CASCADE, related_name='fields', to=FormTemplate,
        verbose_name=_('Form template field')
    )
    name = models.CharField(
        max_length=128, verbose_name=_('Name')
    )
    choice = models.ForeignKey(
        on_delete=models.CASCADE, related_name='forms', to=FieldChoice,
        verbose_name=_('Choice')
    )
    arguments = models.TextField(
        blank=True, verbose_name=_('Arguments')
    )
    widget = models.CharField(
        blank=True, max_length=128, verbose_name=_('Widget')
    )
    widget_arguments = models.CharField(
        blank=True, max_length=128, verbose_name=_('Widget arguments')
    )
    enabled = models.BooleanField(default=True, verbose_name=_('Enabled'))

    class Meta:
        verbose_name = _('Form template field')
        verbose_name_plural = _('Form template fields')

    def get_arguments(self):
        return json.loads(self.arguments or '{}')


@python_2_unicode_compatible
class FormInstance(models.Model):
    form_template = models.ForeignKey(
        on_delete=models.CASCADE, related_name='instances', to=FormTemplate,
        verbose_name=_('Form template field')
    )
    data = models.TextField(
        blank=True, verbose_name=_('Data')
    )

    def __init__(self, *args, **kwargs):
        super(FormInstance, self).__init__(*args, **kwargs)
        self.deserialize_data()

    def __str__(self):
        return force_text(self.form_template)

    class Meta:
        verbose_name = _('Form instance')
        verbose_name_plural = _('Form instances')

    def deserialize_data(self):
        self.data = json.loads(self.data or '{}')

    def serialize_data(self):
        self.data = json.dumps(self.data or {})

    def save(self, *args, **kwargs):
        #if not self.pk:
        self.serialize_data()
        return super(FormInstance, self).save(*args, **kwargs)
