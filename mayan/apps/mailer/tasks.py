from __future__ import absolute_import

from django.core.mail import EmailMultiAlternatives

from documents.models import Document
from mayan.celery import app


@app.task(ignore_result=True)
def task_send_document(subject_text, body_text_content, sender, recipient, document_ids=None):
    email_msg = EmailMultiAlternatives(subject_text, body_text_content, sender, [recipient])

    if document_ids:
        documents = [Document.objects.get(pk=document_id) for document_id in document_ids]
        for document in documents:
            descriptor = document.open()
            email_msg.attach(document.filename, descriptor.read(), document.file_mimetype)
            descriptor.close()

    email_msg.send()
