from __future__ import absolute_import, unicode_literals

from django.apps import apps
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from mayan.apps.dashboards.classes import DashboardWidgetNumeric

from .icons import icon_role_list
from .permissions import permission_role_view


class DashboardWidgetRoleTotal(DashboardWidgetNumeric):
    icon_class = icon_role_list
    label = _('Total roles')
    link = reverse_lazy(viewname='permissions:role_list')

    def render(self, request):
        AccessControlList = apps.get_model(
            app_label='acls', model_name='AccessControlList'
        )
        Role = apps.get_model(
            app_label='permissions', model_name='Role'
        )

        self.count = AccessControlList.objects.restrict_queryset(
            permission=permission_role_view, user=request.user,
            queryset=Role.objects.all()
        ).count()
        return super(DashboardWidgetRoleTotal, self).render(request)
