from django.apps import apps
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from mayan.apps.dashboards.classes import DashboardWidgetNumeric

from .icons import icon_group_list, icon_user_list
from .permissions import permission_group_view, permission_user_view


class DashboardWidgetUserTotal(DashboardWidgetNumeric):
    icon_class = icon_user_list
    label = _('Total users')
    link = reverse_lazy(viewname='user_management:user_list')

    def render(self, request):
        AccessControlList = apps.get_model(
            app_label='acls', model_name='AccessControlList'
        )
        self.count = AccessControlList.objects.restrict_queryset(
            permission=permission_user_view, user=request.user,
            queryset=get_user_model().objects.all()
        ).count()
        return super(DashboardWidgetUserTotal, self).render(request)


class DashboardWidgetGroupTotal(DashboardWidgetNumeric):
    icon_class = icon_group_list
    label = _('Total groups')
    link = reverse_lazy(viewname='user_management:group_list')

    def render(self, request):
        AccessControlList = apps.get_model(
            app_label='acls', model_name='AccessControlList'
        )
        Group = apps.get_model(
            app_label='auth', model_name='Group'
        )
        self.count = AccessControlList.objects.restrict_queryset(
            permission=permission_group_view, user=request.user,
            queryset=Group.objects.all()
        ).count()
        return super(DashboardWidgetGroupTotal, self).render(request)
