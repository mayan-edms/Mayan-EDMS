from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from navigation import Link

from .icons import icon_diagnostic, icon_diagnostic_execute

diagnostic_list = Link(text=_(u'diagnostics'), view='diagnostic_list', icon=icon_diagnostic)
diagnostic_execute = Link(text=_(u'execute'), view='diagnostic_execute', args='object.id', icon=icon_diagnostic_execute)
