from django.utils.translation import ugettext_lazy as _

from common.api import register_menu

from permissions import role_list


check_settings = {'text':_(u'settings'), 'view':'check_settings', 'famfam':'cog'}


register_menu([
    {'text':_(u'home'), 'view':'home', 'famfam':'house', 'position':0},

    {'text':_(u'setup'), 'view':'check_settings', 'links': [
        check_settings, role_list
        ],'famfam':'cog', 'name':'setup','position':7},

    {'text':_(u'about'), 'view':'about', 'position':8},
])
