import hashlib
import logging

from django.core import serializers
from django.db import models
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from mayan.apps.databases.model_mixins import ExtraDataModelMixin
from mayan.apps.common.serialization import yaml_load
from mayan.apps.common.validators import YAMLValidator
from mayan.apps.events.classes import (
    EventManagerMethodAfter, EventManagerSave
)
from mayan.apps.events.decorators import method_event
from mayan.apps.events.models import StoredEventType

from mayan.apps.templating.classes import Template

from ..events import event_workflow_template_edited
from ..literals import FIELD_TYPE_CHOICES, WIDGET_CLASS_CHOICES

from .workflow_models import Workflow
from .workflow_state_models import WorkflowState

__all__ = (
    'WorkflowTransition', 'WorkflowTransitionField',
    'WorkflowTransitionTriggerEvent'
)
logger = logging.getLogger(name=__name__)


class WorkflowTransition(ExtraDataModelMixin, models.Model):
    workflow = models.ForeignKey(
        on_delete=models.CASCADE, related_name='transitions', to=Workflow,
        verbose_name=_('Workflow')
    )
    label = models.CharField(
        help_text=_('A short text to describe the transition.'),
        max_length=255, verbose_name=_('Label')
    )
    origin_state = models.ForeignKey(
        on_delete=models.CASCADE, related_name='origin_transitions',
        to=WorkflowState, verbose_name=_('Origin state')
    )
    destination_state = models.ForeignKey(
        on_delete=models.CASCADE, related_name='destination_transitions',
        to=WorkflowState, verbose_name=_('Destination state')
    )
    condition = models.TextField(
        blank=True, help_text=_(
            'The condition that will determine if this transition '
            'is enabled or not. The condition is evaluated against the '
            'workflow instance. Conditions that do not return any value, '
            'that return the Python logical None, or an empty string (\'\') '
            'are considered to be logical false, any other value is '
            'considered to be the logical true.'
        ), verbose_name=_('Condition')
    )

    class Meta:
        ordering = ('label',)
        unique_together = (
            'workflow', 'label', 'origin_state', 'destination_state'
        )
        verbose_name = _('Workflow transition')
        verbose_name_plural = _('Workflow transitions')

    def __str__(self):
        return self.label

    @method_event(
        action_object='self',
        event_manager_class=EventManagerMethodAfter,
        event=event_workflow_template_edited,
        target='workflow',
    )
    def delete(self, *args, **kwargs):
        return super().delete(*args, **kwargs)

    def evaluate_condition(self, workflow_instance):
        if self.has_condition():
            return Template(template_string=self.condition).render(
                context={'workflow_instance': workflow_instance}
            ).strip()
        else:
            return True

    def get_field_display(self):
        field_list = sorted([str(field) for field in self.fields.all()])

        return ', '.join(field_list)

    get_field_display.short_description = _('Fields')

    def get_hash(self):
        result = hashlib.sha256(
            serializers.serialize(format='json', queryset=(self,)).encode()
        )
        for trigger_event in self.trigger_events.all():
            result.update(trigger_event.get_hash().encode())

        for field in self.fields.all():
            result.update(field.get_hash().encode())

        return result.hexdigest()

    def has_condition(self):
        return self.condition.strip()
    has_condition.help_text = _(
        'The transition will be available, depending on the condition '
        'return value.'
    )
    has_condition.short_description = _('Has a condition?')

    @method_event(
        event_manager_class=EventManagerSave,
        created={
            'action_object': 'self',
            'event': event_workflow_template_edited,
            'target': 'workflow',
        },
        edited={
            'action_object': 'self',
            'event': event_workflow_template_edited,
            'target': 'workflow',
        }
    )
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)


class WorkflowTransitionField(ExtraDataModelMixin, models.Model):
    transition = models.ForeignKey(
        on_delete=models.CASCADE, related_name='fields',
        to=WorkflowTransition, verbose_name=_('Transition')
    )
    field_type = models.PositiveIntegerField(
        choices=FIELD_TYPE_CHOICES, verbose_name=_('Type')
    )
    name = models.CharField(
        help_text=_(
            'The name that will be used to identify this field in other parts '
            'of the workflow system.'
        ), max_length=128, verbose_name=_('Internal name')
    )
    label = models.CharField(
        help_text=_(
            'The field name that will be shown on the user interface.'
        ), max_length=128, verbose_name=_('Label'))
    help_text = models.TextField(
        blank=True, help_text=_(
            'An optional message that will help users better understand the '
            'purpose of the field and data to provide.'
        ), verbose_name=_('Help text')
    )
    required = models.BooleanField(
        default=False, help_text=_(
            'Whether this fields needs to be filled out or not to proceed.'
        ), verbose_name=_('Required')
    )
    widget = models.PositiveIntegerField(
        blank=True, choices=WIDGET_CLASS_CHOICES, help_text=_(
            'An optional class to change the default presentation of the field.'
        ), null=True, verbose_name=_('Widget class')
    )
    widget_kwargs = models.TextField(
        blank=True, help_text=_(
            'A group of keyword arguments to customize the widget. '
            'Use YAML format.'
        ), validators=[YAMLValidator()],
        verbose_name=_('Widget keyword arguments')
    )

    class Meta:
        unique_together = ('transition', 'name')
        verbose_name = _('Workflow transition field')
        verbose_name_plural = _('Workflow transition fields')

    def __str__(self):
        return self.label

    @method_event(
        action_object='self',
        event_manager_class=EventManagerMethodAfter,
        event=event_workflow_template_edited,
        target='transition.workflow',
    )
    def delete(self, *args, **kwargs):
        return super().delete(*args, **kwargs)

    def get_hash(self):
        return hashlib.sha256(
            serializers.serialize(format='json', queryset=(self,)).encode()
        ).hexdigest()

    def get_widget_kwargs(self):
        return yaml_load(stream=self.widget_kwargs or '{}')

    @method_event(
        event_manager_class=EventManagerSave,
        created={
            'action_object': 'self',
            'event': event_workflow_template_edited,
            'target': 'transition.workflow',
        },
        edited={
            'action_object': 'self',
            'event': event_workflow_template_edited,
            'target': 'transition.workflow',
        }
    )
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)


class WorkflowTransitionTriggerEvent(models.Model):
    transition = models.ForeignKey(
        on_delete=models.CASCADE, related_name='trigger_events',
        to=WorkflowTransition, verbose_name=_('Transition')
    )
    event_type = models.ForeignKey(
        on_delete=models.CASCADE, to=StoredEventType,
        verbose_name=_('Event type')
    )

    class Meta:
        verbose_name = _('Workflow transition trigger event')
        verbose_name_plural = _('Workflow transitions trigger events')

    def __str__(self):
        return force_text(s=self.transition)

    def get_hash(self):
        return hashlib.sha256(
            serializers.serialize(format='json', queryset=(self,)).encode()
        ).hexdigest()
