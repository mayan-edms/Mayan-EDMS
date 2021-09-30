from django.apps import apps
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from mayan.apps.dashboards.classes import (
    DashboardWidgetList, DashboardWidgetNumeric
)
from mayan.apps.mayan_statistics.icons import icon_statistics

from .icons import (
    icon_dashboard_documents_in_trash, icon_dashboard_document_types,
    icon_dashboard_pages_per_month, icon_dashboard_new_documents_this_month,
    icon_dashboard_total_document,

    icon_document_recently_accessed_list
)
from .links.document_links import (
    link_document_recently_accessed_list,
    link_document_recently_created_list
)
from .links.favorite_links import link_document_favorites_list
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

    def get_count(self):
        AccessControlList = apps.get_model(
            app_label='acls', model_name='AccessControlList'
        )
        DocumentFilePage = apps.get_model(
            app_label='documents', model_name='DocumentFilePage'
        )
        return AccessControlList.objects.restrict_queryset(
            permission=permission_document_view, user=self.request.user,
            queryset=DocumentFilePage.valid.all()
        ).count()


class DashboardWidgetDocumentsTotal(DashboardWidgetNumeric):
    icon = icon_dashboard_total_document
    label = _('Total documents')
    link = reverse_lazy(viewname='documents:document_list')

    def get_count(self):
        AccessControlList = apps.get_model(
            app_label='acls', model_name='AccessControlList'
        )
        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )
        return AccessControlList.objects.restrict_queryset(
            permission=permission_document_view, user=self.request.user,
            queryset=Document.valid.all()
        ).count()


class DashboardWidgetDocumentsInTrash(DashboardWidgetNumeric):
    icon = icon_dashboard_documents_in_trash
    label = _('Documents in trash')
    link = reverse_lazy(viewname='documents:document_list_deleted')

    def get_count(self):
        AccessControlList = apps.get_model(
            app_label='acls', model_name='AccessControlList'
        )
        TrashedDocument = apps.get_model(
            app_label='documents', model_name='TrashedDocument'
        )
        return AccessControlList.objects.restrict_queryset(
            permission=permission_document_view, user=self.request.user,
            queryset=TrashedDocument.objects.all()
        ).count()


class DashboardWidgetDocumentsTypesTotal(DashboardWidgetNumeric):
    icon = icon_dashboard_document_types
    label = _('Document types')
    link = reverse_lazy(viewname='documents:document_type_list')

    def get_count(self):
        AccessControlList = apps.get_model(
            app_label='acls', model_name='AccessControlList'
        )
        DocumentType = apps.get_model(
            app_label='documents', model_name='DocumentType'
        )
        return AccessControlList.objects.restrict_queryset(
            permission=permission_document_type_view, user=self.request.user,
            queryset=DocumentType.objects.all()
        ).count()


class DashboardWidgetDocumentsNewThisMonth(DashboardWidgetNumeric):
    icon = icon_dashboard_new_documents_this_month
    label = _('New documents this month')
    link = reverse_lazy(
        viewname='statistics:statistic_detail', kwargs={
            'slug': 'new-documents-per-month'
        }
    )
    link_icon = icon_statistics

    def get_count(self):
        return new_documents_this_month(user=self.request.user)


class DashboardWidgetDocumentsPagesNewThisMonth(DashboardWidgetNumeric):
    icon = icon_dashboard_pages_per_month
    label = _('New pages this month')
    link = reverse_lazy(
        viewname='statistics:statistic_detail', kwargs={
            'slug': 'new-document-pages-per-month'
        }
    )
    link_icon = icon_statistics

    def get_count(self):
        return new_document_pages_this_month(user=self.request.user)


class DashboardWidgetUserRecentlyAccessedDocuments(DashboardWidgetList):
    columns = ('datetime_accessed', 'label',)
    icon = icon_document_recently_accessed_list
    label = link_document_recently_accessed_list.text
    link = reverse_lazy(
        viewname=link_document_recently_accessed_list.view
    )

    def get_object_list(self):
        RecentlyAccessedDocument = apps.get_model(
            app_label='documents', model_name='RecentlyAccessedDocument'
        )

        return RecentlyAccessedDocument.valid.get_for_user(
            user=self.request.user
        )


class DashboardWidgetUserRecentlyCreatedDocuments(DashboardWidgetList):
    columns = ('datetime_created', 'label',)
    icon = link_document_recently_created_list.icon
    label = link_document_recently_created_list.text
    link = reverse_lazy(
        viewname=link_document_recently_created_list.view
    )

    def get_object_list(self):
        AccessControlList = apps.get_model(
            app_label='acls', model_name='AccessControlList'
        )
        RecentlyCreatedDocument = apps.get_model(
            app_label='documents', model_name='RecentlyCreatedDocument'
        )

        queryset = RecentlyCreatedDocument.valid.all()

        return AccessControlList.objects.restrict_queryset(
            permission=permission_document_type_view, user=self.request.user,
            queryset=queryset
        )


class DashboardWidgetUserFavoriteDocuments(DashboardWidgetList):
    columns = ('datetime_added', 'label',)
    icon = link_document_favorites_list.icon
    label = link_document_favorites_list.text
    link = reverse_lazy(
        viewname=link_document_favorites_list.view
    )

    def get_object_list(self):
        FavoriteDocument = apps.get_model(
            app_label='documents', model_name='FavoriteDocument'
        )

        return FavoriteDocument.valid.get_for_user(
            user=self.request.user
        )
