'''Configuration options for the main app
'''

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

SIDE_BAR_SEARCH = getattr(settings, 'MAIN_SIDE_BAR_SEARCH', False)

setting_description = {
    'MAIN_SIDE_BAR_SEARCH': _(u'Controls whether the search\
     functionality is provided by a sidebar widget or by a menu entry.')
}
