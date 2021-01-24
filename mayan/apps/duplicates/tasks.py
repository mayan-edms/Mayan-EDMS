from django.apps import apps

from mayan.celery import app


@app.task(ignore_result=True)
def task_duplicates_clean_empty_lists():
    DuplicateBackendEntry = apps.get_model(
        app_label='duplicates', model_name='DuplicateBackendEntry'
    )
    DuplicateBackendEntry.objects.clean_empty_duplicate_lists()


@app.task(ignore_result=True)
def task_duplicates_scan_all():
    StoredDuplicateBackend = apps.get_model(
        app_label='duplicates', model_name='StoredDuplicateBackend'
    )

    StoredDuplicateBackend.objects.scan_all()


@app.task(ignore_result=True)
def task_duplicates_scan_for(document_id):
    Document = apps.get_model(
        app_label='documents', model_name='Document'
    )
    StoredDuplicateBackend = apps.get_model(
        app_label='duplicates', model_name='StoredDuplicateBackend'
    )

    document = Document.objects.get(pk=document_id)

    StoredDuplicateBackend.objects.scan_document(document=document)
