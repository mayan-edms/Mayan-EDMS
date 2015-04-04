from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from navigation import Link

link_events_list = Link(icon='fa fa-list-ol', text=_('Events'), view='events:events_list')
