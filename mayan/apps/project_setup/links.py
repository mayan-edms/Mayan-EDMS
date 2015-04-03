from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from navigation import Link

link_setup = Link(icon='fa fa-gear', text=_('Setup'), view='project_setup:setup_list')
