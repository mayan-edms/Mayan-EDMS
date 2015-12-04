from __future__ import unicode_literals

from django.core.mail import EmailMultiAlternatives

from documents.models import Document
from mayan.celery import app

from .models import LogEntry


@app.task(ignore_result=True)
def task_send_document(subject_text, body_text_content, sender, recipient, document_id, as_attachment=False):
    email_msg = EmailMultiAlternatives(
        subject_text, body_text_content, sender, [recipient]
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
        LogEntry.objects.create(message=exception)
    else:
        LogEntry.objects.all().delete()
