from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation.api import Link

diagnostics = Link(text=_(u'diagnostics'), view='diagnostics', sprite='pill', icon='pill.png')
