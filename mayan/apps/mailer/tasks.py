from django.apps import apps

from mayan.celery import app


@app.task(ignore_result=True)
def task_send_document(body, sender, subject, recipient, user_mailer_id, as_attachment=False, document_id=None):
    Document = apps.get_model(
        app_label='documents', model_name='Document'
    )
    UserMailer = apps.get_model(
        app_label='mailer', model_name='UserMailer'
    )

    if document_id:
        document = Document.objects.get(pk=document_id)
    else:
        document = None

    user_mailer = UserMailer.objects.get(pk=user_mailer_id)

    user_mailer.send_document(
        as_attachment=as_attachment, body=body, document=document,
        subject=subject, to=recipient
    )
