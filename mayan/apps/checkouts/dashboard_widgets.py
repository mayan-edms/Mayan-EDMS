from __future__ import absolute_import, unicode_literals

from django.apps import apps
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from common.classes import DashboardWidget

from .icons import icon_dashboard_checkouts


def checkedout_documents_queryset():
    DocumentCheckout = apps.get_model(
        app_label='checkouts', model_name='DocumentCheckout'
    )
    return DocumentCheckout.objects.all()


widget_checkouts = DashboardWidget(
    icon_class=icon_dashboard_checkouts,
    label=_('Checkedout documents'),
    link=reverse_lazy('checkouts:checkout_list'),
    queryset=checkedout_documents_queryset
)
