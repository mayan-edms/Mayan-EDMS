from django.utils.translation import ugettext_lazy as _

from mayan.apps.dashboards.classes import Dashboard

dashboard_user = Dashboard(name='user', label=_('User dashboard'))
