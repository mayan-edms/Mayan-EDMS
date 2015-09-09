from __future__ import absolute_import, unicode_literals

import datetime

import qsstats

from django.db.models import Avg, Count, Max, Min
from django.template.defaultfilters import filesizeformat
from django.utils import formats
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from statistics.classes import Statistic

from .models import Document, DocumentType, DocumentPage, DocumentVersion
from .runtime import storage_backend


def get_used_size(path, file_list):
    total_size = 0
    for filename in file_list:
        try:
            total_size += storage_backend.size(
                storage_backend.separator.join([path, filename])
            )
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


def new_documents_per_month():
    qss = qsstats.QuerySetStats(Document.passthrough.all(), 'date_added')

    today = datetime.date.today()
    this_year = datetime.date(year=today.year, month=1, day=1)

    return {
        'series': {
            'Document': map(lambda x: {x[0].month: x[1]}, qss.time_series(start=this_year, end=today, interval='months'))
        }
    }


def new_document_versions_per_month():
    qss = qsstats.QuerySetStats(DocumentVersion.objects.all(), 'document__date_added')

    today = datetime.date.today()
    this_year = datetime.date(year=today.year, month=1, day=1)

    return {
        'series': {
            'Document': map(lambda x: {x[0].month: x[1]}, qss.time_series(start=this_year, end=today, interval='months'))
        }
    }


def new_document_pages_per_month():
    qss = qsstats.QuerySetStats(DocumentPage.objects.all(), 'document_version__document__date_added')

    today = datetime.date.today()
    this_year = datetime.date(year=today.year, month=1, day=1)

    return {
        'series': {
            'Document': map(lambda x: {x[0].month: x[1]}, qss.time_series(start=this_year, end=today, interval='months'))
        }
    }


"""

class DocumentUsageStatistics(Statistic):
    def get_results(self):
        results = []

        total_db_documents = Document.objects.only('pk',).count()

        results.extend(
            [
                _('Documents in database: %d') % total_db_documents,
            ]
        )

        try:
            total_storage_documents, storage_used_space = storage_count()
            results.append(
                _('Documents in storage: %d') % total_storage_documents
            )
            results.append(
                _(
                    'Space used in storage: %s'
                ) % filesizeformat(storage_used_space)
            )
        except NotImplementedError:
            pass

        results.extend(
            [
                _(
                    'Document pages in database: %d'
                ) % DocumentPage.objects.only('pk',).count(),
            ]
        )

        return results
"""
