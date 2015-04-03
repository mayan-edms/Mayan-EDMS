from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from navigation import Link

link_tools = Link(icon='fa fa-wrench', text=_('Tools'), view='project_tools:tools_list')
