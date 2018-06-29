from __future__ import absolute_import, unicode_literals

from django.apps import apps
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from common.classes import DashboardWidget

from .icons import (
    icon_dashboard_documents_in_trash, icon_dashboard_document_types,
    icon_dashboard_pages_per_month, icon_dashboard_new_documents_this_month,
    icon_dashboard_total_document
)
from .statistics import (
    new_document_pages_this_month, new_documents_this_month,
)


def get_total_documents_queryset():
    Document = apps.get_model(
        app_label='documents', model_name='Document'
    )
    return Document.objects.all()


def get_document_types_queryset():
    DocumentType = apps.get_model(
        app_label='documents', model_name='DocumentType'
    )
    return DocumentType.objects.all()


def get_deleted_documents_queryset():
    DeletedDocument = apps.get_model(
        app_label='documents', model_name='DeletedDocument'
    )
    return DeletedDocument.objects.all()


widget_pages_per_month = DashboardWidget(
    func=new_document_pages_this_month,
    icon_class=icon_dashboard_pages_per_month,
    label=_('New pages this month'),
    link=reverse_lazy(
        'statistics:statistic_detail',
        args=('new-document-pages-per-month',)
    )
)

widget_new_documents_this_month = DashboardWidget(
    func=new_documents_this_month,
    icon_class=icon_dashboard_new_documents_this_month,
    label=_('New documents this month'),
    link=reverse_lazy(
        'statistics:statistic_detail',
        args=('new-documents-per-month',)
    )
)

widget_total_documents = DashboardWidget(
    icon_class=icon_dashboard_total_document,
    queryset=get_total_documents_queryset,
    label=_('Total documents'),
    link=reverse_lazy('documents:document_list')
)


widget_document_types = DashboardWidget(
    icon_class=icon_dashboard_document_types,
    queryset=get_document_types_queryset,
    label=_('Document types'),
    link=reverse_lazy('documents:document_type_list')
)


widget_documents_in_trash = DashboardWidget(
    icon_class=icon_dashboard_documents_in_trash,
    queryset=get_deleted_documents_queryset,
    label=_('Documents in trash'),
    link=reverse_lazy('documents:document_list_deleted')
)
