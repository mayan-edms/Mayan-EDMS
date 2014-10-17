from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

STATE_CHECKED_OUT = 'checkedout'
STATE_CHECKED_IN = 'checkedin'

STATE_LABELS = {
    STATE_CHECKED_OUT: _(u'Checked out'),
    STATE_CHECKED_IN: _(u'Checked in/available'),
}
