from django.db import models


class WorkflowManager(models.Manager):
    def launch_for(self, document):
        for workflow in document.document_type.workflows.all():
            if workflow.auto_launch:
                workflow.launch_for(document=document)
