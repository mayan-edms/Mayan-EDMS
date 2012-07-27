from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation.api import Link

maintenance_menu = Link(text=_(u'maintenance'), view='maintenance_menu', sprite='wrench', icon='wrench.png')
