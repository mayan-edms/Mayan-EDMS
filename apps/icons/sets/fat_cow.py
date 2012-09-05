import os

from django.utils.translation import ugettext_lazy as _

from icons.literals import *

PATH = os.path.join('fat_cow')
ID = 'fat_cow'
LABEL = _(u'Fat cow')

DICTIONARY = {
    APPLICATION_VIEW_ICONS: 'application_view_icons.png',
    CD_BURN: 'cd_burn.png',
    COG: 'cog.png',
    ERROR: 'error.png',
    GROUP: 'group.png',
    GROUP_ADD: 'group_add.png',
    GROUP_EDIT: 'group_edit.png',
    GROUP_DELETE: 'group_delete.png',
    MEDAL_GOLD: 'medal_gold_1.png',
    MEDAL_GOLD_ADD: 'medal_gold_add.png',
    MEDAL_GOLD_DELETE: 'medal_gold_delete.png',  
    PLUGIN: 'plugin.png',
}
