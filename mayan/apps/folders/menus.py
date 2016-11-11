from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from navigation import Menu

menu_folders = Menu(
    icon='fa fa-folder', label=_('Folders'), name='folders menu'
)
