from __future__ import absolute_import

from django.utils.translation import ugettext as _

from .models import DocumentQueue, QueueDocument


def get_statistics():
    paragraphs = [
        _(u'Document queues: %d') % DocumentQueue.objects.count(),
        _(u'Queued documents: %d') % QueueDocument.objects.only('pk').count()
    ]

    return {
        'title': _(u'OCR statistics'),
        'paragraphs': paragraphs
    }
