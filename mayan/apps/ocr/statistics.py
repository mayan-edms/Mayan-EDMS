from __future__ import absolute_import

from django.utils.translation import ugettext as _

from statistics.classes import Statistic

from .models import DocumentQueue, QueueDocument


class OCRStatistics(Statistic):
    def get_results(self):
        results = []

        results.extend([
            _(u'Document queues: %d') % DocumentQueue.objects.count(),
            _(u'Queued documents: %d') % QueueDocument.objects.only('pk').count()
        ])

        return results
