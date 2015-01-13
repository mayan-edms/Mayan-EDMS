from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext as _

from documents.models import Document, DocumentType


@python_2_unicode_compatible
class Workflow(models.Model):
    label = models.CharField(max_length=255, unique=True, verbose_name=_('Label'))

    def __str__(self):
        return self.label

    def get_initial_state(self):
        try:
            return self.states.get(initial=True)
        except self.states.model.DoesNotExist:
            return None

    class Meta:
        verbose_name = _('Workflow')
        verbose_name_plural = _('Workflows')


@python_2_unicode_compatible
class WorkflowState(models.Model):
    workflow = models.ForeignKey(Workflow, related_name='states', verbose_name=_('Workflow'))
    label = models.CharField(max_length=255, verbose_name=_('Label'))
    initial = models.BooleanField(default=False, verbose_name=_('Initial'))

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
    workflow = models.ForeignKey(Workflow, related_name='transitions', verbose_name=_('Workflow'))
    label = models.CharField(max_length=255, verbose_name=_('Label'))

    origin_state = models.ForeignKey(WorkflowState, related_name='origins', verbose_name=_('Origin state'))
    destination_state = models.ForeignKey(WorkflowState, related_name='destinations', verbose_name=_('Destination state'))

    def __str__(self):
        return self.label

    class Meta:
        unique_together = ('workflow', 'label', 'origin_state', 'destination_state')
        verbose_name = _('Workflow transition')
        verbose_name_plural = _('Workflow transitions')


@python_2_unicode_compatible
class DocumentTypeWorkflow(models.Model):
    document_type = models.ForeignKey(DocumentType, verbose_name=_('Document type'))
    workflow = models.ForeignKey(Workflow, verbose_name=_('Workflow'))

    def __str__(self):
        return self.label

    class Meta:
        unique_together = ('document_type', 'workflow')
        verbose_name = _('Document type workflow')
        verbose_name_plural = _('Document type workflow')


@python_2_unicode_compatible
class WorkflowInstance(models.Model):
    workflow = models.ForeignKey(Workflow, verbose_name=_('Workflow'))
    document = models.ForeignKey(Document, verbose_name=_('Document'))

    def do_transition(self, transition):
        try:
            if transition in self.get_current_state().origins:
                self.log_entries.create(transition=transition)
        except AttributeError:
            # No initial state has been set for this workflow
            pass

    def get_current_state(self):
        try:
            return self.log_entries.order_by('datetime').last().transition.destination_state
        except AttributeError:
            return self.workflow.get_initial_state()

    def __str__(self):
        return self.label

    class Meta:
        unique_together = ('document', 'workflow')
        verbose_name = _('Workflow instance')
        verbose_name_plural = _('Workflow instances')


@python_2_unicode_compatible
class WorkflowInstanceLogEntry(models.Model):
    workflow_instance = models.ForeignKey(WorkflowInstance, related_name='log_entries', verbose_name=_('Workflow instance'))
    datetime = models.DateTimeField(auto_now_add=True, verbose_name=_('Datetime'))
    transition = models.ForeignKey(WorkflowTransition, verbose_name=_('Transition'))

    def __str__(self):
        return self.label

    class Meta:
        verbose_name = _('Workflow instance log entry')
        verbose_name_plural = _('Workflow instance log entries')
