from django.apps import apps

from mayan.celery import app


@app.task(ignore_result=True)
def task_duplicates_clean_empty_lists():
    DuplicatedDocument = apps.get_model(
        app_label='duplicates', model_name='DuplicatedDocument'
    )
    DuplicatedDocument.objects.clean_empty_duplicate_lists()


@app.task(ignore_result=True)
def task_duplicates_scan_all():
    DuplicatedDocument = apps.get_model(
        app_label='duplicates', model_name='DuplicatedDocument'
    )

    DuplicatedDocument.objects.scan()


@app.task(ignore_result=True)
def task_duplicates_scan_for(document_id):
    Document = apps.get_model(
        app_label='documents', model_name='Document'
    )
    DuplicatedDocument = apps.get_model(
        app_label='duplicates', model_name='DuplicatedDocument'
    )

    document = Document.objects.get(pk=document_id)

    DuplicatedDocument.objects.scan_for(document=document)
