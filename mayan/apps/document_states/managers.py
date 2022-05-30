from django.db import models


class WorkflowManager(models.Manager):
    def launch_for(self, document, user=None):
        for workflow_template in document.document_type.workflows.all():
            if workflow_template.auto_launch:
                workflow_template.launch_for(document=document, user=user)


class ValidWorkflowInstanceManager(models.Manager):
    def get_queryset(self):
        return models.QuerySet(
            model=self.model, using=self._db
        ).filter(document__in_trash=False)
