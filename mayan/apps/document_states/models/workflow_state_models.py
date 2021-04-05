import hashlib
import json
import logging

from django.apps import apps
from django.conf import settings
from django.core import serializers
from django.db import models
from django.db.models import F, Max, Q
from django.utils.module_loading import import_string
from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.models import AccessControlList
from mayan.apps.databases.model_mixins import ExtraDataModelMixin
from mayan.apps.documents.models import Document
from mayan.apps.documents.permissions import permission_document_view
from mayan.apps.events.classes import (
    EventManagerMethodAfter, EventManagerSave
)
from mayan.apps.events.decorators import method_event

from mayan.apps.templating.classes import Template

from ..events import event_workflow_template_edited
from ..literals import (
    WORKFLOW_ACTION_WHEN_CHOICES, WORKFLOW_ACTION_ON_ENTRY,
    WORKFLOW_ACTION_ON_EXIT
)

from .workflow_models import Workflow

__all__ = (
    'WorkflowState', 'WorkflowStateAction', 'WorkflowStateRuntimeProxy'
)
logger = logging.getLogger(name=__name__)


class WorkflowState(ExtraDataModelMixin, models.Model):
    """
    Fields:
    * completion - Completion Amount - A user defined numerical value to help
    determine if the workflow of the document is nearing completion (100%).
    The Completion Amount will be determined by the completion value of the
    Actual State. Example: If the workflow has 3 states: registered, approved,
    archived; the admin could give the follow completion values to the
    states: 33%, 66%, 100%. If the Actual State of the document if approved,
    the Completion Amount will show 66%.
    """
    workflow = models.ForeignKey(
        on_delete=models.CASCADE, related_name='states', to=Workflow,
        verbose_name=_('Workflow')
    )
    label = models.CharField(
        help_text=_('A short text to describe the workflow state.'),
        max_length=255, verbose_name=_('Label')
    )
    initial = models.BooleanField(
        default=False,
        help_text=_(
            'The state at which the workflow will start in. Only one state '
            'can be the initial state.'
        ), verbose_name=_('Initial')
    )
    completion = models.IntegerField(
        blank=True, default=0, help_text=_(
            'The percent of completion that this state represents in '
            'relation to the workflow. Use numbers without the percent sign.'
        ), verbose_name=_('Completion')
    )

    class Meta:
        ordering = ('label',)
        unique_together = ('workflow', 'label')
        verbose_name = _('Workflow state')
        verbose_name_plural = _('Workflow states')

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

    @property
    def entry_actions(self):
        return self.actions.filter(when=WORKFLOW_ACTION_ON_ENTRY)

    @property
    def exit_actions(self):
        return self.actions.filter(when=WORKFLOW_ACTION_ON_EXIT)

    def get_documents(self):
        WorkflowInstanceLogEntry = apps.get_model(
            app_label='document_states',
            model_name='WorkflowInstanceLogEntry'
        )

        latest_entries = WorkflowInstanceLogEntry.objects.annotate(
            max_datetime=Max(
                'workflow_instance__log_entries__datetime'
            )
        ).filter(
            datetime=F('max_datetime')
        )

        state_latest_entries = latest_entries.filter(
            transition__destination_state=self
        )

        return Document.valid.filter(
            Q(
                workflows__pk__in=state_latest_entries.values_list(
                    'workflow_instance', flat=True
                )
            ) | Q(
                workflows__log_entries__isnull=True,
                workflows__workflow__states=self,
                workflows__workflow__states__initial=True
            )
        ).distinct()

    def get_hash(self):
        result = hashlib.sha256(
            serializers.serialize(format='json', queryset=(self,)).encode()
        )
        for action in self.actions.all():
            result.update(action.get_hash().encode())

        return result.hexdigest()

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
        # Solve issue #557 "Break workflows with invalid input"
        # without using a migration.
        # Remove blank=True, remove this, and create a migration in the next
        # minor version.

        try:
            self.completion = int(self.completion)
        except (TypeError, ValueError):
            self.completion = 0

        if self.initial:
            self.workflow.states.all().update(initial=False)
        return super().save(*args, **kwargs)


class WorkflowStateAction(ExtraDataModelMixin, models.Model):
    state = models.ForeignKey(
        on_delete=models.CASCADE, related_name='actions', to=WorkflowState,
        verbose_name=_('Workflow state')
    )
    label = models.CharField(
        max_length=255, help_text=_('A short text describing the action.'),
        verbose_name=_('Label')
    )
    enabled = models.BooleanField(default=True, verbose_name=_('Enabled'))
    when = models.PositiveIntegerField(
        choices=WORKFLOW_ACTION_WHEN_CHOICES,
        default=WORKFLOW_ACTION_ON_ENTRY, help_text=_(
            'At which moment of the state this action will execute.'
        ), verbose_name=_('When')
    )
    action_path = models.CharField(
        max_length=128, help_text=_(
            'The dotted Python path to the workflow action class to execute.'
        ), verbose_name=_('Entry action path')
    )
    action_data = models.TextField(
        blank=True, verbose_name=_('Entry action data')
    )
    condition = models.TextField(
        blank=True, help_text=_(
            'The condition that will determine if this state action '
            'is executed or not. The condition is evaluated against the '
            'workflow instance. Conditions that do not return any value, '
            'that return the Python logical None, or an empty string (\'\') '
            'are considered to be logical false, any other value is '
            'considered to be the logical true.'
        ), verbose_name=_('Condition')
    )

    class Meta:
        ordering = ('label',)
        unique_together = ('state', 'label')
        verbose_name = _('Workflow state action')
        verbose_name_plural = _('Workflow state actions')

    def __str__(self):
        return self.label

    @method_event(
        action_object='self',
        event_manager_class=EventManagerMethodAfter,
        event=event_workflow_template_edited,
        target='state.workflow',
    )
    def delete(self, *args, **kwargs):
        return super().delete(*args, **kwargs)

    def dumps(self, data):
        self.action_data = json.dumps(obj=data)
        self.save()

    def get_hash(self):
        return hashlib.sha256(
            serializers.serialize(format='json', queryset=(self,)).encode()
        ).hexdigest()

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

    def get_class(self):
        return import_string(dotted_path=self.action_path)

    def get_class_instance(self):
        return self.get_class()(form_data=self.loads())

    def get_class_label(self):
        try:
            return self.get_class().label
        except ImportError:
            return _('Unknown action type')

    def has_condition(self):
        return self.condition.strip()
    has_condition.help_text = _(
        'The state action will be executed, depending on the condition '
        'return value.'
    )
    has_condition.short_description = _('Has a condition?')

    def loads(self):
        return json.loads(s=self.action_data or '{}')

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


class WorkflowStateRuntimeProxy(WorkflowState):
    class Meta:
        proxy = True
        verbose_name = _('Workflow state runtime proxy')
        verbose_name_plural = _('Workflow state runtime proxies')

    def get_document_count(self, user):
        """
        Return the numeric count of documents at this workflow state.
        The count is filtered by access.
        """
        return AccessControlList.objects.restrict_queryset(
            permission=permission_document_view, queryset=self.get_documents(),
            user=user
        ).count()
