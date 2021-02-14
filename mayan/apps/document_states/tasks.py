import logging

from django.apps import apps

from mayan.celery import app

from mayan.apps.lock_manager.exceptions import LockError

from .literals import TASK_GENERATE_WORKFLOW_IMAGE_RETRY_DELAY

logger = logging.getLogger(name=__name__)


@app.task(
    bind=True, default_retry_delay=TASK_GENERATE_WORKFLOW_IMAGE_RETRY_DELAY
)
def task_generate_workflow_image(self, document_state_id):
    Workflow = apps.get_model(
        app_label='document_states', model_name='Workflow'
    )

    workflow = Workflow.objects.get(pk=document_state_id)

    try:
        return workflow.generate_image()
    except LockError as exception:
        logger.warning(
            'LockError during attempt to generate workflow "%s" image. '
            'Retrying.', workflow.internal_name
        )
        raise self.retry(exc=exception)


@app.task(ignore_result=True)
def task_launch_all_workflows():
    Document = apps.get_model(app_label='documents', model_name='Document')
    Workflow = apps.get_model(
        app_label='document_states', model_name='Workflow'
    )

    logger.info('Start launching workflows')
    for document in Document.valid.all():
        Workflow.objects.launch_for(document=document)

    logger.info('Finished launching workflows')


@app.task(ignore_result=True)
def task_launch_workflow(workflow_id):
    Document = apps.get_model(app_label='documents', model_name='Document')
    Workflow = apps.get_model(
        app_label='document_states', model_name='Workflow'
    )

    workflow = Workflow.objects.get(pk=workflow_id)

    logger.info('Start launching workflow: %d', workflow_id)
    for document in Document.valid.filter(document_type__in=workflow.document_types.all()):
        workflow.launch_for(document=document)

    logger.info('Finished launching workflow: %d', workflow_id)


@app.task(ignore_result=True)
def task_launch_workflow_for(document_id, workflow_id):
    Document = apps.get_model(app_label='documents', model_name='Document')
    Workflow = apps.get_model(
        app_label='document_states', model_name='Workflow'
    )

    document = Document.valid.get(pk=document_id)
    workflow = Workflow.objects.get(pk=workflow_id)

    logger.info(
        'Start launching workflow: %d for document: %d',
        workflow_id, document_id
    )
    workflow.launch_for(document=document)

    logger.info(
        'Finished launching workflow: %d for document: %d', workflow_id,
        document_id
    )


@app.task(ignore_result=True)
def task_launch_all_workflow_for(document_id):
    Document = apps.get_model(app_label='documents', model_name='Document')
    Workflow = apps.get_model(
        app_label='document_states', model_name='Workflow'
    )

    document = Document.valid.get(pk=document_id)

    logger.info(
        'Start launching all workflows for document: %d', document_id
    )
    Workflow.objects.launch_for(document=document)

    logger.info(
        'Finished launching all workflows for document: %d', document_id
    )
