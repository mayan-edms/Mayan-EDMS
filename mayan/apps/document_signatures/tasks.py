import logging

from django.apps import apps

from mayan.celery import app

logger = logging.getLogger(name=__name__)


@app.task(bind=True, ignore_result=True)
def task_unverify_key_signatures(self, key_id):
    DetachedSignature = apps.get_model(
        app_label='document_signatures', model_name='DetachedSignature'
    )

    EmbeddedSignature = apps.get_model(
        app_label='document_signatures', model_name='EmbeddedSignature'
    )

    for signature in DetachedSignature.objects.filter(key_id__endswith=key_id).filter(signature_id__isnull=False):
        signature.save()

    for signature in EmbeddedSignature.objects.filter(key_id__endswith=key_id).filter(signature_id__isnull=False):
        signature.save()


@app.task(bind=True, ignore_result=True)
def task_verify_key_signatures(self, key_pk):
    Key = apps.get_model(
        app_label='django_gpg', model_name='Key'
    )

    DetachedSignature = apps.get_model(
        app_label='document_signatures', model_name='DetachedSignature'
    )

    EmbeddedSignature = apps.get_model(
        app_label='document_signatures', model_name='EmbeddedSignature'
    )

    key = Key.objects.get(pk=key_pk)

    for signature in DetachedSignature.objects.filter(key_id__endswith=key.key_id).filter(signature_id__isnull=True):
        signature.save()

    for signature in EmbeddedSignature.objects.filter(key_id__endswith=key.key_id).filter(signature_id__isnull=True):
        signature.save()


@app.task(bind=True, ignore_result=True)
def task_verify_missing_embedded_signature(self):
    EmbeddedSignature = apps.get_model(
        app_label='document_signatures', model_name='EmbeddedSignature'
    )

    for document_file in EmbeddedSignature.objects.unsigned_document_files():
        task_verify_document_file.apply_async(
            kwargs=dict(document_file_pk=document_file.pk)
        )


@app.task(bind=True, ignore_result=True)
def task_verify_document_file(self, document_file_pk):
    DocumentFile = apps.get_model(
        app_label='documents', model_name='DocumentFile'
    )

    EmbeddedSignature = apps.get_model(
        app_label='document_signatures', model_name='EmbeddedSignature'
    )

    document_file = DocumentFile.objects.get(pk=document_file_pk)
    try:
        EmbeddedSignature.objects.create(document_file=document_file)
    except IOError as exception:
        error_message = 'File missing for document file ID {}; {}'.format(
            document_file_pk, exception
        )
        logger.error(error_message)
        raise IOError(error_message)


@app.task(ignore_result=True)
def task_refresh_signature_information():
    DetachedSignature = apps.get_model(
        app_label='document_signatures', model_name='DetachedSignature'
    )
    EmbeddedSignature = apps.get_model(
        app_label='document_signatures', model_name='EmbeddedSignature'
    )

    for signanture in DetachedSignature.objects.all():
        try:
            signanture.save()
        except Exception as exception:
            logger.error(
                'Error refreshing detached signature {} for document file ID {}; {}'.format(
                    signanture, signanture.document_file_id, exception,
                ), exc_info=True
            )
            raise

    for signanture in EmbeddedSignature.objects.all():
        try:
            signanture.save()
        except Exception as exception:
            logger.error(
                'Error refreshing embedded signature {} for document file ID {}; {}'.format(
                    signanture, signanture.document_file_id, exception,
                ), exc_info=True
            )
            raise
