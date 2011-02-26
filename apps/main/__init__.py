from django.utils.translation import ugettext_lazy as _

from common.api import register_menu

from permissions import role_list

from documents import document_find_all_duplicates
from filesystem_serving import filesystem_serving_recreate_all_links

check_settings = {'text':_(u'settings'), 'view':'check_settings', 'famfam':'cog'}


register_menu([
    {'text':_(u'home'), 'view':'home', 'famfam':'house', 'position':0},

    {'text':_(u'tools'), 'view':'tools_menu', 'links': [
        document_find_all_duplicates, filesystem_serving_recreate_all_links
        ],'famfam':'wrench', 'name':'tools','position':7},

    {'text':_(u'setup'), 'view':'check_settings', 'links': [
        check_settings, role_list
        ],'famfam':'cog', 'name':'setup','position':8},

    {'text':_(u'about'), 'view':'about', 'position':9},
])
