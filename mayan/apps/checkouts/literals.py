from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

STATE_CHECKED_OUT = 'checkedout'
STATE_CHECKED_IN = 'checkedin'

STATE_LABELS = {
    STATE_CHECKED_OUT: _('Checked out'),
    STATE_CHECKED_IN: _('Checked in/available'),
}
