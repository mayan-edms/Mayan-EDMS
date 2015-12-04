from __future__ import unicode_literals

import logging

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import IntegrityError, models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from documents.models import Document, DocumentType

from .managers import WorkflowManager

logger = logging.getLogger(__name__)


@python_2_unicode_compatible
class Workflow(models.Model):
    label = models.CharField(
        max_length=255, unique=True, verbose_name=_('Label')
    )
    document_types = models.ManyToManyField(
        DocumentType, related_name='workflows',
        verbose_name=_('Document types')
    )

    objects = WorkflowManager()

    def __str__(self):
        return self.label

    def get_document_types_not_in_workflow(self):
        return DocumentType.objects.exclude(pk__in=self.document_types.all())

    def get_initial_state(self):
        try:
            return self.states.get(initial=True)
        except self.states.model.DoesNotExist:
            return None

    def launch_for(self, document):
        try:
            logger.info(
                'Launching workflow %s for document %s', self, document
            )
            self.instances.create(document=document)
        except IntegrityError:
            logger.info(
                'Workflow %s already launched for document %s', self, document
            )
        else:
            logger.info(
                'Workflow %s launched for document %s', self, document
            )

    class Meta:
        verbose_name = _('Workflow')
        verbose_name_plural = _('Workflows')


@python_2_unicode_compatible
class WorkflowState(models.Model):
    workflow = models.ForeignKey(
        Workflow, related_name='states', verbose_name=_('Workflow')
    )
    label = models.CharField(max_length=255, verbose_name=_('Label'))
    initial = models.BooleanField(
        default=False,
        help_text=_(
            'Select if this will be the state with which you want the '
            'workflow to start in. Only one state can be the initial state.'
        ), verbose_name=_('Initial')
    )
    completion = models.IntegerField(
        blank=True, default=0, help_text=_(
            'Enter the percent of completion that this state represents in '
            'relation to the workflow. Use numbers without the percent sign.'
        ), verbose_name=_('Completion')
    )

    def __str__(self):
        return self.label

    def save(self, *args, **kwargs):
        if self.initial:
            self.workflow.states.all().update(initial=False)
        return super(WorkflowState, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('workflow', 'label')
        verbose_name = _('Workflow state')
        verbose_name_plural = _('Workflow states')


@python_2_unicode_compatible
class WorkflowTransition(models.Model):
    workflow = models.ForeignKey(
        Workflow, related_name='transitions', verbose_name=_('Workflow')
    )
    label = models.CharField(max_length=255, verbose_name=_('Label'))

    origin_state = models.ForeignKey(
        WorkflowState, related_name='origin_transitions',
        verbose_name=_('Origin state')
    )
    destination_state = models.ForeignKey(
        WorkflowState, related_name='destination_transitions',
        verbose_name=_('Destination state')
    )

    def __str__(self):
        return self.label

    class Meta:
        unique_together = (
            'workflow', 'label', 'origin_state', 'destination_state'
        )
        verbose_name = _('Workflow transition')
        verbose_name_plural = _('Workflow transitions')


@python_2_unicode_compatible
class WorkflowInstance(models.Model):
    workflow = models.ForeignKey(
        Workflow, related_name='instances', verbose_name=_('Workflow')
    )
    document = models.ForeignKey(
        Document, related_name='workflows', verbose_name=_('Document')
    )

    def __str__(self):
        return unicode(self.workflow)

    def get_absolute_url(self):
        return reverse(
            'document_states:workflow_instance_detail', args=(str(self.pk),)
        )

    def do_transition(self, comment, transition, user):
        try:
            if transition in self.get_current_state().origin_transitions.all():
                self.log_entries.create(
                    comment=comment, transition=transition, user=user
                )
        except AttributeError:
            # No initial state has been set for this workflow
            pass

    def get_current_state(self):
        try:
            return self.get_last_transition().destination_state
        except AttributeError:
            return self.workflow.get_initial_state()

    def get_last_log_entry(self):
        try:
            return self.log_entries.order_by('datetime').last()
        except AttributeError:
            return None

    def get_last_transition(self):
        try:
            return self.get_last_log_entry().transition
        except AttributeError:
            return None

    def get_transition_choices(self):
        return self.get_current_state().origin_transitions.all()

    class Meta:
        unique_together = ('document', 'workflow')
        verbose_name = _('Workflow instance')
        verbose_name_plural = _('Workflow instances')


@python_2_unicode_compatible
class WorkflowInstanceLogEntry(models.Model):
    workflow_instance = models.ForeignKey(
        WorkflowInstance, related_name='log_entries',
        verbose_name=_('Workflow instance')
    )
    datetime = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name=_('Datetime')
    )
    transition = models.ForeignKey(
        WorkflowTransition, verbose_name=_('Transition')
    )
    user = models.ForeignKey(User, verbose_name=_('User'))
    comment = models.TextField(blank=True, verbose_name=_('Comment'))

    def __str__(self):
        return unicode(self.transition)

    class Meta:
        verbose_name = _('Workflow instance log entry')
        verbose_name_plural = _('Workflow instance log entries')
