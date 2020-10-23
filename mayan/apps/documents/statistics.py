from django.apps import apps
from django.utils import timezone
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

import qsstats

from mayan.apps.mayan_statistics.classes import (
    StatisticLineChart, StatisticNamespace
)

from .permissions import permission_document_view

MONTH_NAMES = [
    _('January'), _('February'), _('March'), _('April'), _('May'),
    _('June'), _('July'), _('August'), _('September'), _('October'),
    _('November'), _('December')
]


def get_month_name(month_number):
    return force_text(s=MONTH_NAMES[month_number - 1])


def new_documents_per_month():
    Document = apps.get_model(app_label='documents', model_name='Document')

    qss = qsstats.QuerySetStats(Document.objects.all(), 'date_added')

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
    DocumentPage = apps.get_model(
        app_label='documents', model_name='DocumentPage'
    )

    qss = qsstats.QuerySetStats(
        DocumentPage.objects.all(), 'document_version__document__date_added'
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

    queryset = Document.objects.all()

    if user:
        queryset = AccessControlList.objects.restrict_queryset(
            permission=permission_document_view, user=user,
            queryset=queryset
        )

    qss = qsstats.QuerySetStats(queryset, 'date_added')
    return qss.this_month() or '0'


def new_document_versions_per_month():
    DocumentVersion = apps.get_model(
        app_label='documents', model_name='DocumentVersion'
    )

    qss = qsstats.QuerySetStats(
        DocumentVersion.objects.all(), 'document__date_added'
    )

    now = timezone.now().date()
    start = timezone.datetime(year=now.year, month=1, day=1).date()

    return {
        'series': {
            'Versions': map(
                lambda x: {get_month_name(month_number=x[0].month): x[1]},
                qss.time_series(start=start, end=now, interval='months')
            )
        }
    }


def new_document_pages_this_month(user=None):
    AccessControlList = apps.get_model(
        app_label='acls', model_name='AccessControlList'
    )
    DocumentPage = apps.get_model(
        app_label='documents', model_name='DocumentPage'
    )

    queryset = DocumentPage.objects.all()

    if user:
        queryset = AccessControlList.objects.restrict_queryset(
            permission=permission_document_view, user=user,
            queryset=queryset
        )

    qss = qsstats.QuerySetStats(
        queryset, 'document_version__document__date_added'
    )
    return qss.this_month() or '0'


def total_document_per_month():
    Document = apps.get_model(app_label='documents', model_name='Document')

    qss = qsstats.QuerySetStats(Document.objects.all(), 'date_added')
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


def total_document_version_per_month():
    DocumentVersion = apps.get_model(
        app_label='documents', model_name='DocumentVersion'
    )

    qss = qsstats.QuerySetStats(
        DocumentVersion.objects.all(), 'document__date_added'
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
            'Versions': result
        }
    }


def total_document_page_per_month():
    DocumentPage = apps.get_model(
        app_label='documents', model_name='DocumentPage'
    )

    qss = qsstats.QuerySetStats(
        DocumentPage.objects.all(), 'document_version__document__date_added'
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
    slug='new-document-versions-per-month',
    label=_('New document versions per month'),
    func=new_document_versions_per_month,
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
    slug='total-document-versions-at-each-month',
    label=_('Total document versions at each month'),
    func=total_document_version_per_month,
    minute='0'
)
namespace.add_statistic(
    klass=StatisticLineChart,
    slug='total-document-pages-at-each-month',
    label=_('Total document pages at each month'),
    func=total_document_page_per_month,
    minute='0'
)
