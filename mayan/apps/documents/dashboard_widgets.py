from django.apps import apps
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from mayan.apps.dashboards.classes import DashboardWidgetNumeric
from mayan.apps.mayan_statistics.icons import icon_statistics

from .icons import (
    icon_dashboard_documents_in_trash, icon_dashboard_document_types,
    icon_dashboard_pages_per_month, icon_dashboard_new_documents_this_month,
    icon_dashboard_total_document
)
from .permissions import (
    permission_document_view, permission_document_type_view
)
from .statistics import (
    new_document_pages_this_month, new_documents_this_month,
)


class DashboardWidgetDocumentFilePagesTotal(DashboardWidgetNumeric):
    icon = icon_dashboard_pages_per_month
    label = _('Total pages')
    link = reverse_lazy(
        viewname='statistics:statistic_detail', kwargs={
            'slug': 'total-document-pages-at-each-month'
        }
    )
    link_icon = icon_statistics

    def render(self, request):
        AccessControlList = apps.get_model(
            app_label='acls', model_name='AccessControlList'
        )
        DocumentFilePage = apps.get_model(
            app_label='documents', model_name='DocumentFilePage'
        )
        self.count = AccessControlList.objects.restrict_queryset(
            permission=permission_document_view, user=request.user,
            queryset=DocumentFilePage.valid.all()
        ).count()
        return super().render(request)


class DashboardWidgetDocumentsTotal(DashboardWidgetNumeric):
    icon = icon_dashboard_total_document
    label = _('Total documents')
    link = reverse_lazy(viewname='documents:document_list')

    def render(self, request):
        AccessControlList = apps.get_model(
            app_label='acls', model_name='AccessControlList'
        )
        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )
        self.count = AccessControlList.objects.restrict_queryset(
            permission=permission_document_view, user=request.user,
            queryset=Document.valid.all()
        ).count()
        return super().render(request)


class DashboardWidgetDocumentsInTrash(DashboardWidgetNumeric):
    icon = icon_dashboard_documents_in_trash
    label = _('Documents in trash')
    link = reverse_lazy(viewname='documents:document_list_deleted')

    def render(self, request):
        AccessControlList = apps.get_model(
            app_label='acls', model_name='AccessControlList'
        )
        TrashedDocument = apps.get_model(
            app_label='documents', model_name='TrashedDocument'
        )
        self.count = AccessControlList.objects.restrict_queryset(
            permission=permission_document_view, user=request.user,
            queryset=TrashedDocument.objects.all()
        ).count()
        return super().render(request)


class DashboardWidgetDocumentsTypesTotal(DashboardWidgetNumeric):
    icon = icon_dashboard_document_types
    label = _('Document types')
    link = reverse_lazy(viewname='documents:document_type_list')

    def render(self, request):
        AccessControlList = apps.get_model(
            app_label='acls', model_name='AccessControlList'
        )
        DocumentType = apps.get_model(
            app_label='documents', model_name='DocumentType'
        )
        self.count = AccessControlList.objects.restrict_queryset(
            permission=permission_document_type_view, user=request.user,
            queryset=DocumentType.objects.all()
        ).count()
        return super().render(request)


class DashboardWidgetDocumentsNewThisMonth(DashboardWidgetNumeric):
    icon = icon_dashboard_new_documents_this_month
    label = _('New documents this month')
    link = reverse_lazy(
        viewname='statistics:statistic_detail', kwargs={
            'slug': 'new-documents-per-month'
        }
    )
    link_icon = icon_statistics

    def render(self, request):
        self.count = new_documents_this_month(user=request.user)
        return super().render(request)


class DashboardWidgetDocumentsPagesNewThisMonth(DashboardWidgetNumeric):
    icon = icon_dashboard_pages_per_month
    label = _('New pages this month')
    link = reverse_lazy(
        viewname='statistics:statistic_detail', kwargs={
            'slug': 'new-document-pages-per-month'
        }
    )
    link_icon = icon_statistics

    def render(self, request):
        self.count = new_document_pages_this_month(user=request.user)
        return super().render(request)
