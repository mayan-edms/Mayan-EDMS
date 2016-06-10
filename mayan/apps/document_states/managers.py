from __future__ import unicode_literals

from django.apps import apps
from django.db import models

from organizations.managers import CurrentOrganizationManager


class OrganizationWorkflowStateManager(models.Manager):
    def get_queryset(self):
        Workflow = apps.get_model('document_states', 'Workflow')

        return super(
            OrganizationWorkflowStateManager, self
        ).get_queryset().filter(
            workflow__in=Workflow.on_organization.all(),
        )


class OrganizationWorkflowTransitionManager(models.Manager):
    def get_queryset(self):
        Workflow = apps.get_model('document_states', 'Workflow')

        return super(
            OrganizationWorkflowTransitionManager, self
        ).get_queryset().filter(
            workflow__in=Workflow.on_organization.all(),
        )


class OrganizationWorkflowInstanceManager(models.Manager):
    def get_queryset(self):
        Document = apps.get_model('documents', 'Document')
        Workflow = apps.get_model('document_states', 'Workflow')

        return super(
            OrganizationWorkflowInstanceManager, self
        ).get_queryset().filter(
            workflow__in=Workflow.on_organization.all(),
            document__in=Document.on_organization.all(),
        )


class OrganizationWorkflowInstanceLogEntryManager(models.Manager):
    def get_queryset(self):
        Workflow = apps.get_model('document_states', 'Workflow')

        return super(
            OrganizationWorkflowInstanceLogEntryManager, self
        ).get_queryset().filter(
            workflow_instance__workflow__in=Workflow.on_organization.all(),
        )


class WorkflowManager(models.Manager):
    def launch_for(self, document):
        for workflow in document.document_type.workflows.all():
            workflow.launch_for(document)


class OrganizationWorkflowManager(WorkflowManager, CurrentOrganizationManager):
    pass
