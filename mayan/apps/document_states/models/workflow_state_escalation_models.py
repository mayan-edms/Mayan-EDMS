from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from mayan.apps.common.literals import (
    TIME_DELTA_UNIT_CHOICES, TIME_DELTA_UNIT_DAYS
)
from mayan.apps.databases.model_mixins import ExtraDataModelMixin
from mayan.apps.events.classes import (
    EventManagerMethodAfter, EventManagerSave
)
from mayan.apps.events.decorators import method_event
from mayan.apps.templating.classes import Template

from ..events import event_workflow_template_edited

from .workflow_state_models import WorkflowState
from .workflow_transition_models import WorkflowTransition

__all__ = ('WorkflowStateEscalation',)


class WorkflowStateEscalation(models.Model):
    state = models.ForeignKey(
        on_delete=models.CASCADE, related_name='escalations',
        to=WorkflowState, verbose_name=_('Workflow state')
    )
    transition = models.ForeignKey(
        on_delete=models.CASCADE, related_name='escalations',
        to=WorkflowTransition, verbose_name=_('Transition')
    )
    priority = models.IntegerField(
        blank=True, db_index=True, default=0, help_text=_(
            'Determine the order in which the escalations will be evaluated.'
        ), verbose_name=_('Priority')
    )
    enabled = models.BooleanField(
        default=True, help_text=_(
            'Enable automatic transition the workflow after a specified '
            'amount of time has elapsed in the state without change.'
        ), verbose_name=_('Enable escalation')
    )
    unit = models.CharField(
        blank=True, choices=TIME_DELTA_UNIT_CHOICES,
        default=TIME_DELTA_UNIT_DAYS, max_length=32, verbose_name=_(
            'Expiration time unit'
        )
    )
    amount = models.PositiveIntegerField(
        blank=True, default=1, help_text=_(
            'Amount of the selected expiration units of time.'
        ), verbose_name=_('Expiration amount')
    )
    condition = models.TextField(
        blank=True, help_text=_(
            'The condition that will determine if this state escalation '
            'is executed or not. The condition is evaluated against the '
            'workflow instance. Conditions that do not return any value, '
            'that return the Python logical None, or an empty string (\'\') '
            'are considered to be logical false, any other value is '
            'considered to be the logical true.'
        ), verbose_name=_('Condition')
    )

    class Meta:
        ordering = ('priority',)
        unique_together = ('state', 'transition')
        verbose_name = _('Workflow state escalation')
        verbose_name_plural = _('Workflow state escalations')

    def __str__(self):
        return '{} -> {} ({})'.format(
            self.state, self.transition, self.priority
        )

    @method_event(
        action_object='self',
        event_manager_class=EventManagerMethodAfter,
        event=event_workflow_template_edited,
        target='state.workflow',
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

    def execute(self, context, workflow_instance):
        if self.evaluate_condition(workflow_instance=workflow_instance):
            try:
                self.get_class_instance().execute(context=context)
            except Exception as exception:
                self.error_log.create(
                    text='{}; {}'.format(
                        exception.__class__.__name__, exception
                    )
                )

                if settings.DEBUG or settings.TESTING:
                    raise
            else:
                self.error_log.all().delete()

    def has_condition(self):
        return self.condition.strip()
    has_condition.help_text = _(
        'The state escalation will be executed, depending on the condition '
        'return value.'
    )
    has_condition.short_description = _('Has a condition?')

    @method_event(
        event_manager_class=EventManagerSave,
        created={
            'action_object': 'self',
            'event': event_workflow_template_edited,
            'target': 'state.workflow',
        },
        edited={
            'action_object': 'self',
            'event': event_workflow_template_edited,
            'target': 'state.workflow',
        }
    )
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)
