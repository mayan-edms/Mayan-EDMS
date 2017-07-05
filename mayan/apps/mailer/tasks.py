from __future__ import unicode_literals

from django.apps import apps
from django.core.mail import EmailMultiAlternatives

from documents.models import Document
from mayan.celery import app


@app.task(ignore_result=True)
def task_send_document(subject_text, body_text_content, sender, recipient, document_id, user_mailer_id, as_attachment=False):
    UserMailer = apps.get_model(
        app_label='mailer', model_name='UserMailer'
    )

    user_mailer = UserMailer.objects.get(pk=user_mailer_id)

    connection = user_mailer.get_connection()

    email_msg = EmailMultiAlternatives(
        subject_text, body_text_content, sender, [recipient],
        connection=connection,
    )

    if as_attachment:
        document = Document.objects.get(pk=document_id)
        with document.open() as descriptor:
            email_msg.attach(
                document.label, descriptor.read(), document.file_mimetype
            )

    try:
        email_msg.send()
    except Exception as exception:
        user_mailer.error_log.create(message=exception)
    else:
        user_mailer.error_log.all().delete()
