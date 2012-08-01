from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

STATE_CHECKED_OUT = 'checkedout'
STATE_CHECKED_IN = 'checkedin'

STATE_ICONS = {
    STATE_CHECKED_OUT: 'basket_put.png',
    STATE_CHECKED_IN: 'traffic_lights_green.png',
}

STATE_LABELS = {
    STATE_CHECKED_OUT: _(u'checked out'),
    STATE_CHECKED_IN: _(u'checked in/available'),
}

CHECK_EXPIRED_CHECK_OUTS_INTERVAL = 60  # Lowest check out expiration allowed
