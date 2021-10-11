from django.utils.translation import ugettext_lazy as _

from .classes import Dashboard

dashboard_administrator = Dashboard(
    name='administrator', label=_('Administrator dashboard')
)
