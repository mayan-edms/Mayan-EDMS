from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from mayan.apps.smart_settings.classes import Namespace

namespace = Namespace(label=_('Search'), name='search')

setting_disable_simple_search = namespace.add_setting(
    global_name='SEARCH_DISABLE_SIMPLE_SEARCH',
    default=False, help_text=_(
        'Disables the single term bar search leaving only the advanced '
        'search button.'
    )
)
