from django.apps import apps
from django.utils import timezone
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

import qsstats

from mayan.apps.mayan_statistics.classes import (
    StatisticLineChart, StatisticNamespace
)

from .permissions import permission_document_view

from .literals import MONTH_NAMES


def get_month_name(month_number):
    return force_text(s=MONTH_NAMES[month_number - 1])


def new_documents_per_month():
    Document = apps.get_model(app_label='documents', model_name='Document')

    qss = qsstats.QuerySetStats(Document.valid.all(), 'datetime_created')

    now = timezone.now().date()
    start = timezone.datetime(year=now.year, month=1, day=1).date()

    return {
        'series': {
            'Documents': map(
                lambda x: {get_month_name(month_number=x[0].month): x[1]},
                qss.time_series(start=start, end=now, interval='months')
            )
        }
    }


def new_document_pages_per_month():
    DocumentFilePage = apps.get_model(
        app_label='documents', model_name='DocumentFilePage'
    )

    qss = qsstats.QuerySetStats(
        DocumentFilePage.valid.all(), 'document_file__document__datetime_created'
    )

    now = timezone.now().date()
    start = timezone.datetime(year=now.year, month=1, day=1).date()

    return {
        'series': {
            'Pages': map(
                lambda x: {get_month_name(month_number=x[0].month): x[1]},
                qss.time_series(start=start, end=now, interval='months')
            )
        }
    }


def new_documents_this_month(user=None):
    AccessControlList = apps.get_model(
        app_label='acls', model_name='AccessControlList'
    )
    Document = apps.get_model(app_label='documents', model_name='Document')

    queryset = Document.valid.all()

    if user:
        queryset = AccessControlList.objects.restrict_queryset(
            permission=permission_document_view, user=user,
            queryset=queryset
        )

    qss = qsstats.QuerySetStats(queryset, 'datetime_created')
    return qss.this_month() or '0'


def new_document_files_per_month():
    DocumentFile = apps.get_model(
        app_label='documents', model_name='DocumentFile'
    )

    qss = qsstats.QuerySetStats(
        DocumentFile.valid.all(), 'document__datetime_created'
    )

    now = timezone.now().date()
    start = timezone.datetime(year=now.year, month=1, day=1).date()

    return {
        'series': {
            'Files': map(
                lambda x: {get_month_name(month_number=x[0].month): x[1]},
                qss.time_series(start=start, end=now, interval='months')
            )
        }
    }


def new_document_pages_this_month(user=None):
    AccessControlList = apps.get_model(
        app_label='acls', model_name='AccessControlList'
    )
    DocumentFilePage = apps.get_model(
        app_label='documents', model_name='DocumentFilePage'
    )

    queryset = DocumentFilePage.valid.all()

    if user:
        queryset = AccessControlList.objects.restrict_queryset(
            permission=permission_document_view, user=user,
            queryset=queryset
        )

    qss = qsstats.QuerySetStats(
        queryset, 'document_file__document__datetime_created'
    )
    return qss.this_month() or '0'


def total_document_per_month():
    Document = apps.get_model(app_label='documents', model_name='Document')

    qss = qsstats.QuerySetStats(Document.valid.all(), 'datetime_created')
    now = timezone.now()

    result = []

    for month in range(1, now.month + 1):
        next_month = month + 1

        if month == 12:
            next_month = 1
            year = now.year + 1
        else:
            next_month = month + 1
            year = now.year

        result.append(
            {
                get_month_name(month_number=month): qss.until(
                    timezone.datetime(year, next_month, 1, tzinfo=now.tzinfo)
                )
            }
        )

    return {
        'series': {
            'Documents': result
        }
    }


def total_document_file_per_month():
    DocumentFile = apps.get_model(
        app_label='documents', model_name='DocumentFile'
    )

    qss = qsstats.QuerySetStats(
        DocumentFile.valid.all(), 'document__datetime_created'
    )
    now = timezone.now()

    result = []

    for month in range(1, now.month + 1):
        next_month = month + 1

        if month == 12:
            next_month = 1
            year = now.year + 1
        else:
            next_month = month + 1
            year = now.year

        result.append(
            {
                get_month_name(month_number=month): qss.until(
                    timezone.datetime(year, next_month, 1, tzinfo=now.tzinfo)
                )
            }
        )

    return {
        'series': {
            'Files': result
        }
    }


def total_document_page_per_month():
    DocumentFilePage = apps.get_model(
        app_label='documents', model_name='DocumentFilePage'
    )

    qss = qsstats.QuerySetStats(
        DocumentFilePage.valid.all(), 'document_file__document__datetime_created'
    )
    now = timezone.now()

    result = []

    for month in range(1, now.month + 1):
        next_month = month + 1

        if month == 12:
            next_month = 1
            year = now.year + 1
        else:
            next_month = month + 1
            year = now.year

        result.append(
            {
                get_month_name(month_number=month): qss.until(
                    timezone.datetime(year, next_month, 1, tzinfo=now.tzinfo)
                )
            }
        )

    return {
        'series': {
            'Pages': result
        }
    }


namespace = StatisticNamespace(slug='documents', label=_('Documents'))
namespace.add_statistic(
    klass=StatisticLineChart,
    slug='new-documents-per-month',
    label=_('New documents per month'),
    func=new_documents_per_month,
    minute='0'
)
namespace.add_statistic(
    klass=StatisticLineChart,
    slug='new-document-files-per-month',
    label=_('New document files per month'),
    func=new_document_files_per_month,
    minute='0'
)
namespace.add_statistic(
    klass=StatisticLineChart,
    slug='new-document-pages-per-month',
    label=_('New document pages per month'),
    func=new_document_pages_per_month,
    minute='0'
)
namespace.add_statistic(
    klass=StatisticLineChart,
    slug='total-documents-at-each-month',
    label=_('Total documents at each month'),
    func=total_document_per_month,
    minute='0'
)
namespace.add_statistic(
    klass=StatisticLineChart,
    slug='total-document-files-at-each-month',
    label=_('Total document files at each month'),
    func=total_document_file_per_month,
    minute='0'
)
namespace.add_statistic(
    klass=StatisticLineChart,
    slug='total-document-pages-at-each-month',
    label=_('Total document pages at each month'),
    func=total_document_page_per_month,
    minute='0'
)
