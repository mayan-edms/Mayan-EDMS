from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _

from .icons import icon_tag_list
from .cleanup import delete_all_tags

label = _(u'Tagging')
description = _(u'Handles document tagging.')
dependencies = ['app_registry', 'icons', 'navigation']
icon = icon_tag_list
#bootstrap_models = ['taggit.tag', 'tagproperties']
#TODO: Disabled until a solution for natural keys for Tags is found

cleanup_functions = [delete_all_tags]
bootstrap_models = [
    {
        'name': 'taggit.tag',
        'sanitize': False,
    },
    {
        'name': 'tagproperties',
        'dependencies': ['taggit.tag']
    }
]
