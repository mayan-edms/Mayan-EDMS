from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.db.models import Avg, Count, Min, Max

from common.utils import pretty_size, pretty_size_10
from statistics.classes import Statistic

from .models import Document, DocumentType, DocumentPage, DocumentVersion
from .runtime import storage_backend


def get_used_size(path, file_list):
    total_size = 0
    for filename in file_list:
        try:
            total_size += storage_backend.size(storage_backend.separator.join([path, filename]))
        except OSError:
            pass

    return total_size


def storage_count(path='.'):
    try:
        directories, files = storage_backend.listdir(path)
    except OSError:
        return 0, 0
    else:
        total_count = len(files)
        total_size = get_used_size(path, files)

        for directory in directories:
            file_count, files_size = storage_count(directory)
            total_count += file_count
            total_size += files_size

        return total_count, total_size


class DocumentStatistics(Statistic):
    def get_results(self):
        results = []

        results.extend([
            _('Document types: %d') % DocumentType.objects.count(),
        ])
        document_stats = DocumentVersion.objects.annotate(page_count=Count('pages')).aggregate(Min('page_count'), Max('page_count'), Avg('page_count'))
        results.extend([
            _('Minimum amount of pages per document: %d') % (document_stats['page_count__min'] or 0),
            _('Maximum amount of pages per document: %d') % (document_stats['page_count__max'] or 0),
            _('Average amount of pages per document: %f') % (document_stats['page_count__avg'] or 0),
        ])

        return results


class DocumentUsageStatistics(Statistic):
    def get_results(self):
        results = []

        total_db_documents = Document.objects.only('pk',).count()

        results.extend([
            _('Documents in database: %d') % total_db_documents,
        ])

        try:
            total_storage_documents, storage_used_space = storage_count()
            results.append(_('Documents in storage: %d') %
                           total_storage_documents)
            results.append(_('Space used in storage: %(base_2)s (base 2), %(base_10)s (base 10), %(bytes)d bytes') % {
                'base_2': pretty_size(storage_used_space),
                'base_10': pretty_size_10(storage_used_space),
                'bytes': storage_used_space
            })
        except NotImplementedError:
            pass

        results.extend([
            _('Document pages in database: %d') % DocumentPage.objects.only('pk',).count(),
        ])

        return results
