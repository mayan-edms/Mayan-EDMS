from django.apps import apps

from mayan.celery import app
from mayan.apps.lock_manager.exceptions import LockError


@app.task(ignore_result=True)
def task_duplicates_clean_empty_lists():
    DuplicateBackendEntry = apps.get_model(
        app_label='duplicates', model_name='DuplicateBackendEntry'
    )
    DuplicateBackendEntry.objects.clean_empty_duplicate_lists()


@app.task(ignore_result=True)
def task_duplicates_scan_all():
    Document = apps.get_model(
        app_label='documents', model_name='Document'
    )

    for document in Document.valid.all():
        task_duplicates_scan_for.apply_async(
            kwargs={
                'document_id': document.pk
            }
        )


@app.task(bind=True, ignore_result=True)
def task_duplicates_scan_for(self, document_id):
    Document = apps.get_model(
        app_label='documents', model_name='Document'
    )
    StoredDuplicateBackend = apps.get_model(
        app_label='duplicates', model_name='StoredDuplicateBackend'
    )

    document = Document.objects.get(pk=document_id)

    try:
        StoredDuplicateBackend.objects.scan_document(
            document=document
        )
    except LockError as exception:
        raise self.retry(exc=exception)
