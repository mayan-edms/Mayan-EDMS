from __future__ import absolute_import, unicode_literals

from django.apps import apps
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from common.classes import DashboardWidgetNumeric
from documents.permissions import permission_document_view

from .icons import icon_dashboard_checkouts
from .permissions import permission_document_checkout_detail_view


class DashboardWidgetTotalCheckouts(DashboardWidgetNumeric):
    icon_class = icon_dashboard_checkouts
    label = _('Checkedout documents')
    link = reverse_lazy('checkouts:checkout_list')

    def render(self, request):
        AccessControlList = apps.get_model(
            app_label='acls', model_name='AccessControlList'
        )
        DocumentCheckout = apps.get_model(
            app_label='checkouts', model_name='DocumentCheckout'
        )
        queryset = AccessControlList.objects.filter_by_access(
            permission=permission_document_checkout_detail_view,
            user=request.user,
            queryset=DocumentCheckout.objects.checked_out_documents()
        )
        queryset = AccessControlList.objects.filter_by_access(
            permission=permission_document_view, user=request.user,
            queryset=queryset
        )
        self.count = queryset.count()
        return super(DashboardWidgetTotalCheckouts, self).render(request)
