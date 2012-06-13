from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.conf import settings

from .literals import STATE_CHECKED_OUT, STATE_CHECKED_IN, STATE_ICONS, STATE_LABELS


def checkout_widget(document):
    checkout_state = document.checkout_state()

    widget = (u'<img style="vertical-align: middle;" src="%simages/icons/%s" />' % (settings.STATIC_URL, STATE_ICONS[checkout_state]))
    return _(u'Document status: %(widget)s %(text)s') % {
        'widget': mark_safe(widget),
        'text': STATE_LABELS[checkout_state]
    }
