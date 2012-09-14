from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation import Link

from .permissions import PERMISSION_INSTALLATION_DETAILS

installation_details = Link(text=_(u'installation details'), view='installation_details', icon='interface_preferences.png', permissions=[PERMISSION_INSTALLATION_DETAILS])
