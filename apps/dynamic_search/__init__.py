from django.utils.translation import ugettext_lazy as _
from common.api import register_menu

register_menu([
    {'text':_(u'search'), 'view':'search', 'famfam':'zoom', 'position':2},
])
