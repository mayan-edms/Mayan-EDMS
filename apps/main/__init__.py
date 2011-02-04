from django.utils.translation import ugettext_lazy as _

from common.api import register_menu


register_menu([
    {'text':_(u'home'), 'view':'home', 'famfam':'house', 'position':0},

    #{'text':_(u'setup'), 'view':'', 'links': [
    #],'famfam':'cog', 'name':'setup','position':7},

    {'text':_(u'about'), 'view':'about', 'position':8},
])
