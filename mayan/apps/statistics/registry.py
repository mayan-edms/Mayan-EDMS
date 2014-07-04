from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from .links import link_statistics

label = _(u'Statistics')
description = _(u'Central place to store and display app statistics.')
tool_links = [link_statistics]
